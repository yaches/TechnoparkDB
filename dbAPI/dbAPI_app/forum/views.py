import json
import time
import pytz
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

from dbAPI_app.helpers.helpers import *
from dbAPI_app.queries.forums import *
from dbAPI_app.queries.users import *
from dbAPI_app.queries.threads import *

@csrf_exempt
def create(request):
	params = json.loads(request.body)
	cursor = connection.cursor()

	cursor.execute(SELECT_FORUM_BY_SLUG, [params['slug']])	
	if cursor.rowcount > 0:
		forum = dictfetchall(cursor)[0]
		cursor.close()
		return JsonResponse(forum, status = 409)

	try:
		cursor.execute(CREATE_FORUM, [
			params['slug'], params['title'], params['user']
		])
	except:
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.execute(SELECT_USER_BY_NICKNAME, [params['user']])
	nickname = dictfetchall(cursor)[0]['nickname']
	params['user'] = nickname

	cursor.close()
	return JsonResponse(params, status = 201)


@csrf_exempt
def details(request, slug):
	cursor = connection.cursor()
	cursor.execute(SELECT_FORUM_BY_SLUG, [slug])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	forum = dictfetchall(cursor)[0]

	cursor.execute(SELECT_USER_BY_NICKNAME, [forum['user']])
	nickname = dictfetchall(cursor)[0]['nickname']
	forum['user'] = nickname

	cursor.close()
	return JsonResponse(forum, status = 200)


@csrf_exempt
def create_thread(request, slug):
	params = json.loads(request.body)
	author = params['author']
	message = params['message']
	title = params['title']
	created = params['created'] if 'created' in params else None
	thread_slug = params['slug'] if 'slug' in params else None
	votes = params['votes'] if 'votes' in params else None

	cursor = connection.cursor()

	cursor.execute(SELECT_THREAD_BY_SLUG, [thread_slug])
	if cursor.rowcount > 0:
		thread = dictfetchall(cursor)[0]
		cursor.close()
		return JsonResponse(thread, status = 409)

	try:
		cursor.execute(CREATE_THREAD, [
			thread_slug, title, message, author, created, slug
		])
	except:
		cursor.close()
		return JsonResponse({}, status = 404)

	thread_id = dictfetchall(cursor)[0]['id']
	params['id'] = thread_id

	cursor.close()
	return JsonResponse(params, status = 201)


@csrf_exempt
def get_threads(request, slug):
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

	cursor = connection.cursor()
	cursor.execute(SELECT_FORUM_BY_SLUG, [slug])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	cursor.execute(query, args)
	threads = dictfetchall(cursor)
	
	for thread in threads:
		zone = pytz.timezone('Europe/Moscow')
		thread['created'] = thread['created'].astimezone(zone)

	cursor.close()
	return JsonResponse(threads, status = 200, safe = False)