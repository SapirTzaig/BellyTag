import requests

BASE_URL = "http://localhost:5000"

# -----------------------------
# ✅ Test User Registration
# -----------------------------
def test_register_doctor():
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
    
    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)
    
    assert response.status_code == 201
    print("✅ test_register_doctor PASSED")
    print(response.json()["barcode"])  # ✅ Print the barcode

    return response.json()["barcode"]  # ✅ Return the barcode


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

# -----------------------------
# ✅ Test User Login
# -----------------------------
def test_login_valid_user():
    """Test logging in with the correct barcode from registration."""
    barcode = test_register_doctor()  # ✅ Get correct barcode
    print("BARCODE:", barcode)

    response = requests.post(f"{BASE_URL}/login", json={
        "barcode": barcode,  # ✅ Use correct `id`
        "password": "mypassword"
    })

    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)
    
    assert response.status_code == 200
    print("✅ test_login_valid_user PASSED")



# ❌ Login with incorrect password
def test_login_invalid_password():
    response = requests.post(f"{BASE_URL}/login", json={
        "barcode": "9eaeeefa51",
        "password": "wrongpassword"
    })
    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)
    assert response.status_code == 401
    print("✅ test_login_invalid_password PASSED")

# -----------------------------
# ✅ Test Personal Data Retrieval
# -----------------------------
def test_get_personal_data():
    """Test retrieving personal data after registration."""
    barcode = "9eaeeefa51"  # ✅ Get the correct barcode

    response = requests.get(f"{BASE_URL}/personal", params={"barcode": barcode})
    
    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT:", response.text)
    
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
    test_register_patient_without_last_period()
    test_login_valid_user()
    test_login_invalid_password()
    test_get_personal_data()
    test_get_nonexistent_user()
    print("\n✅ All tests completed successfully!")
