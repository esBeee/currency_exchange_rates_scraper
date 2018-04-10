import unittest
import os
import config
from pymongo import MongoClient


class TestCreateMongoIndices(unittest.TestCase):

    DATABASE_NAME = 'test_create_mongo_indices'

    def setUp(self):
        self.mongo_client = MongoClient(f"mongodb://{config.MONGO_DB_URL}/")
        self.mongo_database = self.mongo_client[self.DATABASE_NAME]
        self.mongo_collection = self.mongo_database[config.EXCHANGE_RATES_TABLE_NAME]

    def tearDown(self):
        self.mongo_client.drop_database(self.DATABASE_NAME)

    def test_indices_creating(self):
        os.system('python -m scripts.create_mongo_indices '
            f"--database-name {self.DATABASE_NAME}"
        )

        index_information = self.mongo_collection.index_information()

        currency_index = index_information['currency_1']
        self.assertEqual(currency_index['key'], [('currency', 1)])

        currency_date_index = index_information['currency_1_date_-1']
        self.assertEqual(currency_date_index['key'], [('currency', 1), ('date', -1)])
        self.assertEqual(currency_date_index['unique'], True)

if __name__ == '__main__':
    unittest.main()
