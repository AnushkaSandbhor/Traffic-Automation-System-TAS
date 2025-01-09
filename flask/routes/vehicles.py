from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response
 
# Create a Blueprint for vehicle-related routes
vehicles_bp = Blueprint('vehicles', __name__)
 
# Route to register a new vehicle
@vehicles_bp.route('/register', methods=['POST'])
def register_vehicle():
    """
    Endpoint to register a new vehicle.
    Requires vehicle number, owner name, and vehicle type in the request body.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        return validation_result
 
    # Extract data from the request body
    data = request.json
    vehicle_number = data.get('vehicle_number')
    owner_name = data.get('owner_name')
    vehicle_type = data.get('vehicle_type')
 
    # Validate that all required fields are provided
    if not vehicle_number or not owner_name or not vehicle_type:
        return jsonify({'message': 'vehicle_number, owner_name, and vehicle_type are required'}), 400
 
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Insert the new vehicle into the database
        query = "INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type) VALUES (%s, %s, %s);"
        cursor.execute(query, (vehicle_number, owner_name, vehicle_type))
        conn.commit()
 
        # Get the ID of the newly registered vehicle
        vehicle_id = cursor.lastrowid
        return jsonify({
            "message": "Vehicle registered successfully",
            "vehicle_id": vehicle_id
        }), 201
 
    except Exception as err:
        # Return a database error if an exception occurs
        return jsonify({
            "status": 500,
            "message": "Database error",
            "error": str(err)
        }), 500
 
    finally:
        # Ensure the database connection is properly closed
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
 
# Route to fetch the details of a specific vehicle by its ID
@vehicles_bp.route('/<string:vehicle_id>', methods=['GET'])
def get_vehicle_details(vehicle_id):
    """
    Endpoint to fetch the details of a specific vehicle based on its ID.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        return validation_result
 
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Query to fetch vehicle details by vehicle_id
        query = "SELECT * FROM vehicles WHERE vehicle_id = %s;"
        cursor.execute(query, (vehicle_id,))
        vehicle = cursor.fetchone()
 
        # Check if the vehicle exists
        if vehicle:
            return jsonify({
                "vehicle_id":vehicle['vehicle_id'],
                "vehicle_number":vehicle['vehicle_number'],
                "owner_name":vehicle['owner_name'],
                "vehicle_type":vehicle['vehicle_type']
                }), 200
        else:
            # Return error if vehicle with the given ID is not found
            return jsonify({
                "status": 404,
                "message": "Vehicle not found"
            }), 404
 
    except Exception as err:
        # Return a database error if an exception occurs
        return jsonify({
            "status": 500,
            "message": "Database error",
            "error": str(err)
        }), 500
 
    finally:
        # Ensure the database connection is properly closed
        if conn and conn.is_connected():
            cursor.close()
            conn.close()