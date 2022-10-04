DROP TABLE IF EXISTS company_to_tag;
DROP TABLE IF EXISTS founder_social_to_social;
DROP TABLE IF EXISTS company_social_to_social;
DROP TABLE IF EXISTS social;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS founder;
DROP TABLE IF EXISTS company;


CREATE TABLE "company" (
  "id" int PRIMARY KEY,
  "company_name" varchar,
  "link" varchar,
  "short_description" varchar,
  "founded" int,
  "team_size" int,
  "location" varchar,
  "country" varchar,
  "no_founders" int,
  "no_company_socials" int,
  "no_tags" int,
  "description" text
);

CREATE TABLE "founder" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "role" varchar,
  "company_id" int
);

CREATE TABLE "social" (
  "id" int PRIMARY KEY,
  "social" varchar
);

CREATE TABLE "tag" (
  "id" int PRIMARY KEY,
  "tag" varchar
);

CREATE TABLE "founder_social_to_social" (
  "id" int PRIMARY KEY,
  "social_media_id" int,
  "founder_id" int
);

CREATE TABLE "company_social_to_social" (
  "id" int PRIMARY KEY,
  "social_media_id" int,
  "company_id" int
);

CREATE TABLE "company_to_tag" (
  "id" int PRIMARY KEY,
  "company_id" int,
  "tag_id" int
);

ALTER TABLE "founder" ADD FOREIGN KEY ("company_id") REFERENCES "company" ("id");

ALTER TABLE "founder_social_to_social" ADD FOREIGN KEY ("social_media_id") REFERENCES "social" ("id");

ALTER TABLE "founder_social_to_social" ADD FOREIGN KEY ("founder_id") REFERENCES "founder" ("id");

ALTER TABLE "company_social_to_social" ADD FOREIGN KEY ("social_media_id") REFERENCES "social" ("id");

ALTER TABLE "company_social_to_social" ADD FOREIGN KEY ("company_id") REFERENCES "company" ("id");

ALTER TABLE "company_to_tag" ADD FOREIGN KEY ("company_id") REFERENCES "company" ("id");

ALTER TABLE "company_to_tag" ADD FOREIGN KEY ("tag_id") REFERENCES "tag" ("id");
