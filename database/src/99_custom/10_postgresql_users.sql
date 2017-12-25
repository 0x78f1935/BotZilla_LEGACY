
-- user: gis_web (passw: 'gis_web')
DO
$$
BEGIN
    IF NOT EXISTS(SELECT * FROM pg_roles WHERE rolname = 'gis_web') THEN
        CREATE ROLE gis_web LOGIN
            NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;
    END IF;

END
$$;

-- user: gis_importer (passw: 'gis_importer')
DO
$$
BEGIN
    IF NOT EXISTS(SELECT * FROM pg_roles WHERE rolname = 'gis_importer') THEN
        CREATE ROLE gis_importer LOGIN
            NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;
    END IF;

END
$$;


GRANT gis TO gis_web;
GRANT gis_writer TO gis_importer;
