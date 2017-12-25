
-- ROLE

CREATE OR REPLACE FUNCTION system.get_role(name character varying)
    RETURNS system.role AS
$$
    SELECT * FROM system.role WHERE role.name = $1;
$$ LANGUAGE sql STABLE;


-- RIGHT

CREATE OR REPLACE FUNCTION system.get_right(name character varying)
    RETURNS system."right" AS
$$
    SELECT * FROM system."right" WHERE "right".name = $1;
$$ LANGUAGE sql STABLE;

