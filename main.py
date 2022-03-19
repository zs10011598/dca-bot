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
	amount_list = [100.0, 100.0, 200.0, 400.0, 800.0]
	current_index_bot = 1
	sell_percentage = 0.0233
	buy_percentage = 0.03
	
	while True:
		
		keep_trading = get_parameter('keep_trading')

		#bot_id = hashlib.md5(bytes('{0}-{1}-{2}'.format(exchange, book, current_index_bot), 'UTF-8')).hexdigest()
		bot_id = '{0}{1}{2}'.format(exchange, cryptocurrency, current_index_bot)

		# Last price obtained
		last_price = get_last_price(exchange)
		logging.info('Bot [{0}] Getting last db price => Exchange {1} - $ {2} - cryptocurrency {3}' \
						.format(bot_id, exchange, last_price, cryptocurrency))

		# Last transaction of current bot
		last_transaction = get_last_transaction(bot_id)

		if last_transaction != None:
			cycle = last_transaction[2]
			transaction_index = last_transaction[3]
			type_operation = last_transaction[5]
			average_price = last_transaction[10]

		if (last_transaction == None or type_operation == 'sell') and keep_trading:

			if should_buy_now():

				logging.info('Bot [{0}] First Buying => Exchange {1} - $ {2} - cryptocurrency {3}' \
								.format(bot_id, exchange, last_price, cryptocurrency))

				available_balance = get_balance(exchange)
				logging.info('Bot [{0}] First Buying => Exchange {1} - Balance $ {2}' \
								.format(bot_id, exchange, available_balance))

				amount_to_buy = amount_list[0]

				if amount_to_buy <= available_balance or environment == 'test':

					oid = do_transaction(bot_id, exchange, cryptocurrency, 1 if last_transaction == None else cycle + 1, 
						transaction_index=0, type_operation='buy', entry_price=last_price, 
						transaction_currency_ammount=amount_to_buy)

				else:

					logging.info('Bot [{0}] First Buying => Not enoght balance (${1}) to buy ${2} in exchange {3}' \
								.format(bot_id, available_balance, amount_to_buy, exchange))
			else:

				logging.info('Bot [{0}] First Buying => It\'s not a good time to buy' \
								.format(bot_id))
				continue

		elif type_operation == 'buy':
			
			if last_price <= average_price*(1 - buy_percentage) and len(amount_list) < 4:

				amount_to_buy = amount_list[transaction_index + 1]

				available_balance = get_balance(exchange)
				logging.info('Bot [{0}] Buying => Exchange {1} - Balance $ {2}' \
								.format(bot_id, exchange, available_balance))

				if amount_to_buy <= available_balance or environment == 'test':
					logging.info('Bot [{0}] Buying => Exchange {1} - amount ${2} - entry price ${3}- cryptocurrency {4}' \
									.format(bot_id, exchange, amount_to_buy, last_price, cryptocurrency))

					oid = do_transaction(bot_id, exchange, cryptocurrency, cycle, transaction_index + 1, 
							type_operation='buy', entry_price=last_price, transaction_currency_ammount=amount_to_buy)
				else:

					logging.info('Bot [{0}] Buying => Not enoght balance (${1}) to buy ${2} in exchange {3}' \
								.format(bot_id, available_balance, amount_to_buy, exchange))

			elif average_price*(1 + sell_percentage) <= last_price:

				logging.info('Bot [{0}] Selling => Exchange {1} - cryptocurrency {4}' \
								.format(bot_id, exchange, cryptocurrency))

				oid = do_transaction(bot_id, exchange, cryptocurrency, cycle, -1, type_operation='sell', 
						entry_price=last_price, transaction_currency_ammount=0)

			else:
				
				logging.info('Bot [{0}] Transaction index {1} => Not buy or sell' \
								.format(bot_id, transaction_index))

		else:
			logging.info('Bot [{0}] Invalid last transaction'.format(bot_id))

		current_index_bot = (current_index_bot + 1) % numbots
		time.sleep(int(60/numbots))

main()