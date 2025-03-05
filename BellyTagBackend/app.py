from flask import Flask, render_template, redirect, url_for, request, flash
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto3
import csv
import os
import bcrypt
import json

# Initialize the app
app = Flask(__name__)


@app.route('/alive', methods=['GET'])
def alive():
    return "Hey Sapir!", 200


@app.route('/register', methods=['GET','POST'])
def insert_to_csv():
    if request.method == 'GET':
        return
    
    elif request.method == 'POST':
        data = request.get_json()
        u_id = data.get('u_id')
        password = data.get('password')
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt)
        mail = data.get('mail')
        age = data.get('age')
        gender = data.get('gender')
        status = data.get('status')
        date_of_birth = data.get('date_of_birth')

        # Here you can add code to insert the data into a CSV file or a database
        # For example, you can use the csv module to write to a CSV file


        with open('patients.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([u_id, password, mail, age, gender, status, date_of_birth])

        return "User registered successfully", 201





if __name__ == '__main__':
    app.run(debug=True)



