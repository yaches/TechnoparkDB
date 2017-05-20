import time, datetime, pytz

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

def marking(name, page):
	try:
		marking.m[name] = page
	except:
		marking.m = {}
		marking.m[name] = page
		

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