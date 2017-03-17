import time, datetime, pytz

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

def localtime(created):
	zone = pytz.timezone('Europe/Moscow')
	return created.astimezone(zone)

def curtime():
	return localtime(datetime.datetime.now())

def marking(name, page):
	try:
		marking.m[name] = page
	except:
		marking.m = {}
		marking.m[name] = page
