import os
import csv
import hashlib

CSV_FILE = r"BellyTagBackend\DB\patients.csv"

print(f"DEBUG: CSV File Path: {os.path.exists(CSV_FILE)}")
# Ensure correct CSV headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['u_id', 'password', 'name', 'mail', 'age', 'gender', 'status', 'children', 'date', 'license'])
        file.flush()

def generate_unique_id(user_id, password):
    """Generate a unique ID for a user using SHA-256."""
    salt = os.urandom(16)
    combined = f"{user_id}{password}".encode('utf-8') + salt
    hash_object = hashlib.sha256(combined)
    return hash_object.hexdigest()

def register_user(user_data):
    """Register a user and save to patients.csv."""
    user_id = user_data['id']
    password = user_data['password']  # Store plain password

    u_id = generate_unique_id(user_id, password)
    
    print(f"\nDEBUG: Writing to {CSV_FILE}: {u_id}, {password}, {user_id}")
    
    try:
        with open(CSV_FILE, mode="a", newline="") as file:
            file.write("\n")
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow([
                u_id, password, user_data['name'], user_data['mail'], user_data['age'],
                user_data['gender'], user_data['status'], user_data['children'],
                user_data['date'], user_data['license']
            ])
        print(f"SUCCESS: User '{user_id}' registered with UID: {u_id}")
    except Exception as e:
        print(f"ERROR: Could not write to CSV - {e}")
    
    return u_id

def check_user_in_csv():
    """Check and display all users in the CSV file."""
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def login_user(u_id, password):
    """Check if a user can log in."""
    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['u_id'] == u_id:
                stored_password = row['password'].strip()
                print(f"DEBUG: Stored Password: {stored_password}")
                if password == stored_password:
                    print(f"Login successful for user ID: {u_id}")
                    return True
                else:
                    print("Incorrect password.")
                    return False
        print("User not found.")
        return False

def get_personal_data(u_id):
    """Retrieve personal data of a registered user."""
    with open(CSV_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        print(f"CSV Headers: {reader.fieldnames}")
        for row in reader:
            if row['u_id'] == u_id:
                print("User Found!")
                print(f"Name: {row['name']}")
                print(f"Email: {row['mail']}")
                print(f"Age: {row['age']}")
                print(f"Gender: {row['gender']}")
                print(f"Status: {row['status']}")
                print(f"Children: {row['children']}")
                print(f"Date: {row['date']}")
                print(f"License: {row['license']}")
                return row
    print("User not found.")
    return None

# ================================
# Run the testing flow
# ================================
print("\n===== Registering 4 Users =====")
test_users = [
    {'id': 'user1', 'password': 'pass1', 'name': 'Alice', 'mail': 'user1@example.com', 'age': '25', 'gender': 'Male', 'status': 'Single', 'children': '0', 'date': '1999-01-01', 'license': '2'},
    {'id': 'user2', 'password': 'pass2', 'name': 'Bob', 'mail': 'user2@example.com', 'age': '30', 'gender': 'Female', 'status': 'Married', 'children': '2', 'date': '1994-05-15', 'license': '1'},
    {'id': 'user3', 'password': 'pass3', 'name': 'Charlie', 'mail': 'user3@example.com', 'age': '28', 'gender': 'Other', 'status': 'Divorced', 'children': '1', 'date': '1996-07-22', 'license': '0'},
    {'id': 'user4', 'password': 'pass4', 'name': 'Diana', 'mail': 'user4@example.com', 'age': '22', 'gender': 'Male', 'status': 'Single', 'children': '0', 'date': '2002-10-10', 'license': '4'}
]

user_ids = [register_user(user) for user in test_users]

print("\n===== Checking Users in CSV =====")
check_user_in_csv()

print("\n===== Testing Login Functionality =====")
for i, u_id in enumerate(user_ids):
    print(f"\nLogging in user {i+1} with correct password:")
    login_user(u_id, f'pass{i+1}')
    print(f"\nLogging in user {i+1} with incorrect password:")
    login_user(u_id, 'wrongpassword')

print("\n===== Testing Non-Existent User Login =====")
login_user('fake_user_id', 'randompass')

print("\n===== Testing Retrieving Personal Data =====")
for u_id in user_ids:
    print("\nRetrieving data for a registered user:")
    get_personal_data(u_id)

print("\n===== Testing Retrieving Non-Existent User Data =====")
get_personal_data('fake_user_id')
