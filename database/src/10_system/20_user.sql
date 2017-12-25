
-- USER

CREATE OR REPLACE FUNCTION system.get_user_by_name(username character varying)
    RETURNS system."user" AS
$$
    SELECT * FROM system."user" WHERE "user".username = $1;
$$ LANGUAGE sql STABLE;

CREATE OR REPLACE FUNCTION system.get_user(id integer)
    RETURNS system."user" AS
$$
    SELECT * FROM system."user" WHERE "user".id = $1;
$$ LANGUAGE sql STABLE;

CREATE OR REPLACE FUNCTION system.new_user(username character varying, fullname character varying, email character varying, enabled boolean)
    RETURNS system."user" AS
$$
    INSERT INTO system."user" (username, fullname, email, enabled)
        VALUES ($1, $2, $3, $4)
    RETURNING "user";
$$ LANGUAGE SQL VOLATILE;

CREATE OR REPLACE FUNCTION system.update_user(user_id integer, username character varying, fullname character varying, email character varying, enabled boolean)
    RETURNS system."user" AS
$$
    UPDATE system."user"
        SET username = $2, fullname = $3, email = $4, enabled = $5
    WHERE id = $1
    RETURNING "user";
$$ LANGUAGE SQL VOLATILE;

CREATE OR REPLACE FUNCTION system.get_user_rights(user_id integer)
    RETURNS SETOF system."right" AS
$$
    SELECT "right".*
    FROM system.user_role
    JOIN system.role_right on role_right.role_id = user_role.role_id
    JOIN system."right" on "right".id = role_right.right_id
    WHERE user_role.user_id = $1;
$$ LANGUAGE sql STABLE;


CREATE OR REPLACE FUNCTION system.change_password(id integer, old_password character varying, new_password character varying)
    RETURNS system."user" AS
$$
    UPDATE system."user"
        SET password = $3
    WHERE id = $1
        AND ( password = $2 OR (password is null and $2 is null))
    RETURNING "user"
$$ LANGUAGE sql VOLATILE;
