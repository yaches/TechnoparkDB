import json, time, datetime, pytz

import psycopg2
from psycopg2.extras import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError
from django.utils import timezone

from dbAPI_app.helpers.helpers import *
from dbAPI_app.helpers.db import *
from dbAPI_app.queries.forums import *
from dbAPI_app.queries.users import *
from dbAPI_app.queries.threads import *
from dbAPI_app.queries.posts import *
from dbAPI_app.queries.common import *


@csrf_exempt
def id_create(request, id, **kwargs):
	params = json.loads(request.body.decode("utf-8"))
	conn = connectFromPool()
	cursor = conn.cursor()

	try:
		id = int(id)
	except:
		pass

	if type(id) == int:
		cursor.execute(CHECK_THREAD_BY_ID, [id])
	else:
		cursor.execute(CHECK_THREAD_BY_SLUG, [id])

	if cursor.rowcount == 0:
		cursor.close();
		return JsonResponse({}, status = 404)
	else:
		thread = dictfetchall(cursor)[0]
		id = thread['id']

	all_created = curtime()
	adding_posts = len(params)	

	parents = []
	values = []
	author_nicknames = set()
	counter = 0
	check_query = 'SELECT "id" FROM "posts" WHERE "thread" = %s AND (' % id
	
	for post in params:

		post_values = []

		post['created'] = post['created'] if 'created' in post else all_created
		post['forum'] = thread['forum']
		post['thread'] = id
		post['parent'] = post['parent'] if 'parent' in post else None
		post['isEdited'] = post['isEdited'] if 'isEdited' in post else None

		cursor.execute('''SELECT NEXTVAL('posts_id_seq')''')
		post['id'] = dictfetchall(cursor)[0]['nextval']

		post_values.append(post['id'])
		post_values.append(post['message'])
		post_values.append(post['author'])
		post_values.append(post['forum'])
		post_values.append(post['thread'])
		post_values.append(post['created'])
		post_values.append(post['parent'])
		post_values.append(post['isEdited'])

		author_nicknames.add(post['author'])

		values.append(post_values)

		if post['parent'] is not None:
			parent = int(post['parent'])
			if not parent in parents:
				parents.append(parent)
				check_query += '"id" = %s OR '
				counter += 1

	check_query += '0 = 0)'
	
	cursor.execute(check_query, parents)
	if cursor.rowcount < counter:
		cursor.close()
		return JsonResponse({}, status = 409)

	formatQuery = postgreQueryFormat(CREATE_POST)
	try:
		cursor.execute("PREPARE posts_insert_plan AS " + formatQuery)
	except psycopg2.Error as e:
		pass

	try:
		execute_batch(cursor, "EXECUTE posts_insert_plan (%s, %s, %s, %s, %s, %s, %s, %s)", values)
	except psycopg2.Error as e:
		print(e.pgcode)
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.execute(INCREASE_FORUM_POSTS, [adding_posts, thread['forum']])

	author_nicknames = list(author_nicknames)
	author_nicknames.sort()
	author_nicknames_values = []
	for author in author_nicknames:
		author_nicknames_values.append([author, thread['forum']])

	try:
		cursor.execute("PREPARE forum_users_insert_plan AS " + postgreQueryFormat(ADD_FORUM_USER))
	except psycopg2.Error as e:
		pass

	try:
		execute_batch(cursor, "EXECUTE forum_users_insert_plan (%s, %s)", author_nicknames_values)
	except psycopg2.Error as e:
		print(e.pgcode)

	cursor.close()
	return JsonResponse(params, status = 201, safe = False)


@csrf_exempt
def slug_create(request, slug):
	return id_create(request, slug)


@csrf_exempt
def id_vote(request, id):
	params = json.loads(request.body.decode("utf-8"))
	voice = params['voice']
	nickname = params['nickname']
	conn = connectFromPool()
	cursor = conn.cursor()

	try:
		cursor.execute('SELECT update_or_insert_votes(CAST(%s AS CITEXT), %s, %s)', [nickname, id, voice])
	except psycopg2.Error as e:
		# print(e)
		print(e.pgcode)
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.execute(SELECT_THREAD_BY_ID, [id])
	thread = dictfetchall(cursor)[0]
	thread['created'] = localtime(thread['created'])

	cursor.close()
	return JsonResponse(thread, status = 200)


@csrf_exempt
def slug_vote(request, slug):
	conn = connectFromPool()
	cursor = conn.cursor()
	cursor.execute(SELECT_THREAD_BY_SLUG, [slug])
	if cursor.rowcount > 0:
		thread = dictfetchall(cursor)[0]
		cursor.close()
		return id_vote(request, thread['id'])
	else:
		cursor.close()
		return JsonResponse({}, status = 404)


@csrf_exempt
def id_details(request, id):
	return details(request, SELECT_THREAD_BY_ID, id)


@csrf_exempt
def slug_details(request, slug):
	return details(request, SELECT_THREAD_BY_SLUG, slug)


@csrf_exempt
def details(request,  query, identifier):
	conn = connectFromPool()
	cursor = conn.cursor()
	cursor.execute(query, [identifier])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	thread = dictfetchall(cursor)[0]
	thread['created'] = localtime(thread['created'])

	if request.method == 'POST':
		params = json.loads(request.body.decode("utf-8"))
		message = params['message'] if 'message' in params else thread['message']
		title = params['title'] if 'title' in params else thread['title']

		cursor.execute(UPDATE_THREAD, [
			title, message, thread['id']
		])

		thread['title'] = title
		thread['message'] = message

	cursor.close()
	return JsonResponse(thread, status = 200)


@csrf_exempt
def id_posts(request, id):
	sort = request.GET.get('sort', 'flat')
	desc = request.GET.get('desc', 'false')

	if sort == 'tree':
		query = SELECT_POSTS_BY_THREAD_ID_TREE
	elif sort == 'parent_tree':
		query = SELECT_POSTS_BY_THREAD_ID_PARENT_TREE
	else:
		if desc == 'false':
			query = SELECT_POSTS_BY_THREAD_ID
		else:
			query = SELECT_POSTS_BY_THREAD_ID_DESC

	return posts(request, SELECT_THREAD_BY_ID, query, id)


@csrf_exempt
def slug_posts(request, slug):
	sort = request.GET.get('sort', 'flat')
	desc = request.GET.get('desc', 'false')

	if sort == 'tree':
		query = SELECT_POSTS_BY_THREAD_SLUG_TREE
	elif sort == 'parent_tree':
		query = SELECT_POSTS_BY_THREAD_SLUG_PARENT_TREE
	else:
		if desc == 'false':	
			query = SELECT_POSTS_BY_THREAD_SLUG
		else:
			query = SELECT_POSTS_BY_THREAD_SLUG_DESC

	return posts(request, SELECT_THREAD_BY_SLUG, query, slug)


@csrf_exempt
def posts(request, check_query, query, identifier):
	limit = int(request.GET.get('limit', False))
	marker = request.GET.get('marker', False)
	desc = request.GET.get('desc', False)
	desc = True if desc == 'true' else False
	sort = request.GET.get('sort', 'flat')

	args = [identifier]

	if sort == 'parent_tree':
		if desc:
			desc_query = 'DESC'
			query += WITH_DESC
		else:
			desc_query = 'ASC'

		if limit:
			limit_query = '\'' + str(limit) + '\''
		else:
			limit_query = 'ALL'
	else:
		if desc and sort == 'tree':
			query += WITH_DESC

		if limit:
			query += WITH_LIMIT
			args.append(limit)

	page = 0
	if marker:
		try:
			page = marking.m[marker]
		except:
			pass

	if sort == 'parent_tree':
		offset_query = '\'' + str(page) + '\''
	else:
		query += WITH_OFFSET
		args.append(page)

	conn = connectFromPool()
	cursor = conn.cursor()
	cursor.execute(check_query, [identifier])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	if sort == 'parent_tree':
		query = query % (desc_query, limit_query, offset_query)
		args = [identifier]

	cursor.execute(query, args)

	if limit:
		page += limit
	else:
		page += cursor.rowcount

	new_marker = marking(page)

	if cursor.rowcount == 0:
		page = 0
		new_marker = marker

	all_posts = dictfetchall(cursor)
	for post in all_posts:
		post['created'] = localtime(post['created'])

	response = {'marker': new_marker, 'posts': all_posts}

	cursor.close()
	return JsonResponse(response, status = 200)