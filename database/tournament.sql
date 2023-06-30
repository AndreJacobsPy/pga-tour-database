CREATE TABLE tournaments (
    tournament_id BIGSERIAL PRIMARY KEY,
    course_name TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    start_date DATE
);

INSERT INTO tournaments (course_name, city, state, country, start_date)
VALUES ('TPC River Highlands', 'Cromwell', 'Connecticut', 'United States', '2023-06-22');