-- sensor_readings
CREATE TABLE IF NOT EXISTS sensor_readings (
    id integer PRIMARY KEY,
    ldr float,
    sunpanel float,
    text_datetime text NOT NULL
);
