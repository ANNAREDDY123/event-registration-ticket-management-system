CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE events(
    id INTEGER PRIMARY KEY,
    event_name VARCHAR(100),
    description TEXT,
    location VARCHAR(100),
    event_date DATE,
    total_seats INTEGER,
    available_seats INTEGER
);

CREATE TABLE registrations(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    event_id INTEGER,
    registration_date DATETIME
);

CREATE TABLE tickets(
    id INTEGER PRIMARY KEY,
    registration_id INTEGER,
    ticket_number VARCHAR(100),
    attendee_name VARCHAR(100),
    event_name VARCHAR(100),
    registration_date DATETIME
);
