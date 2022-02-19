import os
import json
import psycopg2


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


def write_db_operation(sql_name, price_row):
	'''
		Description: run a sql statement
	'''
	conn = get_db_conn()
	cur = conn.cursor()
	cur.execute(get_sql(sql_name).format(**price_row))
	conn.commit()
	cur.close()
	conn.close()