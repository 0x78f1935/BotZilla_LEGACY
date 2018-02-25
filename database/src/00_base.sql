CREATE SCHEMA botzilla;
CREATE TABLE botzilla.users(
    ID bigserial primary key,
    name varchar(508)
);
-- INSERT INTO botzilla.users (ID, name) VALUES (456164513, 'test15');

CREATE TABLE botzilla.help(
    name varchar(200) primary key,
    cog varchar(200),
    info varchar(1500)
);

CREATE TABLE botzilla.mute(
    id varchar(200) primary key
);

CREATE TABLE botzilla.music(
    ID bigserial primary key,
    channel_name varchar(508),
    server_name varchar(508),
    type_channel varchar(24)
);

CREATE TABLE botzilla.battleship(
    ID bigserial primary key,
    gamehash varchar(508),
    board varchar(1700),
    score varchar(508),
    ship_row varchar(508),
    ship_col varchar(508),
    last_message varchar(508)
);

CREATE TABLE botzilla.blacklist(
    ID bigserial primary key,
    server_name varchar(508),
    reason varchar(2000),
    total_votes integer
);

CREATE TABLE botzilla.swearwords(
    swearword varchar(508) primary key,
    total bigserial
);

INSERT INTO botzilla.swearwords(swearword, total) VALUES ('shit', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('fuck', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('damn', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('questionmark', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('crap', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('pussy', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('wtf', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('fag', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('gay', 0);