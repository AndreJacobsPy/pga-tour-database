CREATE TABLE rounds (
    round_id BIGSERIAL PRIMARY KEY,
    tournament_id INT FOREIGN KEY REFERENCES tournaments(tournament_id)
    round INT
);

ALTER TABLE rounds
ADD UNIQUE (tournament_id, round);