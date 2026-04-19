CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    city TEXT NOT NULL,
    product_type TEXT NOT NULL,
    value NUMERIC,
    unit TEXT,
    wind_speed NUMERIC,
    wind_direction NUMERIC,
    timestamp TIMESTAMPTZ NOT NULL
);
