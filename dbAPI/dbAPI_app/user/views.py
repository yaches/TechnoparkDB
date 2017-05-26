import psycopg2

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

from dbAPI_app.helpers.helpers import *
from dbAPI_app.helpers.db import *
from dbAPI_app.queries.users import *


@csrf_exempt
def create(request, nickname):
	# print(request.path)

	params = json.loads(request.body.decode("utf-8"))
	params['nickname'] = nickname
	conn = connectFromPool()
	cursor = conn.cursor()

	cursor.execute(CHECK_USERS_EXIST, [nickname, params['email']])
	if cursor.rowcount > 0:
		users = dictfetchall(cursor)
		cursor.close()
		return JsonResponse(users, status = 409, safe = False)

	cursor.execute(CREATE_USER, [nickname, params['email'], params['fullname'], params['about']])

	cursor.close()
	return JsonResponse(params, status = 201)


@csrf_exempt
def profile(request, nickname):
	# print(request.path)
	
	conn = connectFromPool()
	cursor = conn.cursor()

	cursor.execute(SELECT_USER_BY_NICKNAME, [nickname])
	if cursor.rowcount == 0:
		cursor.close()
		return JsonResponse({}, status = 404)
	
	user = dictfetchall(cursor)[0]

	if request.method == 'GET':
		cursor.close()
		return JsonResponse(user, status = 200)
	else:
		params = json.loads(request.body.decode("utf-8"))
		params['nickname'] = nickname
		
		if not 'email' in params:
			params['email'] = user['email']
		
		if not 'fullname' in params:
			params['fullname'] = user['fullname']

		if not 'about' in params:
			params['about'] = user['about']

		try:
			cursor.execute(UPDATE_USER, [
				params['email'], params['fullname'], params['about'], nickname
			])
		except psycopg2.Error as e:
			if e.pgcode == '23505':
				cursor.close()
				return JsonResponse({}, status = 409)
			else:
				print(e.pgcode)
				print(e)

		cursor.close()
		return JsonResponse(params, status = 200)