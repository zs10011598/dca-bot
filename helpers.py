import os
import json
import psycopg2
import logging
from api_connections.bitso import *
import time

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_last_price(exchange):
	'''
		Description: get last price from db
	'''
	return run_query_db('get_last_price', {'exchange': exchange})[0][0]


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
	# ToDo: more sophisticated logic
	return True


def do_transaction(bot_id, exchange, cryptocurrency, cycle, transaction_index, 
		type_operation, entry_price, transaction_currency_ammount):
	'''
		Description: function to buy or to sell
	'''
	environment = os.environ['environment']
	exchange = os.environ['exchange']
	oid = ''
	fee_percent = 0.0065

	last_transaction = get_last_transaction(bot_id)

	if environment == 'production':
		pass
	elif environment == 'test':

		oid = int(time.time()*1000)

		if type_operation == 'buy':
			
			transaction_cryptocurrency_ammount = transaction_currency_ammount / entry_price
			transaction_cryptocurrency_fee = transaction_cryptocurrency_ammount * fee_percent
			transaction_cryptocurrency_ammount -= transaction_cryptocurrency_fee
			transaction_currency_fee = 0

			if last_transaction == None or transaction_index == 0:
				cummulated_currency_ammount = transaction_currency_ammount
				cummulated_cryptocurrency_ammount = transaction_cryptocurrency_ammount
			else:
				cummulated_currency_ammount = last_transaction[9] + transaction_currency_ammount
				cummulated_cryptocurrency_ammount = last_transaction[12] + transaction_cryptocurrency_ammount

			average_price = cummulated_currency_ammount / cummulated_cryptocurrency_ammount
			profit = 0

		elif type_operation == 'sell':
			transaction_cryptocurrency_ammount = 0
			transaction_cryptocurrency_fee = 0
			cummulated_currency_ammount = last_transaction[9]
			cummulated_cryptocurrency_ammount = last_transaction[12]
			transaction_currency_ammount =  entry_price * cummulated_cryptocurrency_ammount
			transaction_currency_fee = transaction_currency_ammount * fee_percent
			transaction_currency_ammount -= transaction_currency_fee
			average_price = transaction_currency_ammount / cummulated_cryptocurrency_ammount
			profit = transaction_currency_ammount - cummulated_currency_ammount

	row = {}
	row['bot_id'] = bot_id
	row['cycle'] = cycle 
	row['transaction_index'] = transaction_index
	row['type_operation'] = type_operation
	row['entry_price'] = entry_price
	row['transaction_currency_fee'] = transaction_currency_fee
	row['transaction_currency_ammount'] = transaction_currency_ammount
	row['environment'] = environment
	row['order_id'] = oid
	row['exchange'] = exchange 
	row['cummulated_currency_ammount'] = cummulated_currency_ammount
	row['average_price'] = average_price
	row['cummulated_cryptocurrency_ammount'] = cummulated_cryptocurrency_ammount
	row['transaction_cryptocurrency_ammount'] = transaction_cryptocurrency_ammount
	row['transaction_cryptocurrency_fee'] = transaction_cryptocurrency_fee
	row['profit'] = profit

	write_db_operation('insert_transaction', row)

	return oid


def get_parameter(parameter):
	'''
		Description: get a specified parameter
	'''
	# ToDo
	return True


def get_balance(exchange):
	'''
		Description: get balance
	'''
	if exchange == 'bitso':
		return get_bitso_balance()
	return None