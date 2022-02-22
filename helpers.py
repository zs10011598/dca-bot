import os
import json
import psycopg2


def get_last_price(exchange):
	'''
		Description: get last price from db
	'''
	return run_query_db('get_last_price', {'exchange': exchange})[0]


def get_routes(exchange):
	'''
		Description: get the routes for a given exchange
	'''
	with open(os.path.dirname(os.path.abspath(__file__)) + '/routes_exchanges/' + exchange + '.json', 'r') as f:
		routes = f.read()
	return json.loads(routes)


def get_db_conn():
	'''
		Descripction: get dca bot db connection
	'''
	dbname = os.environ['dbname']
	dbuser = os.environ['dbuser']
	dbpass = os.environ['dbpass']
	dbhost = os.environ['dbhost']
	dbport = os.environ['dbport']
	conn = psycopg2.connect('dbname={0} user={1} password={2} host={3} port={4}'.format(dbname, dbuser, dbpass, dbhost, dbport))
	return conn


def get_sql(name_sql):
	'''
		Description: get the sql statement specified
	'''
	with open(os.path.dirname(os.path.abspath(__file__)) + '/sqls/' + name_sql + '.sql', 'r') as f:
		return f.read()


def write_db_operation(sql_name, row):
	'''
		Description: run a sql statement
	'''
	conn = get_db_conn()
	cur = conn.cursor()
	cur.execute(get_sql(sql_name).format(**row))
	conn.commit()
	cur.close()
	conn.close()


def run_query_db(sql_name, row):
	'''
		Description: run query on db
	'''
	conn = get_db_conn()
	cur = conn.cursor()
	query = get_sql(sql_name).format(**row)
	cur.execute(query)
	result = cur.fetchall()
	cur.close()
	conn.close()

	return result