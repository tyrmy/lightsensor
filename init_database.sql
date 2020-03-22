-- sensor_readings
CREATE TABLE IF NOT EXISTS sensor_readings (
    id integer PRIMARY KEY,
    ldr integer,
    sunpanel integer,
    text_datetime text NOT NULL
);
