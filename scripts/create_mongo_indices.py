import argparse
import config
import pymongo
from pymongo import MongoClient


"""
Define script arguments.
"""
parser = argparse.ArgumentParser(
    description='Creates relevant indices in your MongoDB.'
)

parser.add_argument('--database-name',
    help='Name of the MongoDB database the scraped exchange rates will be '
        f"stored in. Defaults to \"{config.MONGO_DATABASE_NAME}\"",
    dest='database_name',
    default=config.MONGO_DATABASE_NAME
)



"""
Create indices.
"""
# Get script arguments.
args = parser.parse_args()

mongo_client = MongoClient(f"mongodb://{config.MONGO_DB_URL}/")
mongo_database = mongo_client[args.database_name]
collection = mongo_database[config.EXCHANGE_RATES_TABLE_NAME]

collection.create_index([('currency', pymongo.ASCENDING)])
collection.create_index([('currency', pymongo.ASCENDING), ('date', pymongo.DESCENDING)], unique=True)
