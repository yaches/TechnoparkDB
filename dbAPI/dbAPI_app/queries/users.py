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

# SELECT_USERS_BY_FORUM_WHERE = u''' 
# 			SELECT u."about", u."email", u."fullname", u."nickname" 
# 			FROM "users" AS u 
# 			WHERE u."nickname" IN (
# 				SELECT "nickname"
# 				FROM "forum_users"
# 				WHERE "forum" = %s
# 			) AND u."nickname" > %s
# 			ORDER BY u."nickname"
# '''

# SELECT_USERS_BY_FORUM_WHERE_DESC = u''' 
# 			SELECT u."about", u."email", u."fullname", u."nickname" 
# 			FROM "users" AS u 
# 			WHERE u."nickname" IN (
# 				SELECT "nickname"
# 				FROM "forum_users"
# 				WHERE "forum" = %s
# 			) AND u."nickname" < %s
# 			ORDER BY u."nickname" DESC
# '''

# SELECT_USERS_BY_FORUM = u''' 
# 			SELECT u."about", u."email", u."fullname", u."nickname" 
# 			FROM "users" AS u 
# 			WHERE u."nickname" IN (
# 				SELECT "nickname"
# 				FROM "forum_users"
# 				WHERE "forum" = %s
# 			)
# 			ORDER BY u."nickname"
# '''

# SELECT_USERS_BY_FORUM_DESC = u''' 
# 			SELECT u."about", u."email", u."fullname", u."nickname" 
# 			FROM "users" AS u 
# 			WHERE u."nickname" IN (
# 				SELECT "nickname"
# 				FROM "forum_users"
# 				WHERE "forum" = %s
# 			)
# 			ORDER BY u."nickname" DESC
# '''

SELECT_USERS_BY_FORUM_WHERE = u''' 
			SELECT u."nickname", "email", "fullname", "about" 
			FROM "forum_users" AS fu
			JOIN "users" AS u ON u."nickname" = fu."nickname"
			WHERE "forum" = %s AND u."nickname" > %s
			ORDER BY u."nickname"
'''

SELECT_USERS_BY_FORUM_WHERE_DESC = u''' 
			SELECT u."nickname", "email", "fullname", "about" 
			FROM "forum_users" AS fu
			JOIN "users" AS u ON u."nickname" = fu."nickname"
			WHERE "forum" = %s AND u."nickname" < %s
			ORDER BY u."nickname" DESC
'''

SELECT_USERS_BY_FORUM = u''' 
			SELECT u."nickname", "email", "fullname", "about" 
			FROM "forum_users" AS fu
			JOIN "users" AS u ON u."nickname" = fu."nickname"
			WHERE "forum" = %s
			ORDER BY u."nickname"
'''

SELECT_USERS_BY_FORUM_DESC = u''' 
			SELECT u."nickname", "email", "fullname", "about" 
			FROM "forum_users" AS fu
			JOIN "users" AS u ON u."nickname" = fu."nickname"
			WHERE "forum" = %s
			ORDER BY u."nickname" DESC
'''

ADD_FORUM_USER = u''' 
			INSERT INTO "forum_users"
			("nickname", "forum") 
			VALUES (%s, %s)
'''