from django.http import JsonResponse
from json import loads
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, DatabaseError, IntegrityError

@csrf_exempt
def create(request, nickname):
	# args = loads(request.body)
	args = {}
	args['nickname'] = nickname
	# print(args)
	cursor = connection.cursor()
	cursor.execute('DROP TABLE IF EXISTS persons')
	cursor.execute('CREATE TABLE Persons (\
    PersonID int,\
    LastName varchar(255),\
    FirstName varchar(255),\
    Address varchar(255),\
    City varchar(255) \
);')
	cursor.close()
	return JsonResponse(args, status = 201)