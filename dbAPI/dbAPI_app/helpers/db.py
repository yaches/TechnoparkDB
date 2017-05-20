import psycopg2

def connect():
	try:
		return connect.conn
	except:
		connect.conn = psycopg2.connect(dbname='dbapi', user='postgres')
		return connect.conn