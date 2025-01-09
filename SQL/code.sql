CREATE DATABASE traffic_control;
use traffic_control;

CREATE TABLE traffic_signals(
	signal_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255),
    signal_state ENUM('Red','Yellow','Green'),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_data(
	sensor_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    traffic_count INT,
    average_speed DECIMAL(5,2),
    traffic_condition VARCHAR(255) 
);

CREATE TABLE vehicles(
	vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(255) NOT NULL UNIQUE,
    owner_name VARCHAR(255),
    vehicle_type VARCHAR(50),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cameras(
	camera_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255),
    camera_feed_url VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE violations(
	violation_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT,
    signal_id INT,
    violation_type VARCHAR(255),
    violation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fine_amount DECIMAL(10,2),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (signal_id) REFERENCES traffic_signals(signal_id)
);

CREATE TABLE fines(
	fine_id INT AUTO_INCREMENT PRIMARY KEY,
    violation_id INT,
    fine_status ENUM('Paid','Unpaid') DEFAULT 'Unpaid',
    payment_date TIMESTAMP NULL,
    FOREIGN KEY (violation_id) REFERENCES violations(violation_id)
);

-- Sample data for vehicles
INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type)
VALUES 
('ABC123', 'John Doe', 'Sedan'),
('XYZ789', 'Jane Smith', 'SUV'),
('LMN456', 'Mike Johnson', 'Truck'),
('PQR321', 'Sara Lee', 'Motorcycle');

-- Sample data for traffic signals
INSERT INTO traffic_signals (location, signal_state)
VALUES 
('Main Street & 1st Ave', 'Red'),
('Elm St & Oak Rd', 'Green'),
('Broadway & 5th Ave', 'Yellow');

-- Sample data for violations
INSERT INTO violations (vehicle_id, signal_id, violation_type, fine_amount)
VALUES 
(1, 1, 'Red Light Jump', 150.00),
(2, 2, 'Speeding', 200.00);

-- Sample data for fines
INSERT INTO fines (violation_id, fine_status)
VALUES 
(1, 'Unpaid'),
(2, 'Paid');

-- Sample data for sensor data
INSERT INTO sensor_data (location, traffic_count, average_speed, traffic_condition)
VALUES 
('Main Street', 250, 45.6, 'Moderate'),
('5th Avenue', 180, 40.0, 'Heavy'),
('Oak Road', 300, 50.0, 'Clear');

-- Sample data for cameras
INSERT INTO cameras (location, camera_feed_url)
VALUES 
('Main Street Camera 1', 'http://s3.amazonaws.com/camera1_feed'),
('5th Avenue Camera 2', 'http://s3.amazonaws.com/camera2_feed');

SELECT * FROM cameras;
SELECT * FROM violations;
SELECT * FROM fines;


    
    