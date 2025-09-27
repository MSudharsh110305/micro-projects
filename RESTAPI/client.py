import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("=== Testing Flask RESTful API ===\n")
    
    # Test GET all users (should be empty initially)
    print("1. Getting all users:")
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Status: {response.status_code}")
    print(f"Data: {response.json()}\n")
    
    # Test POST - Create users
    print("2. Creating users:")
    users_to_create = [
        {"name": "Alice", "email": "alice@example.com", "age": 25},
        {"name": "Bob", "email": "bob@example.com", "age": 30},
        {"name": "Charlie", "email": "charlie@example.com", "age": 28}
    ]
    
    for user_data in users_to_create:
        response = requests.post(f"{BASE_URL}/api/users", json=user_data)
        print(f"Created {user_data['name']} - Status: {response.status_code}")
    
    # Test GET all users again
    print("\n3. Getting all users after creation:")
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Status: {response.status_code}")
    print(f"Data: {json.dumps(response.json(), indent=2)}\n")
    
    # Test GET single user
    print("4. Getting user with ID 1:")
    response = requests.get(f"{BASE_URL}/api/users/1")
    print(f"Status: {response.status_code}")
    print(f"Data: {json.dumps(response.json(), indent=2)}\n")
    
    # Test PUT - Update user
    print("5. Updating user with ID 1:")
    update_data = {"name": "Alice Updated", "email": "alice.updated@example.com", "age": 26}
    response = requests.put(f"{BASE_URL}/api/users/1", json=update_data)
    print(f"Status: {response.status_code}")
    print(f"Updated Data: {json.dumps(response.json(), indent=2)}\n")
    
    # Test DELETE user
    print("6. Deleting user with ID 2:")
    response = requests.delete(f"{BASE_URL}/api/users/2")
    print(f"Status: {response.status_code}")
    print(f"Remaining users: {json.dumps(response.json(), indent=2)}\n")
    
    # Test error handling - Get non-existent user
    print("7. Testing error handling - Get user with ID 999:")
    response = requests.get(f"{BASE_URL}/api/users/999")
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json()}\n")
    
    # Test validation - Missing required field
    print("8. Testing validation - Missing name field:")
    bad_data = {"email": "test@example.com", "age": 25}
    response = requests.post(f"{BASE_URL}/api/users", json=bad_data)
    print(f"Status: {response.status_code}")
    print(f"Error: {response.json()}")

if __name__ == '__main__':
    test_api()
