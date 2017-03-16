CREATE_THREAD = u'''
			INSERT INTO "threads"
			("slug", "title", "message", "author", "created", "forum")
			VALUES
			(%s, %s, %s, %s, %s, %s)
			RETURNING "id"
		'''

SELECT_THREAD_BY_SLUG = u'''
			SELECT * FROM "threads"
			WHERE "slug" = %s
		'''

SELECT_THREAD_BY_ID = u'''
			SELECT * FROM "threads"
			WHERE "id" = %s
		'''

SELECT_THREADS_BY_FORUM = u'''
			SELECT * FROM "threads"
			WHERE "forum" = %s AND created >= %s
			ORDER BY "created"
		'''

SELECT_THREADS_BY_FORUM_DESC = u'''
			SELECT * FROM "threads"
			WHERE "forum" = %s AND created <= %s
			ORDER BY "created" DESC
		'''

WITH_LIMIT = u'''
			LIMIT %s
		'''