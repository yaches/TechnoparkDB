CREATE_POST = u'''
			INSERT INTO "posts"
			("message", "author", "forum", "thread", "created", "parent", "isEdited")
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			RETURNING "id"
		'''

POST_UPDATE_MESSAGE = u'''
			UPDATE "posts" 
			SET "message" = %s, "isEdited" = TRUE
			WHERE "id" = %s
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

SELECT_POSTS_BY_THREAD_ID_TREE = u'''
			WITH RECURSIVE recursetree (id, message, author, forum, thread, parent, created, isEdited, path) AS (
					SELECT posts.*, array_append('{}'::int[], id) FROM posts
					WHERE parent IS NULL
						AND "thread" = %s
				UNION ALL
					SELECT p.*, array_append(path, p.id)
					FROM posts AS p
					JOIN recursetree rt ON rt.id = p.parent
			)
			SELECT rt.*, array_to_string(path, '.') as path1 
			FROM recursetree AS rt
			ORDER BY path
		'''

SELECT_POSTS_BY_THREAD_SLUG_TREE = u'''
			WITH RECURSIVE recursetree (id, message, author, forum, thread, parent, created, isEdited, path) AS (
					SELECT posts.*, array_append('{}'::int[], id) FROM posts
					WHERE parent IS NULL
						AND "thread" = (
							SELECT "id" FROM "threads"
							WHERE "slug" = %s
						)
				UNION ALL
					SELECT p.*, array_append(path, p.id)
					FROM posts AS p
					JOIN recursetree rt ON rt.id = p.parent
			)
			SELECT rt.*, array_to_string(path, '.') as path1 
			FROM recursetree AS rt
			ORDER BY path
		'''

SELECT_POSTS_BY_THREAD_ID_PARENT_TREE = u'''
			WITH RECURSIVE recursetree (id, message, author, forum, thread, parent, created, isEdited, path) AS (
					(SELECT posts.*, array_append('{}'::int[], id) FROM posts
					WHERE parent IS NULL
						AND "thread" = %%s
					ORDER BY "id" %s
					LIMIT %s OFFSET %s)
				UNION ALL
					SELECT p.*, array_append(path, p.id)
					FROM posts AS p
					JOIN recursetree rt ON rt.id = p.parent
			)
			SELECT rt.*, array_to_string(path, '.') as path1 
			FROM recursetree AS rt
			ORDER BY path
		'''

SELECT_POSTS_BY_THREAD_SLUG_PARENT_TREE = u'''
			WITH RECURSIVE recursetree (id, message, author, forum, thread, parent, created, isEdited, path) AS (
					(SELECT posts.*, array_append('{}'::int[], id) FROM posts
					WHERE parent IS NULL AND
					"thread" = (
						SELECT "id" FROM "threads"
						WHERE "slug" = %%s
					)
					ORDER BY "id" %s
					LIMIT %s OFFSET %s)
				UNION ALL
					SELECT p.*, array_append(path, p.id)
					FROM posts AS p
					JOIN recursetree rt ON rt.id = p.parent
			)
			SELECT rt.*, array_to_string(path, '.') as path1 
			FROM recursetree AS rt
			ORDER BY path
		'''

SELECT_POST_BY_ID = u'''
			SELECT * FROM "posts" AS p
			WHERE "id" = %s
		'''

# WHERE_ID = u'''
# 			WHERE "id" = %s
# 		'''

# JOIN_USERS = u'''
# 			JOIN "users" AS u ON p."author" = u."nickname"
# 		'''

# JOIN_THREADS = u'''
# 			JOIN "threads" AS t ON p."thread" = t."id"
# 		'''

# JOIN_FORUMS = u'''
# 			JOIN "forums" AS f ON p."forum" = f."slug"