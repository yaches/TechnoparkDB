import json
import time
import pytz
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

from dbAPI_app.helpers.helpers import *
from dbAPI_app.queries.service import *


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
	
	cursor.execute(CLEAR_VOTES)
	cursor.execute(CLEAR_POSTS)
	cursor.execute(CLEAR_THREADS)
	cursor.execute(CLEAR_FORUMS)
	cursor.execute(CLEAR_USERS)

	cursor.close()
	return JsonResponse({}, status = 200)