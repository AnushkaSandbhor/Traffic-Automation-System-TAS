from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask import request, jsonify
from flask_jwt_extended import create_access_token
import datetime
from db import get_db_connection
import os
from routes.auth import auth_bp
from routes.vehicles import vehicles_bp
from routes.signals import signals_bp
from routes.violations import violations_bp
from routes.sensors import sensors_bp
from routes.fines import fines_bp
 
# Load environment variables from .env file
load_dotenv()
 
app = Flask(__name__)
 
# Configure JWT Secret Key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

# Define a custom error handler for invalid tokens
@jwt.unauthorized_loader
def unauthorized_error(callback):
    return jsonify({"msg": "Missing Authorization Header"}), 401
 
@jwt.invalid_token_loader
def invalid_token_error(callback):
    return jsonify({"msg": "Invalid token"}), 401
 
@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email_id = data.get('email_id')
    password = data.get('password')
 
    if not email_id or not password:
        return jsonify({'message': 'Email_id and password are required'}), 400
 
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
 
        query = "SELECT * FROM users WHERE email_id = %s AND pass = %s;"
        cursor.execute(query, (email_id, password))
        user = cursor.fetchone()
 
        if user:
            expiration = datetime.timedelta(hours=4)
            token = create_access_token(identity=user['email_id'], expires_delta=expiration)
            return jsonify({
                "message": "success",
                "credentials": {
                    "id": user['user_id'],
                    "email": user['email_id'],
                    "token": token
                }
            }), 200
        else:
            return jsonify({'status': 401, 'message': 'failed', 'Error': 'Access Denied'}), 401
 
    except Exception as err:
        return jsonify({'message': 'Database error', 'error': str(err)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
 
# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
app.register_blueprint(signals_bp, url_prefix='/signals')
app.register_blueprint(violations_bp, url_prefix='/violations')
app.register_blueprint(sensors_bp, url_prefix='/sensors')
app.register_blueprint(fines_bp, url_prefix='/fines')
 
if __name__ == '__main__':
    app.run(debug=True, port=2999)