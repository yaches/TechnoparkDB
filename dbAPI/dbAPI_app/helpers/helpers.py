import time, datetime, pytz
import string
import random


def random_string(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

def localtime(created):
	zone = pytz.timezone('Europe/Moscow')
	if created.tzinfo is None:
		created = zone.localize(created)
	else:
		created = created.astimezone(zone)
	return created


def curtime():
	return localtime(datetime.datetime.now())


def marking(page):
	name = random_string()
	try:
		marking.m[name] = page
	except:
		marking.m = {}
		marking.m[name] = page
	finally:
		return name
		

def postgreQueryFormat(query):
	ind = 0
	count = 1
	while True:
		ind = query.find('%s')
		if ind != -1:
			query = query[:ind] + '$' + str(count) + query[ind+2:]
			count += 1
		else:
			break

	return query

def preparing(query):
	try:
		preparing.queries
	except:
		preparing.queries = []

	if query in preparing.queries:
		return True
	else:
		preparing.queries.append(query)
		return False