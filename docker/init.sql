CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    equipment_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER REFERENCES equipment(id),
    air_temperature FLOAT,
    process_temperature FLOAT,
    rotational_speed FLOAT,
    torque FLOAT,
    tool_wear FLOAT,
    failure_prediction INTEGER,
    failure_probability FLOAT,
    risk_level VARCHAR(20),
    maintenance_recommendation TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO equipment (equipment_name, equipment_type)
VALUES ('Machine-001', 'M');