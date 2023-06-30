CREATE TABLE strokesgained (
    id BIGSERIAL PRIMARY KEY,
    player_id INT,
    tournament_id INT,
    round_id INT,
    total INT,
    round INT,
    sg_putt DECIMAL(6, 3),
    sg_arg DECIMAL(6, 3),
    sg_app DECIMAL(6, 3),
    sg_ott DECIMAL(6, 3),
    sg_t2g DECIMAL(6, 3),
    sg_total DECIMAL(6, 3),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id),
    FOREIGN KEY (round_id) REFERENCES rounds(round_id)
);

ALTER TABLE strokesgained
ADD UNIQUE (player_id, tournament_id, round_id);