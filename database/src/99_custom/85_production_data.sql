CREATE TABLE botzilla.musicque(
    url varchar(508) primary key
);

CREATE TABLE botzilla.highlow(
    ID bigint primary key,
    server_name varchar(508),
    score bigserial
);

CREATE TABLE botzilla.battleship(
    ID bigint primary key,
    gamehash varchar(508),
    board varchar(1700),
    score varchar(508),
    ship_row varchar(508),
    ship_col varchar(508),
    last_message varchar(508),
    online VARCHAR(508),
    enemy VARCHAR(508)
);

CREATE TABLE botzilla.infect(
    ID bigint primary key,
    until varchar(508),
    emoji VARCHAR(508)
);

--INSERT INTO botzilla.highlow(ID, server_name, score) VALUES( , '', )