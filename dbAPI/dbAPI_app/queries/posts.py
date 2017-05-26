CREATE_POST = u'''INSERT INTO "posts"
			("id", "message", "author", "forum", "thread", "created", "parent", "isEdited", "path", "root_id")
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		'''

POST_UPDATE_MESSAGE = u'''
			UPDATE "posts" 
			SET "message" = %s, "isEdited" = TRUE
			WHERE "id" = %s
		'''

SELECT_POSTS_BY_THREAD_ID = u'''
			SELECT * FROM "posts"
			WHERE "thread" = %s
			ORDER BY "created", "id"
		'''

SELECT_POSTS_BY_THREAD_ID_DESC = u'''
			SELECT * FROM "posts"
			WHERE "thread" = %s
			ORDER BY "created" DESC, "id" DESC
		'''

SELECT_POSTS_BY_THREAD_SLUG = u'''
			SELECT * FROM "posts"
			WHERE "thread" = (
				SELECT "id" FROM "threads"
				WHERE "slug" = %s
			) ORDER BY "created", "id"
		'''

SELECT_POSTS_BY_THREAD_SLUG_DESC = u'''
			SELECT * FROM "posts"
			WHERE "thread" = (
				SELECT "id" FROM "threads"
				WHERE "slug" = %s
			) ORDER BY "created" DESC, "id" DESC
		'''

SELECT_POSTS_BY_THREAD_ID_TREE = u''' 
			SELECT * FROM "posts"
			WHERE "thread" = %s
			ORDER BY path
'''

SELECT_POSTS_BY_THREAD_SLUG_TREE = u'''
			SELECT * FROM "posts"
			WHERE "thread" = (
				SELECT "id" FROM "threads"
				WHERE "slug" = %s)
			ORDER BY path
'''

SELECT_POSTS_BY_THREAD_ID_PARENT_TREE = u''' 
			SELECT * FROM "posts"
			WHERE "root_id" IN (
				SELECT "id" FROM "posts"
				WHERE "parent" IS NULL AND "thread" = %%s
				ORDER BY "id" %s
				LIMIT %s OFFSET %s
			)
			ORDER BY "path"
'''

SELECT_POSTS_BY_THREAD_SLUG_PARENT_TREE = u'''
			SELECT * FROM "posts"
			WHERE "root_id" IN (
				SELECT "id" FROM "posts"
				WHERE "parent" IS NULL AND "thread" = (
					SELECT "id" FROM "threads"
					WHERE "slug" = %%s
				)
				ORDER BY "id" %s
				LIMIT %s OFFSET %s
			)
			ORDER BY "path"
'''

SELECT_POST_BY_ID = u'''
			SELECT * FROM "posts" AS p
			WHERE "id" = %s
		'''

CHECK_POST_BY_ID = u''' 
			SELECT "id", "thread" FROM "posts"
			WHERE "id" = %s
			'''