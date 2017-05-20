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
			SELECT "threads".*, SUM("voice") AS "votes" FROM "threads"
			LEFT JOIN "votes" ON "votes"."thread" = "threads"."id"
			WHERE "slug" = %s
			GROUP BY "id"
		'''

SELECT_THREAD_BY_ID = u'''
			SELECT "threads".*, SUM("voice") AS "votes" FROM "threads"
			LEFT JOIN "votes" ON "votes"."thread" = "threads"."id"
			WHERE "id" = %s
			GROUP BY "id"
		'''

# SELECT_THREAD_BY_SLUG = u'''
# 			SELECT * FROM "threads"
# 			WHERE "slug" = %s
# 			GROUP BY "id"
# 		'''

# SELECT_THREAD_BY_ID = u'''
# 			SELECT * FROM "threads"
# 			WHERE "id" = %s
# 			GROUP BY "id"
# 		'''

SELECT_THREADS_BY_FORUM = u'''
			SELECT "threads".*, SUM("voice") AS "votes" FROM "threads"
			LEFT JOIN "votes" ON "votes"."thread" = "threads"."id"
			WHERE "forum" = %s AND created >= %s
			GROUP BY "id"
			ORDER BY "created"
		'''

SELECT_THREADS_BY_FORUM_DESC = u'''
			SELECT "threads".*, SUM("voice") AS "votes" FROM "threads"
			LEFT JOIN "votes" ON "votes"."thread" = "threads"."id"
			WHERE "forum" = %s AND created <= %s
			GROUP BY "id"
			ORDER BY "created" DESC
		'''

CREATE_VOTE = u'''
			INSERT INTO "votes"
			("nickname", "thread", "voice")
			VALUES
			(%s, %s, %s)
		'''

UPDATE_VOTE = u'''
			UPDATE "votes"
			SET "voice" = %s
			WHERE "nickname" = %s AND "thread" = %s
		'''

SELECT_VOTE = u'''
			SELECT * FROM "votes"
			WHERE "nickname" = %s AND "thread" = %s
		'''