from flask import Flask, render_template, redirect, url_for, request, flash
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto3
import csv
import os
import bcrypt
import hashlib

# Initialize the app
app = Flask(__name__)

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
        user_id = data.get('id')
        password = data.get('password')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Generate unique user ID
        u_id, _ = generate_unique_id(user_id, password)

        mail = data.get('mail')
        age = data.get('age')
        gender = data.get('gender')
        status = data.get('status')
        date_of_birth = data.get('date_of_birth')

        # Save user data along with the unique ID in CSV
        with open('patients.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([u_id, user_id, password_hash, mail, age, gender, status, date_of_birth])
        print(u_id)

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
                        return "Login successful", 200
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
