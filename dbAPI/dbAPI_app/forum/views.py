import json
import time
import pytz

import psycopg2

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

from dbAPI_app.helpers.helpers import *
from dbAPI_app.helpers.db import *
from dbAPI_app.queries.forums import *
from dbAPI_app.queries.users import *
from dbAPI_app.queries.threads import *
from dbAPI_app.queries.common import *

@csrf_exempt
def create(request):
	# print(request.path)

	params = json.loads(request.body.decode("utf-8"))
	slug = params['slug']
	title = params['title']
	user = params['user']
	posts = params['posts'] if 'posts' in params else 0
	threads = params['threads'] if 'threads' in params else 0

	conn = connectFromPool()
	cursor = conn.cursor()

	cursor.execute(SELECT_USER_BY_NICKNAME, [user])
	if cursor.rowcount > 0:
		profile = dictfetchall(cursor)[0]
		user = params['user'] = profile['nickname']

	cursor.execute(SELECT_FORUM_BY_SLUG, [slug])	
	if cursor.rowcount > 0:
		forum = dictfetchall(cursor)[0]
		cursor.close()
		return JsonResponse(forum, status = 409)

	try:
		cursor.execute(CREATE_FORUM, [
			slug, title, user, posts, threads
		])
	except psycopg2.IntegrityError:
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.close()
	return JsonResponse(params, status = 201)


@csrf_exempt
def details(request, slug):
	# print(request.path)

	conn = connectFromPool()
	cursor = conn.cursor()
	cursor.execute(SELECT_FORUM_BY_SLUG, [slug])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	forum = dictfetchall(cursor)[0]

	cursor.close()
	return JsonResponse(forum, status = 200)


@csrf_exempt
def create_thread(request, slug):
	# print(request.path)

	params = json.loads(request.body.decode("utf-8"))
	author = params['author']
	message = params['message']
	title = params['title']
	created = params['created'] if 'created' in params else curtime()
	thread_slug = params['slug'] if 'slug' in params else None

	conn = connectFromPool()
	cursor = conn.cursor()

	cursor.execute(SELECT_FORUM_BY_SLUG, [slug])
	if cursor.rowcount > 0:
		forum = dictfetchall(cursor)[0]
		slug = params['forum'] = forum['slug']
	else:
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.execute(SELECT_THREAD_BY_SLUG, [thread_slug])
	if cursor.rowcount > 0:
		thread = dictfetchall(cursor)[0]
		thread['created'] = localtime(thread['created'])
		cursor.close()
		return JsonResponse(thread, status = 409)

	try:
		cursor.execute(CREATE_THREAD, [
			title, message, author, slug, created, thread_slug
		])
	except psycopg2.Error as e:
		# print(e)
		# print(e.pgcode)
		cursor.close()
		return JsonResponse({}, status = 404)

	thread_id = dictfetchall(cursor)[0]['id']
	params['id'] = thread_id
	params['forum'] = slug

	cursor.execute(INCREASE_FORUM_THREADS, [1, slug])

	try:
		cursor.execute(ADD_FORUM_USER, [author, slug])
	except psycopg2.Error as e:
		# print(e)
		# print(e.pgcode)
		pass

	cursor.close()
	return JsonResponse(params, status = 201)


@csrf_exempt
def get_threads(request, slug):
	# print(request.path)

	limit = request.GET.get('limit', False)
	since = request.GET.get('since', False)
	desc = request.GET.get('desc', False)
	desc = True if desc == 'true' else False

	args = [slug]

	if desc:
		query = SELECT_THREADS_BY_FORUM_DESC
		since_arg = 'infinity'
	else:
		query = SELECT_THREADS_BY_FORUM
		since_arg = 'epoch'

	if since:
		args.append(since)
	else:
		args.append(since_arg)

	if limit:
		query += WITH_LIMIT
		args.append(limit)

	conn = connectFromPool()
	cursor = conn.cursor()
	cursor.execute(SELECT_FORUM_BY_SLUG, [slug])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.execute(query, args)
	threads = dictfetchall(cursor)
	
	for thread in threads:
		thread['created'] = localtime(thread['created'])

	cursor.close()
	return JsonResponse(threads, status = 200, safe = False)


@csrf_exempt
def get_users(request, slug):
	# print(request.path)
	
	limit = request.GET.get('limit', False)
	since = request.GET.get('since', False)
	desc = request.GET.get('desc', False)
	desc = True if desc == 'true' else False

	args = [slug]

	if since:
		args.append(since)
		if desc:
			query = SELECT_USERS_BY_FORUM_WHERE_DESC
		else:
			query = SELECT_USERS_BY_FORUM_WHERE
	else:
		if desc:
			query = SELECT_USERS_BY_FORUM_DESC
		else:
			query = SELECT_USERS_BY_FORUM

	if limit:
		query += WITH_LIMIT
		args.append(limit)

	conn = connectFromPool()
	cursor = conn.cursor()
	cursor.execute(SELECT_FORUM_BY_SLUG, [slug])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.execute(query, args)
	users = dictfetchall(cursor)

	# print(users)
	
	cursor.close()
	return JsonResponse(users, status = 200, safe = False)
