SELECT_DATA_AMOUNT = u'''
			SELECT * FROM 
				(SELECT COUNT(*) AS "forum" FROM "forums") AS "f",
				(SELECT COUNT(*) AS "thread" FROM "threads") AS "t",
				(SELECT COUNT(*) AS "post" FROM "posts") AS "p",
				(SELECT COUNT(*) AS "user" FROM "users") AS "u"
		'''