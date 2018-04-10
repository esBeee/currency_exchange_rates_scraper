import argparse
import config
import csv
import datetime
from pymongo import MongoClient
import cers.auxiliary.functions as auxiliary_functions


"""
Define script arguments.
"""
parser = argparse.ArgumentParser(
    description='Exports all exchange rates in the specified MongoDB database '
        'into a CSV file.'
)

parser.add_argument('csv_location',
    help='The location of the CSV file to be created.'
)

parser.add_argument('--database-name',
    help='Name of the MongoDB database the exchange rates will be exported '
        f"from. Defaults to \"{config.MONGO_DATABASE_NAME}\"",
    dest='database_name',
    default=config.MONGO_DATABASE_NAME
)


"""
Start scraping.
"""
# Get script arguments.
args = parser.parse_args()

mongo_client = MongoClient(f"mongodb://{config.MONGO_DB_URL}/")
mongo_database = mongo_client[args.database_name]
collection = mongo_database[config.EXCHANGE_RATES_TABLE_NAME]

with open(args.csv_location, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)

    currencies = collection.distinct('currency')
    currencies.sort()

    # Write header.
    csv_writer.writerow(['Date'] + currencies)

    dates = collection.distinct('date')
    dates.sort()

    for date in dates:
        rates_for_date = []
        for currency in currencies:
            exchange_rate = collection.find_one({'date': date, 'currency': currency})
            rate = exchange_rate['rate'] if exchange_rate else None
            rates_for_date.append(rate)
        csv_writer.writerow([auxiliary_functions.ymd_date_string(date)] + rates_for_date)
