INSERT INTO system."user" (username, password, fullname, email, enabled)
    VALUES
        ('guest', 'guest', 'Guest User', 'guest@bi-bricks.com', True);

INSERT INTO system."user_role" (user_id, role_id)
    SELECT
        (system.get_user_by_name('guest')).id, (system.get_role('user')).id;


INSERT INTO system."user" (username, password, fullname, email, enabled)
    VALUES
        ('admin', 'admin', 'Administrator', 'admin@bi-bricks.com', True);

INSERT INTO system."user_role" (user_id, role_id)
    SELECT
        (system.get_user_by_name('admin')).id, (system.get_role('admin')).id;