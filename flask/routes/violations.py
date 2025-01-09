from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response
 
# Create a Blueprint for violation-related routes
violations_bp = Blueprint('violations', __name__)
 
# Route to fetch the violation report by violation ID
@violations_bp.route('/<int:violation_id>', methods=['GET'])
def get_violation_report(violation_id):
    """
    Endpoint to fetch the violation details by violation_id.
    Requires a valid token and violation_id in the URL.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        return validation_result
 
    # Validate that violation_id is provided
    if not violation_id:
        return jsonify({'message': 'violation_id is required'}), 400
 
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Query to fetch violation details
        query = """
            SELECT v.violation_id, ve.vehicle_number, v.violation_type, v.fine_amount
            FROM violations v
            JOIN vehicles ve ON ve.vehicle_id = v.vehicle_id
            WHERE v.violation_id = %s;
        """
        cursor.execute(query, (violation_id,))
        data = cursor.fetchone()
 
        # Check if the violation exists
        if data:
            return jsonify(data), 200
        else:
            return jsonify({
                "status": 404,
                "message": "Violation not found"
            }), 404
 
    except Exception as err:
        # Handle any database errors
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
 
# Route to generate a new violation report
@violations_bp.route('/generate', methods=['POST'])
def generate_violation_report():
    """
    Endpoint to generate a new violation report.
    Requires vehicle_id, signal_id, violation_type, and fine_amount in the request body.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        return validation_result
 
    # Extract data from the request body
    data = request.json
    vehicle_id = data.get('vehicle_id')
    signal_id = data.get('signal_id')
    violation_type = data.get('violation_type')
    fine_amount = data.get('fine_amount')
 
    # Validate that all required fields are provided
    if not vehicle_id or not signal_id or not violation_type or not fine_amount:
        return jsonify({'message': 'Please insert all mandatory data'}), 400
 
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Insert the new violation into the database
        query = """
            INSERT INTO violations (vehicle_id, signal_id, violation_type, fine_amount)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (vehicle_id, signal_id, violation_type, fine_amount))
        conn.commit()
 
        # Fetch the most recently generated violation ID
        cursor.execute("SELECT LAST_INSERT_ID() AS violation_id;")
        result = cursor.fetchone()
 
        # Return the generated violation ID
        if result:
            return jsonify({
                "message": "Violation report generated",
                "violation_id": result['violation_id']
            }), 201
        else:
            return jsonify({
                "message": "Report generation unsuccessful"
            }), 404
 
    except Exception as err:
        # Handle any database errors
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