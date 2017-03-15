DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS users;

CREATE EXTENSION IF NOT EXISTS CITEXT;

CREATE TABLE IF NOT EXISTS users (
	nickname CITEXT COLLATE ucs_basic PRIMARY KEY,
	email CITEXT UNIQUE,
	fullname TEXT,
	about TEXT
);

CREATE TABLE IF NOT EXISTS forums (
	slug CITEXT PRIMARY KEY NOT NULL,
	title TEXT NOT NULL,
	posts INTEGER DEFAULT 0,
	threads INTEGER DEFAULT 0,
	author CITEXT COLLATE ucs_basic NOT NULL REFERENCES users (nickname) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS threads (
	id SERIAL PRIMARY KEY,
	slug CITEXT UNIQUE,
	title TEXT NOT NULL,
	message TEXT,
	author CITEXT COLLATE ucs_basic NOT NULL REFERENCES users (nickname) ON DELETE CASCADE,
	created TIMESTAMP,
	forum CITEXT NOT NULL REFERENCES forums (slug) ON DELETE CASCADE,
	votes INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS votes (
	nickname CITEXT COLLATE ucs_basic NOT NULL REFERENCES users (nickname) ON DELETE CASCADE,
	voice INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS posts (
	id SERIAL PRIMARY KEY,
	message TEXT,
	author CITEXT COLLATE ucs_basic NOT NULL REFERENCES users (nickname) ON DELETE CASCADE,
	forum CITEXT NOT NULL REFERENCES forums (slug),
	thread INTEGER REFERENCES threads (id) ON DELETE CASCADE,
	parent INTEGER DEFAULT 0,
	created TIMESTAMP,
	isEdited BOOLEAN DEFAULT FALSE
);