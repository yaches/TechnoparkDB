# coding=utf-8

SELECT_USER_BY_EMAIL = u''' 
			SELECT * FROM "users"
			WHERE "email" = %s
		'''

SELECT_USER_BY_NICKNAME = u'''
			SELECT * FROM "users"
			WHERE "nickname" = %s
		'''

CHECK_USERS_EXIST = u'''
			SELECT * FROM "users"
			WHERE "nickname" = %s 
			OR "email" = %s
		'''

CREATE_USER = u'''
			INSERT INTO "users"
			("nickname", "email", "fullname", "about")
			VALUES
			(%s, %s, %s, %s)
		'''

UPDATE_USER = u''' 
			UPDATE "users"
			SET "email" = %s, "fullname" = %s, "about" = %s
			WHERE "nickname" = %s
		'''

SELECT_USERS_BY_FORUM_WHERE = u'''
			SELECT * FROM (
				(SELECT "author" FROM "threads"
				WHERE "forum" = %s
				UNION
				SELECT "author" FROM "posts"
				WHERE "forum" = %s)
			) AS "a"
			JOIN "users" 
				ON "users"."nickname" = "a"."author"
			WHERE "a"."author" > %s
			ORDER BY "author"
		'''

SELECT_USERS_BY_FORUM_WHERE_DESC = u'''
			SELECT * FROM (
				(SELECT "author" FROM "threads"
				WHERE "forum" = %s
				UNION
				SELECT "author" FROM "posts"
				WHERE "forum" = %s)
			) AS "a"
			JOIN "users" 
				ON "users"."nickname" = "a"."author"
			WHERE "a"."author" < %s
			ORDER BY "author" DESC
		'''

SELECT_USERS_BY_FORUM = u'''
			SELECT * FROM (
				(SELECT "author" FROM "threads"
				WHERE "forum" = %s
				UNION
				SELECT "author" FROM "posts"
				WHERE "forum" = %s)
			) AS "a"
			JOIN "users" 
				ON "users"."nickname" = "a"."author"
			ORDER BY "author"
		'''

SELECT_USERS_BY_FORUM_DESC = u'''
			SELECT * FROM (
				(SELECT "author" FROM "threads"
				WHERE "forum" = %s
				UNION
				SELECT "author" FROM "posts"
				WHERE "forum" = %s)
			) AS "a"
			JOIN "users" 
				ON "users"."nickname" = "a"."author"
			ORDER BY "author" DESC
		'''
