from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

from dbAPI_app.helpers.helpers import *
from dbAPI_app.queries.forums import *
from dbAPI_app.queries.users import *

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