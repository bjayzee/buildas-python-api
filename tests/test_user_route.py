from fastapi.testclient import TestClient
from app import app
from faker import Faker

fake = Faker()
client = TestClient(app)

def test_register():
    """Test user registration"""
    signup_data = {
        "username": fake.user_name(),
        "name": fake.name(),
        "email": fake.email(),
        "password": "password1"
    }

    response = client.post("/users/register", json=signup_data)
    assert response.status_code == 200

    json_response = response.json()
    assert json_response["message"] == "Registration is successful"
    assert json_response["success"] is True

def get_user_data():
    """Helper function to register a user and return user login details."""
    password = "password1"  # Define a fixed password
    user_data = {
        "username": fake.user_name(),
        "name": fake.name(),
        "email": fake.email(),
        "password": password  # Include the password here
    }

    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200

    # Return user data including the password
    return {
        "id": response.json()["data"]["id"],
        "email": user_data["email"],  # Return the email for login
        "password": password  # Return the same password for login
    }



def test_login():
    login_data = get_user_data()  # Get registered user login details

    response = client.post("/users/login", json=login_data)

    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

def get_user_data():
    """Helper function to register a user and return user login details."""
    password = "password1"
    user_data = {
        "username": fake.user_name(),
        "name": fake.name(),
        "email": fake.email(),
        "password": password
    }

    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200
    
    # Print the user data to debug
    print("Registered user data:", response.json()) 

    return {
        "id": response.json()["data"]["id"],  # Ensure this matches your model
        "email": user_data["email"],
        "password": password
    }

def test_get_user():
    user_data = get_user_data()  # Register and get user data
    
    # Fetch the user by ID
    response = client.get(f"/users/{user_data['id']}")
    assert response.status_code == 200
    assert response.json()["data"]["email"] == user_data["email"]
    assert response.json()["message"] == "User fetched successfully"

def test_delete_user():
    user_data = get_user_data()  # Register and get user data
    
    # Delete the user by ID
    response = client.delete(f"/users/{user_data['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

    # Try to get the deleted user (should return 404)
    response = client.get(f"/users/{user_data['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"



