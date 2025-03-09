from google import genai
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

    pdf_text = text.replace("\n", " ")
    pdf_text += "\n\nI want you to get from the text the following parameters and their values " \
                "(the desired type is provided) and the metric (mm/cm/bpm etc...). " \
                "If something doesn't exist, put None instead:\n"

    for key, value, high, low, unit in kvp:
        pdf_text += f"name: {key} value: {value} min: {low} max: {high} unit: {unit}\n"

    pdf_text += "I want only the parameters, values of the parameters, high values and low values with the ones" \
                " I gave you, and the metric, no * or bullet points or the opening line, i want a list of the" \
                " example of the format I want: [{ 'name': 'Hemoglobin', 'value': 11, 'min': 12, 'max': 16, 'unit': 'MoM' },...]" \
                "you should return it to me as a Text (not json), and I want to be able to take it as it is and transform" \
                " it to a list and jsonfy it."

    client = genai.Client(api_key="AIzaSyBpT6qJ1A28dh2XQDnmSiNL4hIl-P94jFU")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=pdf_text,
    )

    # print(response.to_json_dict())
    text = response.text[8:-4].replace("'", '"')
    data = json.loads(text)
    # Print the result

    return data




if __name__ == "__main__":
    dir_path = r'C:\Users\galev\OneDrive\Desktop'
    test_name = "Ultrasound-for-Fetal-Nuchal-Translucency"
    file_to_text()

    # latest = get_updated_file(dir_path, test_name)
    # print(latest)

