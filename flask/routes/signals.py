from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response
 
# Create a Blueprint for signal-related routes
signals_bp = Blueprint('signals', __name__)
 
# Route to update the state of a specific traffic signal
@signals_bp.route('/<int:signal_id>/state', methods=['PUT'])
def update_signal(signal_id):
    """
    Endpoint to update the state of a specific traffic signal.
    The new state is provided in the request body.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the validation response
        return validation_result
   
    # Get the new signal state from the request data
    data = request.json
    signal_state = data.get('signal_state')
   
    # Validate that signal_state is provided
    if not signal_state:
        return jsonify({'message': 'Signal state is required'}), 400
 
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Query to update the signal state
        update_query = "UPDATE traffic_signals SET signal_state = %s WHERE signal_id = %s;"
        cursor.execute(update_query, (signal_state, signal_id))
        conn.commit()
       
        # Query to check the updated signal state
        check_query = "SELECT signal_state FROM traffic_signals WHERE signal_id = %s;"
        cursor.execute(check_query, (signal_id,))
        state = cursor.fetchone()
       
        # Check if the signal state was successfully updated
        if state:
            return jsonify({
                "message": "Traffic signal updated successfully",
                "signal_state": signal_state
            }), 200
        else:
            # If signal_id not found, return an error
            return jsonify({
                "status": 404,
                "message": "Signal ID not found"
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
 
# Route to delete a specific traffic signal
@signals_bp.route('/<int:signal_id>', methods=['DELETE'])
def delete_signal(signal_id):
    """
    Endpoint to delete a specific traffic signal based on its ID.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the validation response
        return validation_result
 
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Check if the signal_id exists in the database
        check_query = "SELECT signal_id FROM traffic_signals WHERE signal_id = %s;"
        cursor.execute(check_query, (signal_id,))
        data = cursor.fetchone()
       
        # If signal_id not found, return an error
        if not data:
            return jsonify({
                "status": 404,
                "message": "Signal ID not found"
            }), 404
       
        # Delete the traffic signal from the database
        delete_query = "DELETE FROM traffic_signals WHERE signal_id = %s;"
        cursor.execute(delete_query, (signal_id,))
        conn.commit()
       
        # Return success response after deletion
        return jsonify({
            "message": "Traffic signal deleted successfully"
        }), 200
 
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