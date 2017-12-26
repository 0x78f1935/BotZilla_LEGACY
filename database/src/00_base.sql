CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS "directory";

CREATE TABLE IF NOT EXISTS "directory"."pointset"
(
  "id" serial NOT NULL,
  "name" varchar(50) NOT NULL,
  "style_id" integer,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "directory"."pointset_attribute"
(
  "id" serial NOT NULL,
  "joindate" timestamp NOT NULL,
  "name" varchar(50) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "directory"."style"
(
  "id" serial NOT NULL,
  "name" varchar(50) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "directory"."style_zoomlevel"
(
  "style_id" integer NOT NULL,
  "zoomlevel_id" integer NOT NULL,
  "config" jsonb NOT NULL,
  PRIMARY KEY (style_id, zoomlevel_id)
);

CREATE SCHEMA IF NOT EXISTS "system";

CREATE TABLE IF NOT EXISTS "system"."user"
(
  "id" serial NOT NULL,
  "username" varchar(64) NOT NULL,
  "password" varchar(250),
  "fullname" varchar(100),
  "email" varchar(100),
  "enabled" boolean NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS "system"."role"
(
  "id" serial NOT NULL,
  "name" varchar(100) NOT NULL,
  "description" text,
  PRIMARY KEY (id),
  UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS "system"."user_role"
(
  "user_id" integer NOT NULL,
  "role_id" integer NOT NULL,
  PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS "system"."right"
(
  "id" serial NOT NULL,
  "name" varchar(100) NOT NULL,
  "description" text,
  PRIMARY KEY (id),
  UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS "system"."role_right"
(
  "role_id" integer NOT NULL,
  "right_id" integer NOT NULL,
  PRIMARY KEY (role_id, right_id)
);

CREATE TABLE IF NOT EXISTS "system"."session"
(
  "id" varchar(64) NOT NULL,
  "user_id" integer,
  "expiration_time" timestamp NOT NULL,
  PRIMARY KEY (id)
);

ALTER TABLE "directory"."pointset_attribute" ADD CONSTRAINT "directory_pointset_attribute_fk_0" FOREIGN KEY (pointset_id) REFERENCES "directory"."pointset" (id);
ALTER TABLE "system"."user_role" ADD CONSTRAINT "system_user_role_fk_0" FOREIGN KEY (user_id) REFERENCES "system"."user" (id);
ALTER TABLE "system"."user_role" ADD CONSTRAINT "system_user_role_fk_1" FOREIGN KEY (role_id) REFERENCES "system"."role" (id);
ALTER TABLE "system"."role_right" ADD CONSTRAINT "system_role_right_fk_0" FOREIGN KEY (role_id) REFERENCES "system"."role" (id);
ALTER TABLE "system"."role_right" ADD CONSTRAINT "system_role_right_fk_1" FOREIGN KEY (right_id) REFERENCES "system"."right" (id);
ALTER TABLE "system"."session" ADD CONSTRAINT "system_session_fk_0" FOREIGN KEY (user_id) REFERENCES "system"."user" (id);