CREATE TABLE botzilla.musicque(
    url varchar(508) primary key
);

CREATE TABLE botzilla.highlow(
    ID bigserial primary key,
    server_name varchar(254),
    score bigserial
);

--INSERT INTO botzilla.highlow(ID, server_name, score) VALUES( , '', )