SELECT_DATA_AMOUNT = u'''
			SELECT * FROM 
				(SELECT COUNT(*) AS "forum" FROM "forums") AS "f",
				(SELECT COUNT(*) AS "thread" FROM "threads") AS "t",
				(SELECT COUNT(*) AS "post" FROM "posts") AS "p",
				(SELECT COUNT(*) AS "user" FROM "users") AS "u"
		'''

CLEAR_VOTES = u'''
			DELETE FROM "votes"
		'''

CLEAR_POSTS = u'''
			DELETE FROM "posts"
		'''

CLEAR_THREADS = u'''
			DELETE FROM "threads"
		'''

CLEAR_FORUMS = u'''
			DELETE FROM "forums"
		'''

CLEAR_USERS = u'''
			DELETE FROM "users"
		'''