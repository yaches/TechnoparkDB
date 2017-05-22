CREATE_THREAD = u'''
			INSERT INTO "threads"
			("title", "message", "author", "forum", "created", "slug")
			VALUES
			(%s, %s, %s, %s, %s, %s)
			RETURNING "id"
		'''

UPDATE_THREAD = u'''
			UPDATE "threads"
			SET "title" = %s, "message" = %s
			WHERE "id" = %s
		'''

SELECT_THREAD_BY_SLUG = u''' 
			SELECT * FROM "threads"
			WHERE "slug" = %s
'''

SELECT_THREAD_BY_ID = u''' 
			SELECT * FROM "threads"
			WHERE "id" = %s
'''

CHECK_THREAD_BY_SLUG = u'''
			SELECT id, forum FROM "threads"
			WHERE "slug" = %s
		'''

CHECK_THREAD_BY_ID = u'''
			SELECT id, forum FROM "threads"
			WHERE "id" = %s
		'''

SELECT_THREADS_BY_FORUM = u''' 
			SELECT * FROM "threads"
			WHERE "forum" = %s AND "created" >= %s
			ORDER BY "created"
'''

SELECT_THREADS_BY_FORUM_DESC = u''' 
			SELECT * FROM "threads"
			WHERE "forum" = %s AND "created" <= %s
			ORDER BY "created" DESC
'''
