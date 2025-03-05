from flask import Flask, render_template, redirect, url_for, request, flash
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto3

# Initialize the app
app = Flask(__name__)


@app.route('/alive', methods=['GET'])
def alive():
    return "Hey Sapir!", 200





if __name__ == '__main__':
    app.run(debug=True)



