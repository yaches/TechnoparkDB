import psycopg2
import psycopg2.pool

def connectSimple():
	try:
		return connectSimple.conn
	except:
		connectSimple.conn = psycopg2.connect(dbname='dbapi', user='postgres')
		# connectSimple.conn = psycopg2.connect(dbname='dbapi', user='docker', password='docker', host='localhost', port='5432')
		connectSimple.conn.autocommit = True
		return connectSimple.conn

def connectFromPool():
	try:
		conn = connectFromPool.pool.getconn()
	except:
		connectFromPool.pool = psycopg2.pool.PersistentConnectionPool(1, 10, dbname='dbapi', user='postgres')
		# connectFromPool.pool = psycopg2.pool.PersistentConnectionPool(1, 10, dbname='dbapi', user='docker', password='docker', host='localhost', port='5432')
		conn = connectFromPool.pool.getconn()
	finally:
		conn.autocommit = True;
		return conn