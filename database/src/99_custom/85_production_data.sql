--=============================================
--Insert CSV Data into temporary staging tables
--=============================================

--------------
--antennes.csv
--------------

CREATE TABLE staging.antennes (
  x text,
  y text,
  hoofdsoort text,
  sat_code text,
  postcode text,
  woonplaats text,
  gemeente text,
  plaatsing text,
  ingebruikname text,
  objectid text,
  hoogte text,
  hoofdstraalrichting text,
  frequentie text,
  vermogen text,
  "veiligeAfstand" text
);

COPY staging.antennes FROM '/database/input/antennes.csv' CSV HEADER DELIMITER ';';

ALTER TABLE staging.antennes ADD COLUMN freq decimal;

UPDATE staging.antennes SET freq = substring(frequentie FROM '([0-9.]+) M.*')::DECIMAL;


-------------------------------
--frequency_bands_operators.csv
-------------------------------

CREATE TABLE staging.operators (
  operator text,
  band_start_MHz text,
  band_end_MHz text,
  type text,
  remarks text
);

COPY staging.operators FROM '/database/input/frequency_bands_operators.csv' CSV HEADER DELIMITER ';';


--====================================
--transfer staged data to point tables
--====================================

-----------
--All Sites
-----------

SELECT directory.create_pointset('Site'::text, 0, '{postcode,woonplaats,gemeente}');

INSERT INTO point."Site"(
  position,
  postcode,
  woonplaats,
  gemeente
)
SELECT
  ST_Transform(ST_SetSRID(ST_MakePoint(x::numeric,y::numeric), 28992), 4326),
  postcode,
  woonplaats,
  gemeente
FROM staging.antennes
GROUP BY x,y,postcode,woonplaats,gemeente;

-------------
--KPN sectors
-------------

SELECT
    directory.create_pointset(
        'KPN'::text,
        0,
        '{azimuth,hoofdsoort,sat_code,postcode,woonplaats,gemeente,plaatsing,ingebruikname,objectid,hoogte,hoofdstraalrichting,frequentie,vermogen,veiligeAfstand,type}');

INSERT INTO point."KPN"(position,azimuth,hoofdsoort,sat_code,postcode,woonplaats,gemeente,plaatsing, ingebruikname,objectid, hoogte,hoofdstraalrichting,frequentie,vermogen,"veiligeAfstand",type)
    SELECT
      ST_Transform(ST_SetSRID(ST_MakePoint(x::numeric,y::numeric), 28992), 4326),
      substring(hoofdstraalrichting FROM '([0-9.]+).*'),
      hoofdsoort,
      sat_code,
      postcode,
      woonplaats,
      gemeente,
      plaatsing,
      ingebruikname,
      objectid,
      hoogte,
      hoofdstraalrichting,
      frequentie,
      vermogen,
      "veiligeAfstand",
      "type"
    FROM staging.antennes
    JOIN staging.operators ON freq > operators.band_start_MHz::decimal AND freq < operators.band_end_MHz::decimal
    WHERE hoofdstraalrichting IS NOT NULL AND operator = 'KPN';


------------------
--T-Mobile sectors
------------------

SELECT
    directory.create_pointset(
        'T-Mobile'::text,
        0,
        '{azimuth,hoofdsoort,sat_code,postcode,woonplaats,gemeente,plaatsing,ingebruikname,objectid,hoogte,hoofdstraalrichting,frequentie,vermogen,veiligeAfstand,type}');

INSERT INTO point."T-Mobile"(position,azimuth,hoofdsoort,sat_code,postcode,woonplaats,gemeente,plaatsing, ingebruikname,objectid, hoogte,hoofdstraalrichting,frequentie,vermogen,"veiligeAfstand",type)
    SELECT
      ST_Transform(ST_SetSRID(ST_MakePoint(x::numeric,y::numeric), 28992), 4326),
      substring(hoofdstraalrichting FROM '([0-9.]+).*'),
      hoofdsoort,
      sat_code,
      postcode,
      woonplaats,
      gemeente,
      plaatsing,
      ingebruikname,
      objectid,
      hoogte,
      hoofdstraalrichting,
      frequentie,
      vermogen,
      "veiligeAfstand",
      "type"
    FROM staging.antennes
    JOIN staging.operators ON freq > operators.band_start_MHz::decimal AND freq < operators.band_end_MHz::decimal
    WHERE hoofdstraalrichting IS NOT NULL AND operator = 'T-Mobile';

------------------
--Vodafone sectors
------------------

SELECT
    directory.create_pointset(
        'Vodafone'::text,
        0,
        '{azimuth,hoofdsoort,sat_code,postcode,woonplaats,gemeente,plaatsing,ingebruikname,objectid,hoogte,hoofdstraalrichting,frequentie,vermogen,veiligeAfstand,type}');

INSERT INTO point."Vodafone"(position,azimuth,hoofdsoort,sat_code,postcode,woonplaats,gemeente,plaatsing, ingebruikname,objectid, hoogte,hoofdstraalrichting,frequentie,vermogen,"veiligeAfstand",type)
    SELECT
      ST_Transform(ST_SetSRID(ST_MakePoint(x::numeric,y::numeric), 28992), 4326),
      substring(hoofdstraalrichting FROM '([0-9.]+).*'),
      hoofdsoort,
      sat_code,
      postcode,
      woonplaats,
      gemeente,
      plaatsing,
      ingebruikname,
      objectid,
      hoogte,
      hoofdstraalrichting,
      frequentie,
      vermogen,
      "veiligeAfstand",
      "type"
    FROM staging.antennes
    JOIN staging.operators ON freq > operators.band_start_MHz::decimal AND freq < operators.band_end_MHz::decimal
    WHERE hoofdstraalrichting IS NOT NULL AND operator = 'Vodafone';
