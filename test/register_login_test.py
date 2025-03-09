import os
import csv
import hashlib

# Define the path for the test CSV file
TEST_CSV_FILE = r"C:\Users\User\Documents\GitHub\BellyTag\test\test_patients.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(TEST_CSV_FILE), exist_ok=True)

# Define CSV headers
CSV_HEADERS = ['id', 'firstName', 'lastName', 'dob', 'age', 'gender', 'status', 'children', 'email', 'password', 'role', 'license', 'lastPeriod']

# Ensure headers are written in the CSV file
if not os.path.exists(TEST_CSV_FILE):
    with open(TEST_CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)

def generate_unique_id(user_id, password):
    """Generate a unique hashed ID using SHA-256."""
    combined = f"{user_id}{password}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()

def register_user(user_data):
    """Register a user with validation."""
    try:
        # Validate role
        if user_data['role'] not in ['Doctor', 'Patient']:
            print(f"ERROR: Invalid role '{user_data['role']}' for user {user_data['firstName']}. Role must be 'Doctor' or 'Patient'.")
            return None

        # Patients must have lastPeriod, but doctors should NOT have it
        if user_data['role'] == 'Patient' and not user_data.get('lastPeriod'):
            print(f"ERROR: Patient {user_data['firstName']} must provide 'lastPeriod'.")
            return None
        if user_data['role'] == 'Doctor' and 'lastPeriod' in user_data and user_data['lastPeriod']:
            print(f"ERROR: Doctor {user_data['firstName']} should not have 'lastPeriod'.")
            return None

        # Generate hashed ID
        u_id = generate_unique_id(user_data['id'], user_data['password'])
        
        print(f"\nDEBUG: Writing to {TEST_CSV_FILE}: Hashed ID: {u_id}, User: {user_data['firstName']}")

        with open(TEST_CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow([
                u_id, user_data['firstName'], user_data['lastName'], user_data['dob'],
                user_data['age'], user_data['gender'], user_data['status'],
                user_data.get('children', ''), user_data['email'], user_data['password'],
                user_data['role'], user_data.get('license', ''), user_data.get('lastPeriod', '')
            ])
        
        print(f"SUCCESS: User '{user_data['firstName']}' registered with UID: {u_id}")
        return u_id  

    except KeyError as e:
        print(f"ERROR: Missing required field: {e}")
        return None

def check_user_in_csv():
    """Check and display all users in the test CSV file."""
    with open(TEST_CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def login_user(user_id, password):
    """Check if a user can log in using hashed ID lookup."""
    hashed_id = generate_unique_id(user_id, password)

    with open(TEST_CSV_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == hashed_id:
                print(f"DEBUG: User {row['firstName']} found!")
                if row['password'].strip() == password:
                    print(f"Login successful for user: {row['firstName']}")
                    return True
                else:
                    print("Incorrect password.")
                    return False

        print("User not found.")
        return False

# ================================
# Run the testing flow with failed cases
# ================================
print("\n===== Registering Users (Including Failed Cases) =====")

test_users = [
    # ✅ Valid Doctor
    {'id': 'doc1', 'password': 'pass1', 'firstName': 'Alice', 'lastName': 'Smith', 'email': 'alice@example.com', 'age': '40', 'gender': 'Female', 'status': 'Married', 'children': '2', 'dob': '1984-05-10', 'role': 'Doctor', 'license': '12345'},

    # ✅ Valid Patient
    {'id': 'pat1', 'password': 'pass2', 'firstName': 'Bob', 'lastName': 'Johnson', 'email': 'bob@example.com', 'age': '30', 'gender': 'Male', 'status': 'Single', 'children': '0', 'dob': '1994-02-25', 'role': 'Patient', 'lastPeriod': '2024-01-15'},

    # ❌ Invalid Role
    {'id': 'usr1', 'password': 'pass3', 'firstName': 'Charlie', 'lastName': 'Brown', 'email': 'charlie@example.com', 'age': '28', 'gender': 'Other', 'status': 'Divorced', 'children': '1', 'dob': '1996-07-22', 'role': 'Nurse'},

    # ❌ Patient without lastPeriod
    {'id': 'pat2', 'password': 'pass4', 'firstName': 'Diana', 'lastName': 'Evans', 'email': 'diana@example.com', 'age': '22', 'gender': 'Female', 'status': 'Single', 'children': '0', 'dob': '2002-10-10', 'role': 'Patient'},

    # ❌ Doctor with lastPeriod
    {'id': 'doc2', 'password': 'pass5', 'firstName': 'Eve', 'lastName': 'Adams', 'email': 'eve@example.com', 'age': '50', 'gender': 'Female', 'status': 'Married', 'children': '3', 'dob': '1974-03-05', 'role': 'Doctor', 'license': '67890', 'lastPeriod': '2023-12-01'},
]

user_ids = [register_user(user) for user in test_users]

print("\n===== Checking Users in CSV =====")
check_user_in_csv()

print("\n===== Testing Login Functionality =====")
for user in test_users:
    plain_id = user['id']
    correct_password = user['password']
    wrong_password = "wrongpassword"

    print(f"\nLogging in {plain_id} with correct password:")
    login_user(plain_id, correct_password)

    print(f"\nLogging in {plain_id} with incorrect password:")
    login_user(plain_id, wrong_password)

print("\n===== Testing Non-Existent User Login =====")
login_user('fake_user_id', 'randompass')

print(f"\nTest file created at: {TEST_CSV_FILE}")
