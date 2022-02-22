import time
import logging
import hashlib

from helpers import *


def main():
	'''
		Description: main structure
	'''
	
	# Initial configuration
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
	exchange = os.environ['exchange']
	currency = os.environ['book']
	routes = get_routes(exchange)
	url = routes['get_price']
	book = routes['book_' + currency]
	numbots = int(os.environ['numbots'])
	current_index_bot = 1
	amount_list = [100, 100, 200, 400, 800]
	
	while True:
		
		#bot_id = hashlib.md5(bytes('{0}-{1}-{2}'.format(exchange, book, current_index_bot), 'UTF-8')).hexdigest()
		bot_id = '{0}-{1}-{2}'.format(exchange, currency, current_index_bot)

		# Last price obtained
		last_price = get_last_price(exchange)
		logging.info('Bot [{0}] Getting last db price => Exchange {1} - $ {2} - Currency {3}' \
						.format(bot_id, exchange, last_price, currency))


		current_index_bot = (current_index_bot + 1) % numbots + 1
		time.sleep(int(60/numbots))

main()