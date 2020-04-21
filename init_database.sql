CREATE TABLE IF NOT EXISTS sensor_readings (
    id integer PRIMARY KEY,
    ldr integer,
    sunpanel integer,
    text_datetime text NOT NULL
);

CREATE TABLE IF NOT EXISTS 2ch_sensor (
    id integer PRIMARY KEY,
    ldr integer,
    sunpanel integer,
    txt_date text NOT NULL
    txt_time text NOT NULL
);

CREATE TABLE IF NOT EXISTS ads1115 (
    id integer PRIMARY KEY,
    ch0 integer,
    ch1 integer,
    ch2 integer,
    ch3 integer,
    txt_date text NOT NULL
    txt_time text NOT NULL
);
