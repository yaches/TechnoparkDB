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
from dbAPI_app.queries.common import *
from dbAPI_app.queries.posts import *


@csrf_exempt
def details(request, id):
	if request.method == 'GET':
		related = request.GET.get('related', False)
		if related:
			related = related.split(',')
		else:
			related = []

		cursor = connection.cursor()
		try:
			cursor.execute(SELECT_POST_BY_ID, [id])
		except IntegrityError:
			return JsonResponse({}, status = 404)

		response = {}

		post = dictfetchall(cursor)[0]
		post['created'] = localtime(post['created'])
		response['post'] = post

		if 'user' in related:
			cursor.execute(SELECT_USER_BY_NICKNAME, [post['author']])
			user = dictfetchall(cursor)[0]
			response['user'] = user
		if 'thread' in related:
			cursor.execute(SELECT_THREAD_BY_ID, [post['thread']])
			thread = dictfetchall(cursor)[0]
			thread['created'] = localtime(thread['created'])
			response['thread'] = thread
		if 'forum' in related:
			cursor.execute(SELECT_FORUM_BY_SLUG, [post['forum']])
			forum = dictfetchall(cursor)[0]
			forum['created'] = localtime(forum['created'])
			response['forum'] = forum

		return JsonResponse(response, status = 200)

	else:
		params = json.loads(request.body)
		message = params['message'] if 'message' in params else False

		cursor = connection.cursor()

		cursor.execute(SELECT_POST_BY_ID, [id])
		post = dictfetchall(cursor)[0]

		if message:
			cursor.execute(POST_UPDATE_MESSAGE, [message, id])
			post['message'] = message
			post['isEdited'] = True

		post['created'] = localtime(post['created'])

		return JsonResponse(post, status = 200)