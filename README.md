# Traffic Automation System (TAS)

## Objective

The **Traffic Automation System (TAS)** is a modern solution for managing traffic in a smart city. It streamlines the management and monitoring of traffic signals, real-time traffic flow, violations, and vehicle registration using advanced technologies.

---

## Features

1. **Vehicle Registration**  
   - Users can register vehicles with details like vehicle number, model, and owner information.

2. **Traffic Signal Management**  
   - Authorities can manage and control traffic signals and adjust timings dynamically based on real-time traffic conditions.

3. **Real-Time Traffic Monitoring**  
   - Traffic sensors and cameras track traffic flow, helping optimize signal timings.

4. **Violation Detection and Management**  
   - Automatic detection of traffic violations (e.g., red-light jumping, speeding) using cameras and sensors.

5. **Violation Reporting**  
   - Generation of violation reports with images, fines, and vehicle details.

6. **Dynamic Signal Adjustment**  
   - Traffic signal timings are adjusted dynamically based on real-time sensor data.

---

## Tech Stack

1. **Backend**: Flask (Python)  
2. **Database**:  
   - **MySQL**: For structured data such as traffic signals, vehicles, and violation reports.  
   - **MongoDB**: For unstructured data such as traffic sensor logs and camera footage.  
3. **Cloud Integration**: AWS S3 for storing violation images and videos.

---

## API Endpoints

### Traffic Signal Management

- **Delete Traffic Signal**  
  - **Endpoint**: `DELETE /signals/{signal_id}`  
  - **Input**:  
    ```json
    { "signal_id": 1 }
    ```
  - **Response**:  
    ```json
    { "message": "Traffic signal deleted successfully" }
    ```
  - **Status Codes**:
    - `200`: Success
    - `404`: Signal not found
    - `500`: Database error

### Other APIs (Highlights)

- **Register Vehicle**: `POST /vehicles/register`  
- **Update Signal State**: `PUT /signals/{signal_id}/state`  
- **Generate Violation Report**: `POST /violations/generate`  
- **Monitor Traffic Sensor Data**: `GET /sensors/{sensor_id}/data`

For more details, refer to the API documentation.

---

## Database Design

1. **MySQL**:  
   - **Tables**:  
     - `vehicles`: Stores vehicle registration data.  
     - `traffic_signals`: Manages traffic signal information.  
     - `violations`: Stores violation records.  
     - `fines`: Tracks fine payments.  

2. **MongoDB**:  
   - **Collections**:  
     - `camera_footage`: Stores traffic sensor logs and violation images.  

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TrafficSignalManager.git
   cd TrafficSignalManager

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Configure the database:
   - Set up MySQL and MongoDB as per the schema.
   - Update the config.py with your database credentials.

4. Run the Flask application:
   ```bash
   flask run

---

## Usage

 - Use tools like Postman or cURL to test the APIs.
 - For real-time data, integrate traffic sensors and cameras with the system.

---

## Future Enhancements

 - Integration with AI/ML for better traffic predictions.
 - Mobile app for end-users to monitor traffic in real-time.
 - Advanced violation detection using deep learning.

---

## License

 This project is licensed under the MIT License.


