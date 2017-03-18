WITH RECURSIVE recursetree (id, message, author, forum, thread, parent, created, isEdited, path) AS (
    (SELECT posts.*, array_append('{}'::int[], id) FROM posts
    WHERE parent IS NULL
    ORDER BY id DESC
    LIMIT 3)
  UNION ALL
    SELECT t.*, array_append(path, t.id)
    FROM posts t
    JOIN recursetree rt ON rt.id = t.parent
  )
SELECT rt.id, array_to_string(path, '.') as path1 FROM recursetree AS rt
ORDER BY path;



SELECT * FROM (
				(SELECT "author" FROM "threads"
				WHERE "forum" = 't26mvnA34_e'
				UNION
				SELECT "author" FROM "posts"
				WHERE "forum" = 't26mvnA34_e')
			) AS "a"
			JOIN "users" 
				ON "users"."nickname" = "a"."author"
			WHERE "a"."author" <= 'infinity'
			ORDER BY "author" DESC
			LIMIT 100