INSERT INTO system."right" (name, description)
    VALUES
        ('login', 'Right to login'),
        ('default.view', 'Normal right to view'),
        ('default.edit', 'Normal right to view'),
        ('default.add', 'Normal right to view'),
        ('default.delete', 'Normal right to view'),
        ('system.view', 'System right to view'),
        ('system.edit', 'System right to view'),
        ('system.add', 'System right to view'),
        ('system.delete', 'System right to view');

INSERT INTO system."role" (name, description)
    VALUES
        ('user', 'Normal User'),
        ('admin', 'Administrator');

INSERT INTO system."role_right" (role_id, right_id)
    SELECT (system.get_role('admin')).id, "right".id FROM system."right";

INSERT INTO system."role_right" (role_id, right_id) SELECT (system.get_role('user')).id, (system.get_right('login')).id;
INSERT INTO system."role_right" (role_id, right_id) SELECT (system.get_role('user')).id, (system.get_right('default.view')).id;
