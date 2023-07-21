CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);


CREATE TABLE IF NOT EXISTS app_users (
    id INTEGER PRIMARY KEY,
    tenant_id INT NOT NULL
        CONSTRAINT fk_tenants_tenant_id REFERENCES tenants ON UPDATE CASCADE ON DELETE RESTRICT,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

ALTER TABLE app_users ENABLE ROW LEVEL SECURITY;

CREATE POLICY app_users_isolation_policy
  ON app_users
  USING (tenant_id = current_setting('app.current_tenant')::INTEGER);


CREATE TABLE IF NOT EXISTS logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id INT NOT NULL
        CONSTRAINT fk_tenants_tenant_id REFERENCES tenants ON UPDATE CASCADE ON DELETE RESTRICT,
    log TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

ALTER TABLE logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY logs_isolation_policy
  ON logs
  USING (tenant_id = current_setting('app.current_tenant')::INTEGER);


INSERT INTO tenants (id, name) VALUES (1, 'tenant1');
INSERT INTO tenants (id, name) VALUES (2, 'tenant2');
INSERT INTO app_users (id, tenant_id, name) VALUES (1, 1, 'user1');
INSERT INTO app_users (id, tenant_id, name) VALUES (2, 2, 'user2');
INSERT INTO app_users (id, tenant_id, name) VALUES (3, 1, 'user3');

CREATE ROLE test_user WITH LOGIN PASSWORD 'password';
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO test_user;
