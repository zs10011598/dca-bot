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
	cryptocurrency = os.environ['cryptocurrency']
	numbots = int(os.environ['numbots'])
	environment = os.environ['environment']
	routes = get_routes(exchange)
	url = routes['get_price']
	book = routes['book_' + cryptocurrency]
	amount_list = [100, 100, 200, 400, 800]
	current_index_bot = 1
	sell_percentage = 0.0201
	buy_percentage = 0.03
	
	while True:
		
		#bot_id = hashlib.md5(bytes('{0}-{1}-{2}'.format(exchange, book, current_index_bot), 'UTF-8')).hexdigest()
		bot_id = '{0}{1}{2}'.format(exchange, cryptocurrency, current_index_bot)

		# Last price obtained
		last_price = get_last_price(exchange)
		logging.info('Bot [{0}] Getting last db price => Exchange {1} - $ {2} - cryptocurrency {3}' \
						.format(bot_id, exchange, last_price, cryptocurrency))

		# Last transaction of current bot
		last_transaction = get_last_transaction(bot_id)
		if last_transaction == None or last_transaction[5] == 'sell':
			if should_buy_now():
				logging.info('Bot [{0}] Buying => Exchange {1} - $ {2} - cryptocurrency {3}' \
								.format(bot_id, exchange, last_price, cryptocurrency))
				buy(bot_id, exchange, cryptocurrency, cycle=1, transaction_index=1, type_operation='buy', 
					entry_price=last_price, transaction_currency_ammount=amount_list[0])
			else:
				continue
		else:
			#ToDo: decide buy or sell
			pass

		current_index_bot = (current_index_bot + 1) % numbots + 1
		time.sleep(int(60/numbots))

main()