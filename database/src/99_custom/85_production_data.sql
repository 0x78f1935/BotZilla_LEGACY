--=============================================
--Insert CSV Data into temporary staging tables
--=============================================

--------------
--antennes.csv
--------------
\c database bot

CREATE DATABASE bot;
CREATE SCHEMA botzilla;
CREATE TABLE botzilla.users(
    ID bigserial primary key,
    name varchar(254),
    date_added timestamp default NULL
);