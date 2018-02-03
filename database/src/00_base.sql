CREATE SCHEMA botzilla;
CREATE TABLE botzilla.users(
    ID bigserial primary key,
    name varchar(254)
);
-- INSERT INTO botzilla.users (ID, name) VALUES (456164513, 'test15');

CREATE TABLE botzilla.music(
    ID bigserial primary key,
    channel_name varchar(254),
    server_name varchar(254),
    type_channel varchar(24)
);

CREATE TABLE botzilla.blacklist(
    ID bigserial primary key,
    server_name varchar(254),
    reason varchar(2000),
    total_votes integer
);

CREATE TABLE botzilla.swearwords(
    swearword varchar(254) primary key,
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

CREATE TABLE botzilla.help(name varchar primary key, info text);