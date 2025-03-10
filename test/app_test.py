from flask import Flask, request, jsonify
import csv
import os
import hashlib
from flask_cors import CORS

# Initialize the app
app = Flask(__name__)
CORS(app)

# Define the CSV file path
CSV_FILE = r"C:\Users\User\Documents\GitHub\BellyTag\test\test_patients.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

# Define correct CSV headers
CSV_HEADERS = ['id', 'password', 'firstName', 'lastName', 'email', 'age', 'gender', 
               'status', 'children', 'dob', 'lastPeriod', 'role', 'license']

# Ensure the CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)

# Simple password hashing function
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Generate a unique ID using user_id and password
def generate_unique_id(user_id, password):
    combined = f"{user_id}{password}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()[:10]  # Return a 10-character unique ID

# ✅ Registration API
@app.route('/register', methods=['POST'])
def insert_to_csv():
    data = request.get_json()

    first_name = data.get('firstName')
    last_name = data.get('lastName')
    user_id = data.get('id')
    password = data.get('password')
    email = data.get('email')
    age = data.get('age')
    gender = data.get('gender')
    status = data.get('status')
    dob = data.get('dob')
    role = data.get('role')
    license_number = data.get('license', '')
    last_period = data.get('lastPeriod', '')

    # Validate required fields
    if not all([first_name, last_name, user_id, password, email, age, gender, status, dob, role]):
        return jsonify({"error": "Missing required fields"}), 400

    if role not in ["Doctor", "Patient"]:
        return jsonify({"error": "Invalid role, must be 'Doctor' or 'Patient'"}), 400

    if role == "Doctor" and not license_number:
        return jsonify({"error": "Doctor must provide a license number"}), 400

    if role == "Patient" and not last_period:
        return jsonify({"error": "Patient must provide lastPeriod"}), 400

    # ✅ Hash the password before saving
    hashed_password = hash_password(password)

    # ✅ Generate a unique user ID
    unique_id = generate_unique_id(user_id, password)

    # ✅ Read existing users
    existing_users = set()
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_users.add(row['id'])  # ✅ Ensure no duplicate id

    if unique_id in existing_users:
        return jsonify({"error": "User already exists"}), 409

    # ✅ Write to CSV with correct structure
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([unique_id, first_name, last_name, dob, age, gender, 
                         status, "N/A" if role == "Doctor" else last_period, 
                         email, hashed_password, role, license_number, last_period])

    return jsonify({"barcode": unique_id}), 201



# ✅ Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('barcode')  # ✅ This is the unique `id` field
    password = data.get('password')

    if not user_id or not password:
        return jsonify({"error": "Barcode and password are required"}), 400

    hashed_input_password = hash_password(password)

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # ✅ Ensure the file has the correct headers
        if 'id' not in reader.fieldnames:
            return jsonify({"error": "CSV structure is incorrect"}), 500

        for row in reader:
            if row['id'] == user_id:  # ✅ Compare against `id`
                stored_hash = row['password'].strip()

                print(f"🔍 DEBUG: Stored hash: {stored_hash}, Input hash: {hashed_input_password}")

                if hashed_input_password == stored_hash:
                    return jsonify({"role": row['role']}), 200
                else:
                    print("❌ Password mismatch!")
                    return jsonify({"error": "Incorrect password"}), 401

    print("❌ User not found!")
    return jsonify({"error": "User not found"}), 404

# ✅ Personal Data API
@app.route('/personal', methods=['GET'])
def get_personal_data():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({"error": "Barcode is missing"}), 400

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == barcode:
                return jsonify({
                    "Name": f"{row['firstName']} {row['lastName']}",
                    "Age": row['age'],
                    "Email": row['email'],
                    "Gender": row['gender'],
                    "Status": row['status'],
                    "DoB": row['dob'],
                    "LastPeriodDate": row.get('lastPeriod', "N/A")
                }), 200

    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
