--=============================================
--Insert CSV Data into temporary staging tables
--=============================================

--------------
--antennes.csv
--------------

CREATE SCHEMA botzilla;
CREATE TABLE botzilla.users(
    ID bigserial primary key,
    name varchar(254)
);
-- INSERT INTO botzilla.users (ID, name,) VALUES (456164513, 'test15');