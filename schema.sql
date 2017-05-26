DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS forum_users;
DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS users;

CREATE EXTENSION IF NOT EXISTS CITEXT;

SET SYNCHRONOUS_COMMIT = 'off';

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

CREATE INDEX IF NOT EXISTS forums_user_idx
	ON "forums" ("user");

CREATE TABLE IF NOT EXISTS "threads" (
	"id" SERIAL PRIMARY KEY,
	"slug" CITEXT UNIQUE DEFAULT NULL,
	"title" TEXT NOT NULL,
	"message" TEXT,
	"author" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE,
	"created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"forum" CITEXT NOT NULL REFERENCES forums ("slug") ON DELETE CASCADE,
	"votes" INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS threads_author_idx
	ON "threads" ("author");

CREATE INDEX IF NOT EXISTS threads_forum_idx
	ON "threads" ("forum");


CREATE TABLE IF NOT EXISTS "votes" (
	"nickname" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE,
	"thread" INTEGER REFERENCES "threads" ("id") ON DELETE CASCADE,
	"voice" INTEGER DEFAULT 0,
	PRIMARY KEY ("nickname", "thread")
);

CREATE INDEX IF NOT EXISTS votes_user_idx
	ON "votes" ("nickname");

CREATE INDEX IF NOT EXISTS votes_thread_idx
	ON "votes" ("thread");

CREATE TABLE IF NOT EXISTS "posts" (
	"id" SERIAL PRIMARY KEY,
	"message" TEXT,
	"author" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE,
	"forum" CITEXT NOT NULL REFERENCES "forums" ("slug"),
	"thread" INTEGER REFERENCES "threads" ("id") ON DELETE CASCADE,
	"parent" INTEGER DEFAULT NULL REFERENCES "posts" ("id"),
	"created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"isEdited" BOOLEAN DEFAULT FALSE,
	"path" INT[] NOT NULL,
	"root_id" INTEGER DEFAULT NULL REFERENCES "posts" ("id")
);

CREATE INDEX IF NOT EXISTS posts_root_idx
	ON "posts" ("root_id");

CREATE INDEX IF NOT EXISTS posts_author_idx
	ON "posts" ("author");

CREATE INDEX IF NOT EXISTS posts_forum_idx
	ON "posts" ("forum");

CREATE INDEX IF NOT EXISTS posts_thread_idx
	ON "posts" ("thread");

CREATE INDEX IF NOT EXISTS posts_parent_idx
	ON "posts" ("parent");

CREATE INDEX IF NOT EXISTS posts_path_idx
	ON "posts" ("path");


CREATE TABLE IF NOT EXISTS "forum_users" (
	"nickname" CITEXT COLLATE ucs_basic NOT NULL REFERENCES "users" ("nickname") ON DELETE CASCADE,
	"forum" CITEXT NOT NULL REFERENCES "forums" ("slug"),
	PRIMARY KEY ("nickname", "forum")
);

CREATE INDEX IF NOT EXISTS forum_users_user_idx
	ON "forum_users" ("nickname");

CREATE INDEX IF NOT EXISTS forum_users_forum_idx
	ON "forum_users" ("forum");


CREATE OR REPLACE FUNCTION update_or_insert_votes(u CITEXT, t_id INTEGER, v INTEGER)
RETURNS VOID AS '
DECLARE
	count INTEGER;
BEGIN
	SELECT COUNT(*)
	FROM votes
	WHERE nickname = u AND thread = t_id
	INTO count;
	IF count > 0
	THEN
		UPDATE votes
		SET voice = v
		WHERE nickname = u AND thread = t_id;
	ELSE
		INSERT INTO votes (nickname, thread, voice) VALUES (u, t_id, v);
	END IF;
	UPDATE threads
	SET votes = (
		SELECT SUM(voice) FROM votes
		WHERE thread = t_id)
	WHERE id = t_id;
END;
' LANGUAGE plpgsql