from flask_jwt_extended import create_access_token
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app  
import pytest 
  
def test_signin_success(client):
    """Test the /signin route with valid email and password."""
    data = {
        "email_id": "rani@gmail.com",
        "password": "234"
    }
    response = client.post("/signin", json=data)
 
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.json}")
 
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
 
 
 
 
# Test for failed sign-in with invalid email
def test_signin_invalid_email(client):
    """Test the /signin route with an invalid email."""
    data = {
        "email_id": "invalid@example.com",
        "password": "validpassword"
    }
    response = client.post("/signin", json=data)
 
    # Check if the response status code is 401 (Unauthorized)
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["status"] == 401
    assert json_data["message"] == "failed"
    assert json_data["Error"] == "Access Denied"
 
# Test for failed sign-in with invalid password
def test_signin_invalid_password(client):
    """Test the /signin route with an invalid password."""
    data = {
        "email_id": "valid@example.com",
        "password": "invalidpassword"
    }
    response = client.post("/signin", json=data)
 
    # Check if the response status code is 401 (Unauthorized)
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["status"] == 401
    assert json_data["message"] == "failed"
    assert json_data["Error"] == "Access Denied"
 
# Test for sign-in with missing email
def test_signin_missing_email(client):
    """Test the /signin route with missing email."""
    data = {
        "password": "validpassword"
    }
    response = client.post("/signin", json=data)
 
    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["message"] == "Email_id and password are required"
 
# Test for sign-in with missing password
def test_signin_missing_password(client):
    """Test the /signin route with missing password."""
    data = {
        "email_id": "valid@example.com"
    }
    response = client.post("/signin", json=data)
 
    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["message"] == "Email_id and password are required"
 
 
 
 
 
# Fixture to generate a valid token for testing
@pytest.fixture()
def valid_token():
    """Generate a valid JWT token for testing."""
    with app.app_context():
        token = create_access_token(identity="valid@example.com")
    return token
 
# Fixture to simulate the sign-in process and return the token
@pytest.fixture()
def signin_data():
    """Simulate a successful sign-in and return the token."""
    client = app.test_client()
    data = {
        "email_id": "valid@example.com",
        "password": "validpassword"
    }
    response = client.post("/signin", json=data)
    return response.json['credentials']['token']  # Extract token from response
 
# Test for /validate route with a valid JWT token
def test_validate_success(client, valid_token):
    """Test the /validate route with a valid JWT token."""
    response = client.post(
        "/auth/validate",  # Use the correct URL with /auth prefix
        headers={"Authorization": f"Bearer {valid_token}"}
    )
 
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
 
    # Check if the response message is correct
    json_data = response.get_json()
    assert json_data["message"] == "success"
 
# Test for /validate route with no JWT token
def test_validate_missing_token(client):
    """Test the /validate route with no JWT token."""
    response = client.post("/auth/validate")  # Use the correct URL with /auth prefix
   
    # Check if the response status code is 401 (Unauthorized)
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["msg"] == "Missing Authorization Header"
 
# Test for /validate route with an invalid JWT token
def test_validate_invalid_token(client):
    """Test the /validate route with an invalid JWT token."""
    invalid_token = "invalid_token"
    response = client.post(
        "/auth/validate",  # Use the correct URL with /auth prefix
        headers={"Authorization": f"Bearer {invalid_token}"}
    )
   
    # Check if the response status code is 401 (Unauthorized)
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["msg"] == "Invalid token"  