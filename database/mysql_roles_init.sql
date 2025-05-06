DROP ROLE IF EXISTS 'normal_role', 'advanced_role';

CREATE ROLE 'normal_role';
GRANT SELECT ON playstation.* TO 'normal_role';

CREATE ROLE 'advanced_role';
GRANT SELECT, INSERT, UPDATE, DELETE ON playstation.* TO 'advanced_role';

SET GLOBAL activate_all_roles_on_login = ON;