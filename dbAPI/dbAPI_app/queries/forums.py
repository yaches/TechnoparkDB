# coding=utf-8

CREATE_FORUM = u''' 
			INSERT INTO "forums"
			("slug", "title", "user", "posts", "threads")
			VALUES
			(%s, %s, %s, %s, %s)
		'''

SELECT_FORUM_BY_SLUG = u''' 
			SELECT * FROM "forums"
			WHERE "slug" = %s
		'''