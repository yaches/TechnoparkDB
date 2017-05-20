# coding=utf-8

CREATE_FORUM = u''' 
			INSERT INTO "forums"
			("slug", "title", "user", "posts", "threads")
			VALUES
			(%s, %s, (SELECT "nickname" FROM "users" WHERE "nickname" = %s), %s, %s)
			RETURNING "user"
		'''

SELECT_FORUM_BY_SLUG = u''' 
			SELECT * FROM "forums"
			WHERE "slug" = %s
		'''

INCREASE_FORUM_THREADS = u'''
			UPDATE "forums"
			SET "threads" = "threads" + %s
			WHERE "slug" = %s
		'''

INCREASE_FORUM_POSTS = u'''
			UPDATE "forums"
			SET "posts" = "posts" + %s
			WHERE "slug" = %s
		'''