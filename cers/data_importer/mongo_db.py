from pymongo import MongoClient
from cers.data_importer.base import DataImporter


class MongoDBDataImporter(DataImporter):
    """
    Imports data into a MongoDB.
    """

    def __init__(self, mongo_db_url, mongo_database_name, exchange_rates_table):
        self.mongo_client = MongoClient(f"mongodb://{mongo_db_url}/")
        self.mongo_database = self.mongo_client[mongo_database_name]
        self.collection = self.mongo_database[exchange_rates_table]

    def __exchange_rate_already_imported__(self, currency, date):
        doc = {'currency': currency, 'date': date}
        return self.collection.find(doc).limit(1).count() > 0

    def __save_exchange_rate__(self, currency, date, rate):
        doc = {
            'currency': currency,
            'date': date,
            'rate': rate
        }

        self.collection.insert_one(doc)
