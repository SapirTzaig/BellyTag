from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto3
import csv
import os
import bcrypt
import hashlib
import PyPDF2
import pdfplumber
from pdfminer.high_level import extract_text
import os
import pytesseract
from PIL import Image
from flask_cors import CORS
import datetime
from werkzeug.utils import secure_filename
import json
import google.generativeai as genai
from decimal import Decimal
import re







# Initialize the app
app = Flask(__name__)

CORS(app)

# Set up the upload folder and allowed file types
UPLOAD_FOLDER = r'C:\Users\sapir\Documents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

### file functions
prenatal_tests = {
    "Ultrasound for Fetal Nuchal Translucency": [
        ("Nuchal Translucency", "float", 3.0, 1.0, "mm"),
        ("Crown Rump Length", "float", 85.0, 30.0, "mm"),
        ("Fetal Heart Rate", "float", 180.0, 110.0, "bpm"),
        ("Biparietal diameter", "float", 90.0, 30.0, "mm"),
    ],
    "Ultrasound for Fetal Nasal Bone Determination": [
        ("Nasal Bone Visible", "boolean", "normal", "normal", "present/absent")
    ],
    "Maternal Serum (Blood) Tests": [
        ("Pregnancy Associated Plasma Protein A", "float", 2.0, 0.5, "MoM"),
        ("Human Chorionic Gonadotropin", "float", 2.5, 0.5, "MoM")
    ],
    "Genetic Screening Recommendation": [
        ("Genetic Counseling Recommended", "boolean", "normal", "normal", "needed/not needed"),
        ("Additional Testing Needed", "boolean", "normal", "normal", "needed/not needed"),
        ("Additional Tests", "list", "normal", "normal", "number of tests")
    ],
    "Multiple Marker Blood Tests (Second Trimester)": [
        ("AFP Screening", "float", 2.5, 0.5, "MoM"),
        ("Estriol", "float", 2.5, 0.5, "MoM"),
        ("Inhibin", "float", 2.0, 0.5, "MoM"),
        ("Human Chorionic Gonadotropin", "float", 3.0, 0.5, "MoM")
    ],
    "Possible Abnormal Indications": [
        ("Abnormal AFP", "boolean", "normal", "normal", "abnormal/normal"),
        ("Miscalculated Due Date", "boolean", "normal", "normal", "correct/incorrect"),
        ("Fetal Abdominal Wall Defects", "boolean", "normal", "normal", "present/absent"),
        ("Chromosomal Abnormalities", "boolean", "normal", "normal", "detected/not detected"),
        ("Open Neural Tube Defects", "boolean", "normal", "normal", "present/absent"),
        ("Multiple Fetuses Detected", "boolean", "normal", "normal", "detected/not detected")
    ],
    "Follow-up Testing": [
        ("Ultrasound Recommended", "boolean", "normal", "normal", "needed/not needed"),
        ("Amniocentesis Needed", "boolean", "normal", "normal", "needed/not needed")
    ],
    "Screening Accuracy": [
        ("False Positive Risk", "float", 5.0, 1.0, "%"),
        ("False Negative Risk", "float", 5.0, 1.0, "%")
    ],
    "Group B Streptococcus Presence": [
        ("Result", "boolean", "normal", "normal", "positive/negative")
    ]
}


# Simple hashing function using SHA-256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def file_to_text(file_path):
    text = ""

    # Try extracting text using PyPDF2
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PyPDF2 failed: {e}")

    # If PyPDF2 fails, try using pdfplumber
    if not text.strip():
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                print("Text extracted successfully using pdfplumber.")
        except Exception as e:
            print(f"pdfplumber failed: {e}")

    # If pdfplumber fails, try pdfminer.six
    if not text.strip():
        try:
            text = extract_text(file_path)
            if text.strip():
                print("Text extracted successfully using pdfminer.six.")
        except Exception as e:
            print(f"pdfminer failed: {e}")

    return text.strip()  # Remove any leading/trailing whitespace


def image_to_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()  # Remove any leading/trailing whitespace


def file_to_attributes(file_path, prenatal_test):
    if file_path[-3:] == "pdf":
        text = file_to_text(file_path)
    elif file_path[-3:] == "png" or file_path[-3:] == "jpg" or file_path[-4:] == "jpeg":
        text = image_to_text(file_path)

    kvp = prenatal_tests[prenatal_test]

    # Extract text
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    prompt = text.replace("\n", " ")
    prompt += "\n\nI want you to get from the text the following parameters and their values " \
                "(the desired type is provided) and the metric (mm/cm/bpm etc...). " \
                "If something doesn't exist, put None instead:\n"

    for key, value, high, low, unit in kvp:
        prompt += f"name: {key} value: {value} min: {low} max: {high} unit: {unit}\n"

    prompt += "I want only the parameters, values of the parameters, high values and low values with the ones" \
                " I gave you, and the metric, no * or bullet points or the opening line, i want a list of the" \
                " example of the format I want: [{ 'name': 'Hemoglobin', 'value': 11, 'min': 12, 'max': 16, 'unit': 'MoM' },...]" \
                "you should return it to me as a Text (not json), and I want to be able to take it as it is and transform" \
                " it to a list and jsonfy it."
    
    genai.configure(api_key="AIzaSyBpT6qJ1A28dh2XQDnmSiNL4hIl-P94jFU")
    model = genai.GenerativeModel("gemini-1.5-flash")
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    response = model.generate_content(prompt)

    # client = genai.Client(api_key="AIzaSyBpT6qJ1A28dh2XQDnmSiNL4hIl-P94jFU")
    # response = client.models.generate_content(
    #     model="gemini-2.0-flash",
    #     contents=prompt,
    # )

    # print(response.to_json_dict())
    text = response.text[8:-4].replace("'", '"')
    data = json.loads(text)
    # Print the result
    print(data)
    return data


################## db functions ####################
from decimal import Decimal
import boto3
from botocore.exceptions import ClientError

def add_record_to_table(u_id, iso_date, test_name, attributes, table_name="Bellytag", region='eu-central-1'):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    if not test_name or not attributes:
        return "Not valid test name or attributes!"

    # Function to recursively convert float values in the attributes to Decimal
    def convert_to_decimal(obj):
        if isinstance(obj, dict):
            return {k: convert_to_decimal(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_decimal(v) for v in obj]
        elif isinstance(obj, float):
            return Decimal(str(obj))  # Convert float to Decimal
        return obj

    # Convert all float values in the attributes to Decimal
    attributes = convert_to_decimal(attributes)

    try:
        # Check if the u_id and iso_date combination exists
        response = table.get_item(
            Key={'u_id': u_id, 'date': iso_date}
        )

        if 'Item' in response:
            # u_id and iso_date combination exists, update the existing record
            update_expression = "SET test_name = :test_name, attributes = :attributes"
            expression_attribute_values = {":test_name": test_name, ":attributes": attributes}
        else:
            # u_id and iso_date combination does not exist, create a new record with the test name and attributes
            update_expression = "SET test_name = :test_name, attributes = :attributes"
            expression_attribute_values = {":test_name": test_name, ":attributes": attributes}

        # Perform the update operation
        table.update_item(
            Key={'u_id': u_id, 'date': iso_date},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        print(response)

    except ClientError as e:
        return f"Error: {e.response['Error']['Message']}"



def get_tests_by_name(u_id, test_name, table_name="Bellytag", region='eu-central-1'):
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression=Key('u_id').eq(u_id) & Attr('test_name').eq(test_name)
    )

    return response['Items'] if response['Items'] else None



def delete_record_from_table(name, category, table_name="Bellytag", region='eu-central-1'):
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)

    response = table.delete_item(
        Key={
            'Name': name.lower(),
            'Category': category
        },
        ReturnValues="ALL_OLD"
    )


    if 'Attributes' in response:
        return "Recipe was deleted!"

    return "Recipe does not exist!"


# Generate a unique ID using user_id and password
def generate_unique_id(user_id, password):
    # Generate a random salt
    salt = os.urandom(16)  # 16-byte random salt

    # Combine the user ID, password, and salt
    combined = f"{user_id}{password}".encode('utf-8') + salt

    # Hash the combined input with SHA-256
    hash_object = hashlib.sha256(combined)

    # Get the first 10 characters of the hexadecimal hash
    unique_id = hash_object.hexdigest()[:10]
    
    return unique_id


# Registration Route
@app.route('/register', methods=['POST'])
def insert_to_csv():

    if request.method == 'POST':
        data = request.get_json()
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        user_id = data.get('id')
        password = data.get('password')

        # Hash the password before storing it
        password_hash = hash_password(password)

        # Generate unique user ID
        u_id = generate_unique_id(user_id, password)

        mail = data.get('email')
        age = data.get('age')
        gender = data.get('gender')
        status = data.get('status')
        date_of_birth = data.get('dob')
        children = data.get('children')
        license = data.get('license')
        last_period = data.get('lastPeriod')

        if license is None:
            license = 0
        else:
            last_period = None


        # Save user data in CSV
        with open(r"BellyTagBackend\DB\patients.csv", mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([u_id, password_hash, f"{firstName} {lastName}", mail, age, gender, status, children, date_of_birth, last_period, license])

        path = r"C:\Users\sapir\Documents\\" + u_id
        if not os.path.exists(path):
            os.makedirs(path)
        


        return {
            "barcode": u_id,
            }, 201


# Login Route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        u_id = data.get('barcode')
        password = data.get('password')

        # Hash the entered password (same method used during registration)
        hashed_input_password = hash_password(password)

        # Search for the user in the CSV file
        with open(r"BellyTagBackend\DB\patients.csv", mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['u_id'] == u_id:
                    stored_hash = row['password'].strip()

                    # Compare hashed passwords
                    if hashed_input_password == stored_hash:
                        license = row.get('license')
                        if license == "0":
                            return {'role': "patient"}, 200
                        return {'role': "doctor"}, 200
                    else:
                        return "Incorrect password", 401

        return "User not found", 404
    

# Personal data route - retrieves user information by u_id
@app.route('/personal', methods=['GET'])
def get_personal_data():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({"error": "Barcode is missing"}), 400

    with open(r"BellyTagBackend\DB\patients.csv", mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['u_id'] == barcode:
                # Get last period date and calculate pregnancy week
                last_period_str = row.get('last_period', '')  # Fetch date as string
                pregnancy_week = 0  # Default value

                if last_period_str:  # If the date exists
                    try:
                        last_period_date = datetime.datetime.strptime(last_period_str, "%Y-%m-%d").date()
                        current_date = datetime.date.today()
                        days_since_last_period = (current_date - last_period_date).days
                        pregnancy_week = max(0, days_since_last_period // 7)  # Ensure non-negative
                    except ValueError:
                        print(f"Invalid date format: {last_period_str}")

                return jsonify({
                    "Name": row.get('name', 'Unknown'),
                    "Age": row.get('age', 'N/A'),
                    "Email": row.get('mail', ''),
                    "Gender": row.get('gender', ''),
                    "Status": row.get('status', '') + (" + " + row.get('children') if row.get('children') else ''),
                    "DoB": row.get('date', ''),  
                    "PregnancyWeek": pregnancy_week,  # Calculated dynamically
                    "LastPeriodDate": last_period_str,
                }), 200

    return jsonify({"error": "User not found"}), 404


# Function to check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_updated_file(dir_path, test_name):
    files = [
        f for f in os.listdir(dir_path)
        if f.startswith(test_name) and f.split('.')[-1] in ALLOWED_EXTENSIONS
    ]

    if not files:
        return None  # No matching files found

    # Use max() to get the most updated file based on filename sorting
    return max(files)

@app.route('/file', methods=['POST'])
def file():

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            barcode = request.form.get('barcode')
            file_name = request.form.get('newFileName')
            test_name = request.form.get('testName')

            # Create the directory for the user based on their barcode if it doesn't exist
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], barcode)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            # Save the file in the appropriate directory with the new file name
            file_path = os.path.join(user_folder, secure_filename(file_name))
            file.save(file_path)

            # Process the file (e.g., extract attributes) and save to the database
            # You can add your logic for processing the file here

            file = get_updated_file(os.path.join(app.config['UPLOAD_FOLDER'], barcode), test_name)
            # if file:
                
            res = file_to_attributes(file_path, test_name)
            pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)'
            match = re.search(pattern, file_name)
            iso_date = match.group(0)
            add_record_to_table(barcode, iso_date, test_name, res)


            return jsonify({"message": "File uploaded successfully!", "file_path": file_path}), 201
        else:
            return jsonify({"error": "Invalid file type"}), 400
    

@app.route('/test', methods=['GET'])
def get_test():
    if request.method == 'GET':
        barcode = request.args.get('barcode')
        test_name = request.args.get('testName')

        print(barcode, test_name)

        tests = get_tests_by_name(barcode, test_name)

        if not barcode or not test_name or not tests:
            return jsonify({"error": "Barcode, test name are required"}), 400


        return tests, 200

def patient_exists(barcode):
    """Check if the patient barcode exists in patients.csv"""
    file_path = os.path.join("BellyTagBackend", "DB", "patients.csv")

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                if row.get("u_id") == barcode:
                    return True
        return False
    except FileNotFoundError:
        return False

@app.route("/check_patient", methods=["POST"])
def check_patient():
    data = request.json
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400

    if patient_exists(barcode):
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False}), 404


if __name__ == '__main__':
    app.run(debug=True)