from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response
 
# Create a Blueprint for fines-related routes
fines_bp = Blueprint('fines', __name__)
 
# Route to mark a fine as paid and update the payment date
@fines_bp.route('/<int:fine_id>/pay', methods=['PUT'])
def update_fines(fine_id):
    """
    Endpoint to update the fine status to 'PAID' and record the payment date.
    The fine is updated based on the provided 'fine_id' and payment date.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the validation response
        return validation_result
   
    # Get the payment date from the request data
    data = request.json
    payment_date = data.get('payment_date')
 
    # Validate that payment_date is provided in the request
    if not payment_date:
        return jsonify({'message': 'Payment date field is required'}), 400
       
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Update the fine status to 'PAID' and set the payment date
        update_query = "UPDATE fines SET fine_status = 'PAID', payment_date = %s WHERE fine_id = %s;"
        cursor.execute(update_query, (payment_date, fine_id))
        conn.commit()
 
        # Check if the fine was successfully updated
        check_query = "SELECT * FROM fines WHERE fine_id = %s;"
        cursor.execute(check_query, (fine_id,))
        result = cursor.fetchone()
 
        # Return success response if the fine was found and updated
        if result:
            return jsonify({
                "message": "Fine paid successfully",
                "fine_status": "Paid"
            }), 201
        else:
            # If fine_id not found, return an error
            return jsonify({
                "status": 404,
                "message": "Fine ID not found"
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