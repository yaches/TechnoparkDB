CREATE_POST = u'''
			INSERT INTO "posts"
			("message", "author", "forum", "thread", "created", "parent", "isEdited")
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			RETURNING "id"
		'''

SELECT_POSTS_BY_THREAD_ID = u'''
			SELECT * FROM "posts"
			WHERE "thread" = %s
			ORDER BY "created"
		'''

SELECT_POSTS_BY_THREAD_SLUG = u'''
			SELECT * FROM "posts"
			WHERE "thread" = (
				SELECT "id" FROM "threads"
				WHERE "slug" = %s
			) ORDER BY "created"
		'''