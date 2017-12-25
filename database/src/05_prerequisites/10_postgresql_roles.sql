-- Create users, needed for BI-Bricks GIS tool.

-- user: gis_admin
DO
$$
BEGIN
    IF NOT EXISTS(SELECT * FROM pg_roles WHERE rolname = 'gis_admin') THEN
        CREATE ROLE gis_admin LOGIN
            NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;
    END IF;
END
$$;

-- role: gis
DO
$$
BEGIN
    IF NOT EXISTS(SELECT * FROM pg_roles WHERE rolname = 'gis') THEN
        CREATE ROLE gis
            NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;
    END IF;
END
$$;

-- role: gis_writer
DO
$$
BEGIN
    IF NOT EXISTS(SELECT * FROM pg_roles WHERE rolname = 'gis_writer') THEN
        CREATE ROLE gis_writer
            NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;
    END IF;

END
$$;

GRANT gis TO gis_writer;
GRANT gis TO gis_admin;
GRANT gis_writer TO gis_admin;

