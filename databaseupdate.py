"""Updates the "base" database to latest version. Run code to execute changes."""

import functions

query = """ALTER TABLE game
DROP COLUMN next_turn
;

ALTER TABLE game
ADD COLUMN next_turn TIMESTAMP
DEFAULT CURRENT_TIMESTAMP
;

ALTER TABLE game
DROP COLUMN starttime
;

ALTER TABLE game
ADD COLUMN starttime TIMESTAMP
DEFAULT CURRENT_TIMESTAMP
;

DROP TABLE lentoalukset
;

CREATE TABLE lentoalukset (
id INT NOT NULL auto_increment,
type VARCHAR(254),
type_numeric INT,
model_name VARCHAR(254),
co2_per_km INT,
max_range_km INT,
speed_kmh INT,
PRIMARY KEY (id)
)
;

INSERT INTO lentoalukset(type, type_numeric, model_name, co2_per_km, max_range_km, speed_kmh)
VALUES("isolentokone", 5, "Boeing B747-400ER", 90, 14200, 1127),
("isolentokone", 5, "Airbus A320-200", 68, 5900, 871),
("lentokone", 1, "Saab 90 scandia", 95, 2350, 370),
("lentokone", 1, "Bombardier Q series Dash 8Q-400", 71, 1569, 629),
("kuumailmapallo", 2, "puinen kuumailmapallo", 0, 30000, 15),
("vesitaso", 4, "vesitaso AVIC AG600", 65, 4500, 560),
("vesitaso", 4, "vesitaso Privateer", 59, 1600, 398),
("helikopteri", 3, "helikopteri AW169", 63, 820, 306),
("helikopteri", 3, "helikopteri EC145", 52, 680, 260)
;

ALTER TABLE airport
DROP COLUMN wikipedia_link
;

ALTER TABLE airport
DROP COLUMN keywords
;

ALTER TABLE airport
DROP COLUMN home_link
;

ALTER TABLE airport
DROP COLUMN iata_code
;

ALTER TABLE airport
DROP COLUMN gps_code
;

ALTER TABLE airport
DROP COLUMN  local_code
;

ALTER TABLE country
DROP COLUMN  keywords
;

SET @count = 0;
UPDATE airport SET airport.id = @count:= @count + 1
;

DELETE FROM goal
;

ALTER TABLE goal
DROP COLUMN  name
;

ALTER TABLE goal
DROP COLUMN  icon
;

ALTER TABLE goal
DROP COLUMN  target
;

ALTER TABLE goal
DROP COLUMN  target_minvalue
;

ALTER TABLE goal
DROP COLUMN  target_maxvalue
;

ALTER TABLE goal
DROP COLUMN  target_text
;

ALTER TABLE game
DROP COLUMN airportid
;

ALTER TABLE goal
ADD COLUMN airportid INT NOT NULL
;

ALTER TABLE game
DROP COLUMN goalreached
;

ALTER TABLE goal
ADD COLUMN goalreached INT NOT NULL DEFAULT 0
;

ALTER TABLE goal_reached
DROP CONSTRAINT goal_reached_ibfk_2
;

DROP TABLE goal
;

CREATE TABLE goal (
id INT NOT NULL,
goalreached BOOL NOT NULL DEFAULT 0,
airportid INT NOT NULL,
PRIMARY KEY (id)
)
;

ALTER TABLE goal_reached
ADD CONSTRAINT FK_gameid_game
FOREIGN KEY (game_id) REFERENCES game(id)
;

ALTER TABLE goal_reached
ADD CONSTRAINT FK_goalid_goal
FOREIGN KEY (goal_id) REFERENCES goal(id)
;

CREATE TABLE leaderboard (
name VARCHAR(254) NOT NULL,
score INT NOT NULL
)
;

ALTER TABLE game
ALTER co2_consumed SET DEFAULT 0,
ALTER co2_budget SET DEFAULT 10000,
ALTER location SET DEFAULT "EGCC"
;

ALTER TABLE lentoalukset
ADD CONSTRAINT UNIQUE(co2_per_km)
;

ALTER TABLE game
DROP COLUMN co2_budget
;"""

functions.cursor(query)