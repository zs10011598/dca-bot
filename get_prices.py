#!/bin/python3

import os
import json
import requests
import logging

from helpers import *


def main():
	'''
		Description: get data prices
	'''
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

	exchange = os.environ['exchange']
	book = os.environ['book']
	
	routes = get_routes(exchange)
	url = routes['get_price']
	book = routes['book_btc']

	res = requests.get('{0}?{1}'.format(url, book))

	try:
		data = res.json()
		if data['success']:
			price_row = {
				'high': data['payload']['high'],
				'last': data['payload']['last'],
				'created_at': data['payload']['created_at'],
				'book': data['payload']['book'],
				'volume': data['payload']['volume'],
				'vwap': data['payload']['vwap'],
				'low': data['payload']['low'],
				'ask': data['payload']['ask'],
				'bid': data['payload']['bid'],
				'change_24': data['payload']['change_24']
			}

			logging.info('Getting price => Exchange {0} - $ {1} - Book {2}' \
				.format(exchange, price_row['last'], book))

			write_db_operation('insert_price', price_row)

	except Exception as e:
		logging.error('Getting price => Exchange {0} - Book {1} - Error {2}'.format(exchange, book, str(e)))

main()