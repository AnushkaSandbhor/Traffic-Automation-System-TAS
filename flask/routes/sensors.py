from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils import validate_response
 
# Create a Blueprint for sensor-related routes
sensors_bp = Blueprint('sensors', __name__)
 
# Route to get data from a specific sensor
@sensors_bp.route('/<int:sensor_id>/data', methods=['GET'])
def sensor_data(sensor_id):
    """
    Endpoint to fetch data from a specific sensor based on the sensor ID.
    Returns the sensor's location, traffic count, average speed, and traffic condition.
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
 
        # Query to fetch sensor data based on the sensor ID
        query = "SELECT location, traffic_count, average_speed, traffic_condition FROM sensor_data WHERE sensor_id = %s;"
        cursor.execute(query, (sensor_id,))
        data = cursor.fetchone()
 
        # Return sensor data if found
        if data:
            return jsonify({
                "sensor_id": sensor_id,
                "location": data['location'],
                "traffic_count": data['traffic_count'],
                "average_speed": data['average_speed'],
                "traffic_condition": data['traffic_condition']
            }), 200
        else:
            # If sensor_id not found, return an error
            return jsonify({
                "status": 404,
                "message": "Sensor ID not found"
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
 
# Route to adjust traffic signals based on sensor data
@sensors_bp.route('/<int:sensor_id>/adjust', methods=['PUT'])
def adjust_signals(sensor_id):
    """
    Endpoint to adjust the traffic condition of a specific sensor.
    Accepts the new traffic condition as input and updates the sensor data.
    """
    # Validate the response (e.g., check if JWT token is valid)
    validation_result = validate_response()
    if validation_result is not True:
        # If token validation failed, return the validation response
        return validation_result
   
    # Get the new traffic condition from the request data
    data = request.json
    traffic_condition = data.get('traffic_condition')
 
    # Validate that traffic_condition is provided
    if not traffic_condition:
        return jsonify({'message': 'Traffic condition field is required'}), 400
   
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        # Update the traffic condition of the specific sensor
        update_query = "UPDATE sensor_data SET traffic_condition = %s WHERE sensor_id = %s;"
        cursor.execute(update_query, (traffic_condition, sensor_id))
        conn.commit()
 
        # Verify if the update was successful
        check_query = "SELECT traffic_condition FROM sensor_data WHERE sensor_id = %s;"
        cursor.execute(check_query, (sensor_id,))
        data = cursor.fetchone()
 
        # Return success response if the traffic condition was updated
        if data:
            return jsonify({
                "message": "Traffic condition adjusted successfully",
                "traffic_condition": traffic_condition
            }), 200
        else:
            # If sensor_id not found, return an error
            return jsonify({
                "message": "Sensor ID not found"
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