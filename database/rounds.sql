CREATE TABLE rounds (
    round_id BIGSERIAL PRIMARY KEY,
    tournament_id INT,
    round INT,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id)
);

ALTER TABLE rounds
ADD UNIQUE (tournament_id, round);