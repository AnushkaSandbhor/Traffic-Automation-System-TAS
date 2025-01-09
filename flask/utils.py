import requests
from flask import request, jsonify
 
def validate_response():
    """
    Validates the Authorization token by making a request to the /validate endpoint.
    Returns:
        - 401 Unauthorized if token is missing or empty.
        - 403 Forbidden if token is invalid.
        - True if the token is valid.
    """
    # Retrieve the Authorization header from the request
    auth_header = request.headers.get("Authorization")
 
    # Check if the Authorization header is missing or empty
    if not auth_header or not auth_header.strip():
        return jsonify({
            "status": 401,
            "message": "Unauthorized: Authorization token is required"
        }), False
 
    # Split the Authorization header into its components (e.g., "Bearer <token>")
    parts = auth_header.split()
   
    # Validate the header format (should contain two parts)
    if len(parts) != 2 or not parts[1].strip(): #strip() remove spaces in the output
        return jsonify({
            "status": 401,
            "message": "Unauthorized: Authorization token cannot be empty"
        }), False
 
    # URL of the /validate endpoint to check token validity
    validate_url = "http://127.0.0.1:2999/auth/validate"
   
    # Set up headers with the Authorization token
    headers = {"Authorization": auth_header}
 
    try:
        # Make a POST request to the /validate endpoint with the token in headers
        response = requests.post(validate_url, headers=headers)
       
        # Check the response status code for validity
        if response.status_code == 200:
            return True
        else:
            return jsonify({
                "status": 403,
                "message": "Forbidden: Invalid Authorization token"
            }), False
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        return jsonify({
            "status": 500,
            "message": "Internal Server Error: Unable to validate token",
            "error": str(e)
        }), False