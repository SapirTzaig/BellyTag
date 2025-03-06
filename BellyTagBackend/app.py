from flask import Flask, render_template, redirect, url_for, request, flash
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
import genai
import os
import pytesseract
from PIL import Image
from flask_cors import CORS



# Initialize the app
app = Flask(__name__)

CORS(app)

### file functions

prenatal_tests = {
        "Ultrasound for Fetal Nuchal Translucency": [
            ("Nuchal Translucency", "float"),
            ("Crown Rump Length", "float"),
            ("Fetal Heart Rate", "float"),
            ("Biparietal diameter", "float"),
        ],
        "Ultrasound for Fetal Nasal Bone Determination": [
            ("Nasal Bone Visible", "boolean")
        ],
        "Maternal Serum (Blood) Tests": [
            ("Pregnancy Associated Plasma Protein A", "float"),
            ("Human Chorionic Gonadotropin", "float")
        ],
        "Genetic Screening Recommendation": [
            ("Genetic Counseling Recommended", "boolean"),
            ("Additional Testing Needed", "boolean"),
            ("Additional Tests", "list")
        ],
        "Multiple Marker Blood Tests (Second Trimester)": [
            ("AFP Screening", "float"),
            ("Estriol", "float"),
            ("Inhibin", "float"),
            ("Human Chorionic Gonadotropin", "float")
        ],
        "Possible Abnormal Indications": [
            ("Abnormal AFP", "boolean"),
            ("Miscalculated Due Date", "boolean"),
            ("Fetal Abdominal Wall Defects", "boolean"),
            ("Chromosomal Abnormalities", "boolean"),
            ("Open Neural Tube Defects", "boolean"),
            ("Multiple Fetuses Detected", "boolean")
        ],
        "Follow-up Testing": [
            ("Ultrasound Recommended", "boolean"),
            ("Amniocentesis Needed", "boolean")
        ],
        "Screening Accuracy": [
            ("False Positive Risk", "float"),
            ("False Negative Risk", "float")
        ],
        "Group B Streptococcus Presence": [
            ("Result", "boolean")
        ]
    }


# Simple hashing function using SHA-256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def pdf_to_text(pdf_path):
    text = ""

    # Try extracting text using PyPDF2
    try:
        with open(pdf_path, "rb") as file:
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
            with pdfplumber.open(pdf_path) as pdf:
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
            text = extract_text(pdf_path)
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
        text = pdf_to_text(file_path)
    elif file_path[-3:] == "png" or file_path[-3:] == "jpg" or file_path[-4:] == "jpeg":
        text = image_to_text(file_path)
    
    
    kvp = prenatal_tests[prenatal_test]


    # Extract text
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    

    pdf_text = pdf_text.replace("\n", " ")
    pdf_text += "\n\nI want you to get from the text the following parameters and their values " \
                "(the desired type is provided) and the metric (mm/cm/bpm etc...). " \
                "If something doesn't exist, put None instead:\n"

    for key, value in kvp:
        pdf_text += f"{key} : {value}\n"

    pdf_text += "I want only the parameters, values of the parameters, and the metric, " \
                "no * or bullet points or the opening line\n"

    client = genai.Client(api_key="AIzaSyBpT6qJ1A28dh2XQDnmSiNL4hIl-P94jFU")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=pdf_text,
    )

    print(response.to_json_dict())
    return response.to_json_dict()



# def text_to_attributes(text):


### db functions
def add_record_to_table(u_id, test, attributes, table_name="Prenatal_Tests", region='us-east-2'):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    if not test or not attributes:
        return "Not valid test or attributes!"

    try:
        # Check if the u_id exists
        response = table.get_item(
            Key={'u_id': u_id}
        )

        if 'Item' in response:
            # u_id exists, update the Tests hashmap
            update_expression = "SET Tests.#test = :attributes"
            expression_attribute_names = {"#test": test}
            expression_attribute_values = {":attributes": attributes}
        else:
            # u_id does not exist, create a new item
            update_expression = "SET Tests = :tests"
            expression_attribute_names = {}
            expression_attribute_values = {":tests": {test: attributes}}

        table.update_item(
            Key={'u_id': u_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )


    except ClientError as e:
        return f"Error: {e.response['Error']['Message']}"


def delete_record_from_table(name, category, table_name="Prenatal_Tests", region='us-east-2'):
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


def get_recipe(name, table_name="Prenatal_Tests", region='us-east-2'):
    dynamodb = boto3.resource("dynamodb", region_name=region)
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=Key('Name').eq(name)
    )

    return response['Items'][0] if len(response['Items']) > 0 in response else None


# Generate a unique ID using user_id and password
def generate_unique_id(user_id, password):
    # Generate a random salt
    salt = os.urandom(16)  # 16-byte random salt

    # Combine the user ID, password, and salt
    combined = f"{user_id}{password}".encode('utf-8') + salt

    # Hash the combined input with SHA-256
    hash_object = hashlib.sha256(combined)
    
    # Get the hexadecimal representation of the hash
    unique_id = hash_object.hexdigest()

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
            "path": path
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
    if request.method == 'GET':
        data = request.get_json()
        u_id = data.get('u_id')

        with open(r"BellyTagBackend\DB\patients.csv", mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['u_id'] == u_id:
                    return {
                        "name": row.get('name'),
                        "mail": row.get('mail'),
                        "age": row.get('age'),
                        "gender": row.get('gender'),
                        "status": row.get('status'),
                        "date": row.get('date_of_birth')
                    }, 200

            return "User not found", 404


@app.route('/file', methods=['POST'])
def file_to_attributes():
    if request.method == 'POST':
        data = request.get_json()
        u_id = data.get('u_id')
        test = data.get('test')
        file_path = data.get('file_path')

        attributes = file_to_attributes(file_path, test)
        add_record_to_table(u_id, test, attributes)
        return attributes, 201




if __name__ == '__main__':
    app.run(debug=True)