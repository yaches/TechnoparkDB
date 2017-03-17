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

SELECT_POSTS_BY_THREAD_ID_TREE = u'''
			WITH RECURSIVE recursetree (id, message, author, forum, thread, parent, created, isEdited, path) AS (
					SELECT posts.*, array_append('{}'::int[], id) FROM posts
					WHERE parent IS NULL
				UNION ALL
					SELECT p.*, array_append(path, p.id)
					FROM posts AS p
					JOIN recursetree rt ON rt.id = p.parent
			)
			SELECT rt.*, array_to_string(path, '.') as path1 
			FROM recursetree AS rt
			WHERE rt."thread" = %s
			ORDER BY path
		'''

SELECT_POSTS_BY_THREAD_SLUG_TREE = u'''
			WITH RECURSIVE recursetree (id, message, author, forum, thread, parent, created, isEdited, path) AS (
					SELECT posts.*, array_append('{}'::int[], id) FROM posts
					WHERE parent IS NULL
				UNION ALL
					SELECT p.*, array_append(path, p.id)
					FROM posts AS p
					JOIN recursetree rt ON rt.id = p.parent
			)
			SELECT rt.*, array_to_string(path, '.') as path1 
			FROM recursetree AS rt
			WHERE rt."thread" = (
				SELECT "id" FROM "threads"
				WHERE "slug" = %s
			)
			ORDER BY path
		'''
