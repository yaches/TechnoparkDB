import json, time, datetime, pytz

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

from dbAPI_app.helpers.helpers import *
from dbAPI_app.queries.forums import *
from dbAPI_app.queries.users import *
from dbAPI_app.queries.threads import *
from dbAPI_app.queries.posts import *
from dbAPI_app.queries.common import *

@csrf_exempt
def id_create(request, id, **kwargs):
	id = int(id)
	params = json.loads(request.body)
	cursor = connection.cursor()

	if 'thread' in kwargs:
		thread = kwargs['thread']
	else:
		cursor.execute(SELECT_THREAD_BY_ID, [id])
		if cursor.rowcount == 0:
			return JsonResponse({}, status = 404)
		else:
			thread = dictfetchall(cursor)[0]

	adding_posts = 0

	for post in params:
		author = post['author']
		message = post['message']
		created = post['created'] if 'created' in post else curtime()
		isEdited = post['isEdited'] if 'isEdited' in post else None
		parent = post['parent'] if 'parent' in post else None

		if parent is not None:
			cursor.execute(SELECT_POST_BY_ID, [parent])
			if cursor.rowcount > 0:
				parent_post = dictfetchall(cursor)[0]
				parent_thread = parent_post['thread']
				if parent_thread != id:
					try:
						cursor.execute(INCREASE_FORUM_POSTS, [adding_posts, params[0]['forum']])
					except:
						pass
					return JsonResponse({}, status = 409)
			else:
				try:
					cursor.execute(INCREASE_FORUM_POSTS, [adding_posts, params[0]['forum']])
				except:
					pass
				return JsonResponse({}, status = 409)

		try:
			cursor.execute(CREATE_POST, [
				message, author, thread['forum'], id, created, parent, isEdited
			])
		except IntegrityError:
			try:
				cursor.execute(INCREASE_FORUM_POSTS, [adding_posts, params[0]['forum']])
			except:
				pass
			return JsonResponse({}, status = 404)

		adding_posts += 1
		returning = dictfetchall(cursor)[0]
		post['id'] = returning['id']
		post['created'] = created
		post['forum'] = thread['forum']
		post['thread'] = id

	try:
		cursor.execute(INCREASE_FORUM_POSTS, [adding_posts, params[0]['forum']])
	except:
		pass

	cursor.close()
	return JsonResponse(params, status = 201, safe = False)


@csrf_exempt
def slug_create(request, slug):
	cursor = connection.cursor()
	cursor.execute(SELECT_THREAD_BY_SLUG, [slug])
	if cursor.rowcount == 0:
		return JsonResponse({}, status = 404)
	else:
		thread = dictfetchall(cursor)[0]
		id = thread['id']

		cursor.close()
		return id_create(request, id, thread = thread)


@csrf_exempt
def id_vote(request, id):
	params = json.loads(request.body)
	voice = params['voice']
	nickname = params['nickname']
	cursor = connection.cursor()

	cursor.execute(SELECT_VOTE, [nickname, id])
	if cursor.rowcount > 0:
		try:
			cursor.execute(UPDATE_VOTE, [voice, nickname, id])
		except:
			cursor.close()
			return JsonResponse({}, status = 404)
	else:
		try:
			cursor.execute(CREATE_VOTE, [nickname, id, voice])
		except IntegrityError:
			cursor.close()
			return JsonResponse({}, status = 404)

	cursor.execute(SELECT_THREAD_BY_ID, [id])
	thread = dictfetchall(cursor)[0]
	thread['created'] = localtime(thread['created'])

	cursor.close()
	return JsonResponse(thread, status = 200)


@csrf_exempt
def slug_vote(request, slug):
	cursor = connection.cursor()
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
	cursor = connection.cursor()
	cursor.execute(query, [identifier])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	thread = dictfetchall(cursor)[0]
	thread['created'] = localtime(thread['created'])

	if request.method == 'POST':
		params = json.loads(request.body)
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

	if sort == 'tree':
		query = SELECT_POSTS_BY_THREAD_ID_TREE
	elif sort == 'parent_tree':
		query = SELECT_POSTS_BY_THREAD_ID_PARENT_TREE
	else:
		query = SELECT_POSTS_BY_THREAD_ID

	return posts(request, SELECT_THREAD_BY_ID, query, id)


@csrf_exempt
def slug_posts(request, slug):
	sort = request.GET.get('sort', 'flat')

	if sort == 'tree':
		query = SELECT_POSTS_BY_THREAD_SLUG_TREE
	elif sort == 'parent_tree':
		query = SELECT_POSTS_BY_THREAD_SLUG_PARENT_TREE
	else:
		query = SELECT_POSTS_BY_THREAD_SLUG

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
		if desc:
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

	cursor = connection.cursor()
	cursor.execute(check_query, [identifier])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)

	if sort == 'parent_tree':
		query = query % (desc_query, limit_query, offset_query)
		args = [identifier]
		print(query)

	cursor.execute(query, args)

	if limit:
		page += limit
	else:
		page += cursor.rowcount

	if cursor.rowcount == 0:
		page = 0

	marking('marker', page)

	all_posts = dictfetchall(cursor)
	for post in all_posts:
		post['created'] = localtime(post['created'])

	response = {'marker': 'marker', 'posts': all_posts}

	cursor.close()
	return JsonResponse(response, status = 200)