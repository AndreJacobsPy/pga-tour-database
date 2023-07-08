CREATE TABLE tournaments (
    tournament_id BIGSERIAL PRIMARY KEY,
    course_name TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    start_date DATE,
    name TEXT
);

INSERT INTO tournaments (course_name, city, state, country, start_date, name)
VALUES ('Los Angeles Country Club', 'Los Angeles', 'California', 'United States', '2023-06-15', 'US Open'),
    ('TPC River Highlands', 'Cromwell', 'Connecticut', 'United States', '2023-06-22', 'Travelers Championship'),
    ('Detroit Golf Club', 'Detroit', 'Michigan', 'United States', '2023-06-29', 'Rocket Mortgage');