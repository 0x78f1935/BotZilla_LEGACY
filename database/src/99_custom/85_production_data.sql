--=============================================
--Insert CSV Data into temporary staging tables
--=============================================

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
    total_users varchar(24)
);