import os


CHROMEDRIVER_URL = os.environ['CHROMEDRIVER_URL']

MONGO_DB_URL = os.environ['MONGO_DB_URL']
MONGO_DATABASE_NAME = 'currency_exchange_rates'
EXCHANGE_RATES_TABLE_NAME = 'exchange_rates'

BACK_UNTIL_DEFAULT = '1-1995'
PAUSES_BETWEEN_PAGE_VISITINGS = (30, 60) # If value is `(5, 10)`, the pauses will be between 5 to 10 seconds.
