import json
import time
import pytz

import psycopg2

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError, Error

from dbAPI_app.helpers.helpers import *
from dbAPI_app.helpers.db import *

from dbAPI_app.queries.service import *


@csrf_exempt
def test(request):
	# print(request.path)

	conn = connectFromPool()
	cursor = conn.cursor()

	query = u''' 
		SELECT * FROM "lalala"
	'''
	try:
		cursor.execute(query)
	except psycopg2.Error as e:
		print(e)
		print(e.pgcode)
		print(e.pgerror)

	cursor.close()
	return JsonResponse({})

@csrf_exempt
def status(request):
	# print(request.path)

	conn = connectFromPool()
	cursor = conn.cursor()

	cursor.execute(SELECT_DATA_AMOUNT)
	response = dictfetchall(cursor)[0]

	cursor.close()
	return JsonResponse(response, status = 200)


@csrf_exempt
def clear(request):
	# print(request.path)

	conn = connectFromPool()
	cursor = conn.cursor()

	cursor.execute(TRUNCATE_ALL)

	cursor.close()
	return JsonResponse({}, status = 200)