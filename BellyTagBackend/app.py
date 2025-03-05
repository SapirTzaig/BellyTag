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
from google import genai
import os
import pytesseract
from PIL import Image

# Initialize the app
app = Flask(__name__)

### file functions
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

        return "Record was added or updated!"

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

    return unique_id, salt

# Registration route - generates unique user ID and stores the data
@app.route('/register', methods=['POST'])
def insert_to_csv():

    if request.method == 'POST':
        data = request.get_json()
        fisrtName = data.get('firstName')
        lastName = data.get('lastName')
        user_id = data.get('id')
        password = data.get('password')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Generate unique user ID
        u_id, _ = generate_unique_id(user_id, password)

        mail = data.get('email')
        age = data.get('age')
        gender = data.get('gender')
        status = data.get('status')
        date_of_birth = data.get('dob')
        children = data.get('children')
        license = data.get('license')
        if license == None:
            license = 0

        # Save user data along with the unique ID in CSV
        with open('patients.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([u_id, password_hash, fisrtName + " " + lastName, mail, age, gender, status, children, date_of_birth, license])

        return u_id, 201


# Login route - verifies user ID and password
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        u_id = data.get('u_id')
        password = data.get('password')

        # Search for the user in the CSV file
        with open('patients.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['u_id'] == u_id:
                    # Verify the password using bcrypt
                    if bcrypt.checkpw(password.encode('utf-8'), row['password'].encode('utf-8')):
                        license = row.get('license')
                        if license == 0:
                            return "Doctor", 200
                        
                        return "Patient", 200
                    else:
                        return "Incorrect password", 401
            
            return "User not found", 404


# Personal data route - retrieves user information by u_id
@app.route('/personal', methods=['GET'])
def get_personal_data():
    if request.method == 'GET':
        data = request.get_json()
        u_id = data.get('u_id')

        with open('patients.csv', mode='r') as file:
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


if __name__ == '__main__':
    app.run(debug=True)
