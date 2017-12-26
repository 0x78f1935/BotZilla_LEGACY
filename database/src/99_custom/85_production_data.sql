--=============================================
--Insert CSV Data into temporary staging tables
--=============================================

--------------
--antennes.csv
--------------

CREATE SCHEMA botzilla;
CREATE TABLE botzilla.users(
    ID bigserial primary key,
    name varchar(254),
    date_added timestamp default NULL
);
INSERT INTO botzilla.users (ID, name, date_added) VALUES (456164513, 'test15', NULL);