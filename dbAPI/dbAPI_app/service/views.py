import json
import time
import pytz

import psycopg2
import asyncio
import asyncpg

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError, Error

from dbAPI_app.helpers.helpers import *
from dbAPI_app.helpers.db import *

from dbAPI_app.queries.service import *


@csrf_exempt
def test(request):
	conn = connect()
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
	cursor = connection.cursor()
	cursor.execute(SELECT_DATA_AMOUNT)
	response = dictfetchall(cursor)[0]

	cursor.close()
	return JsonResponse(response, status = 200)


@csrf_exempt
def clear(request):
	cursor = connection.cursor()
	
	# cursor.execute(CLEAR_VOTES)
	# cursor.execute(CLEAR_POSTS)
	# cursor.execute(CLEAR_THREADS)
	# cursor.execute(CLEAR_FORUMS)
	# cursor.execute(CLEAR_USERS)
	cursor.execute(TRUNCATE_ALL)

	cursor.close()
	return JsonResponse({}, status = 200)