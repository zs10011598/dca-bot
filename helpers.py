import os
import json
import psycopg2
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


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
	if os.environ['environment'] == 'test':
		logging.info('SQL: {0}'.format(query))
	cur.execute(query)
	result = cur.fetchall()
	cur.close()
	conn.close()

	return result


def get_last_transaction(bot_id):
	'''
		Description: get last transaction of a given bot
	'''
	result = run_query_db('get_last_transaction_bot', {'bot_id': bot_id})
	return result[0] if len(result) > 0 else None


def should_buy_now():
	'''
		Description: decide wheter bot should buy now
	'''
	# ToDo
	return True


def buy(bot_id, exchange, cryptocurrency, cycle, transaction_index, 
		type_operation, entry_price, transaction_currency_ammount):
	'''
		Description: function to buy
	'''
	# ToDo
	pass