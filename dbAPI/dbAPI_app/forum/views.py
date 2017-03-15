from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

from dbAPI_app.helpers.helpers import *
from dbAPI_app.queries.forums import *

@csrf_exempt
def create(request):
	params = json.loads(request.body)
	cursor = connection.cursor
	cursor.execute()