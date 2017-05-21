DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS users;

DROP INDEX IF EXISTS votes_thread_id_idx;
DROP INDEX IF EXISTS posts_thread_id_idx;
DROP INDEX IF EXISTS posts_parent_id_idx;
DROP INDEX IF EXISTS votes_multi_idx;

CREATE EXTENSION IF NOT EXISTS CITEXT;

CREATE TABLE IF NOT EXISTS "users" (
	"nickname" CITEXT COLLATE ucs_basic PRIMARY KEY,
	"email" CITEXT UNIQUE,
	"fullname" TEXT,
	"about" TEXT
);

CREATE TABLE IF NOT EXISTS "forums" (
	"slug" CITEXT PRIMARY KEY NOT NULL,
	"title" TEXT NOT NULL,
	"posts" INTEGER DEFAULT 0,
	"threads" INTEGER DEFAULT 0,
	"user" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "threads" (
	"id" SERIAL PRIMARY KEY,
	"slug" CITEXT UNIQUE DEFAULT NULL,
	"title" TEXT NOT NULL,
	"message" TEXT,
	"author" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE,
	"created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"forum" CITEXT NOT NULL REFERENCES forums ("slug") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "votes" (
	"nickname" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE,
	"thread" INTEGER REFERENCES "threads" ("id") ON DELETE CASCADE,
	"voice" INTEGER DEFAULT 0,
	PRIMARY KEY ("nickname", "thread")
);

CREATE INDEX IF NOT EXISTS votes_thread_id_idx
	ON "votes" ("thread");

CREATE TABLE IF NOT EXISTS "posts" (
	"id" SERIAL PRIMARY KEY,
	"message" TEXT,
	"author" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE,
	"forum" CITEXT NOT NULL REFERENCES "forums" ("slug"),
	"thread" INTEGER REFERENCES "threads" ("id") ON DELETE CASCADE,
	"parent" INTEGER DEFAULT NULL REFERENCES "posts" ("id"),
	"created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"isEdited" BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS posts_thread_id_idx
	ON "posts" ("thread");

CREATE INDEX IF NOT EXISTS posts_parent_id_idx
	ON "posts" ("parent");

CREATE INDEX IF NOT EXISTS posts_multi_idx
	ON "posts" ("thread", "parent", "id");
