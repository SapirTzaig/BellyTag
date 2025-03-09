import requests

BASE_URL = "http://localhost:5000"  # Change this if your Flask app runs on a different port

# -----------------------------
# ✅ 1. Test User Registration
# -----------------------------
def test_register_doctor():
    """Test registering a valid doctor."""
    response = requests.post(f"{BASE_URL}/register", json={
        "firstName": "Alice",
        "lastName": "Smith",
        "id": "alice123",
        "password": "mypassword",
        "email": "alice@example.com",
        "age": "30",
        "gender": "Female",
        "status": "Married",
        "dob": "1993-05-20",
        "role": "Doctor",
        "license": "12345"
    })
    
    assert response.status_code == 201
    print("✅ test_register_doctor PASSED")

# ❌ Register a patient without lastPeriod (should fail)
def test_register_patient_without_last_period():
    response = requests.post(f"{BASE_URL}/register", json={
        "firstName": "Bob",
        "lastName": "Johnson",
        "id": "bob123",
        "password": "mypassword",
        "email": "bob@example.com",
        "age": "28",
        "gender": "Male",
        "status": "Single",
        "dob": "1995-08-10",
        "role": "Patient"
    })
    assert response.status_code == 400
    print("✅ test_register_patient_without_last_period PASSED")

# ❌ Register a doctor with lastPeriod (should fail)
def test_register_doctor_with_last_period():
    response = requests.post(f"{BASE_URL}/register", json={
        "firstName": "Charlie",
        "lastName": "Brown",
        "id": "charlie123",
        "password": "mypassword",
        "email": "charlie@example.com",
        "age": "45",
        "gender": "Male",
        "status": "Married",
        "dob": "1978-02-25",
        "role": "Doctor",
        "license": "67890",
        "lastPeriod": "2024-01-15"
    })
    assert response.status_code == 400
    print("✅ test_register_doctor_with_last_period PASSED")

# -----------------------------
# ✅ 2. Test User Login
# -----------------------------
def test_login_valid_user():
    """Test logging in after registering a user."""
    requests.post(f"{BASE_URL}/register", json={
        "firstName": "Diana",
        "lastName": "Evans",
        "id": "diana123",
        "password": "securepass",
        "email": "diana@example.com",
        "age": "33",
        "gender": "Female",
        "status": "Single",
        "dob": "1991-07-14",
        "role": "Doctor",
        "license": "55555"
    })

    response = requests.post(f"{BASE_URL}/login", json={
        "barcode": "diana123",  # Change this to the correct barcode if needed
        "password": "securepass"
    })
    assert response.status_code == 200
    print("✅ test_login_valid_user PASSED")

# ❌ Login with incorrect password
def test_login_invalid_password():
    response = requests.post(f"{BASE_URL}/login", json={
        "barcode": "diana123",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    print("✅ test_login_invalid_password PASSED")

# -----------------------------
# ✅ 3. Test Personal Data Retrieval
# -----------------------------
def test_get_personal_data():
    """Test retrieving personal data after registration."""
    requests.post(f"{BASE_URL}/register", json={
        "firstName": "Frank",
        "lastName": "Miller",
        "id": "frank123",
        "password": "testpass",
        "email": "frank@example.com",
        "age": "50",
        "gender": "Male",
        "status": "Married",
        "dob": "1973-09-18",
        "role": "Patient",
        "lastPeriod": "2024-03-01"
    })

    response = requests.get(f"{BASE_URL}/personal", params={"barcode": "frank123"})
    assert response.status_code == 200
    print("✅ test_get_personal_data PASSED")

# ❌ Retrieve personal data for a non-existent user
def test_get_nonexistent_user():
    response = requests.get(f"{BASE_URL}/personal", params={"barcode": "nonexistentbarcode"})
    assert response.status_code == 404
    print("✅ test_get_nonexistent_user PASSED")

# -----------------------------
# ✅ Run All Tests
# -----------------------------
if __name__ == "__main__":
    print("\nRunning API tests...\n")
    test_register_doctor()
    test_register_patient_without_last_period()
    test_register_doctor_with_last_period()
    test_login_valid_user()
    test_login_invalid_password()
    test_get_personal_data()
    test_get_nonexistent_user()
    print("\n✅ All tests completed successfully!")
