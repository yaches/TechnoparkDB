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

