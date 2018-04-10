import unittest
import os
import datetime
import config
from pymongo import MongoClient


class TestScrapeIMF(unittest.TestCase):

    DATABASE_NAME = 'test_currency_exchange_rates'

    def setUp(self):
        self.mongo_client = MongoClient(f"mongodb://{config.MONGO_DB_URL}/")
        self.mongo_database = self.mongo_client[self.DATABASE_NAME]
        self.mongo_collection = self.mongo_database[config.EXCHANGE_RATES_TABLE_NAME]

    def tearDown(self):
        self.mongo_client.drop_database(self.DATABASE_NAME)

    def test_scraping_from_to(self):
        os.system('python -m scripts.scrape_imf '
            '--back-until 2-2018 '
            '--up-from 3-2018 '
            # '--quiet '
            f"--database-name {self.DATABASE_NAME}"
        )

        # Make sure all currencies get parsed.
        currencies = self.mongo_collection.distinct('currency')
        self.assertEqual(len(currencies), 51)

        # Make sure the rates for all dates get parsed.
        actual_amount_of_dates = 22 + 19
        euro_rates = self.mongo_collection.find({'currency': 'Euro'}).count()
        self.assertEqual(euro_rates, actual_amount_of_dates)
        chil_peso_rates = self.mongo_collection.find({'currency': 'Chilean Peso'}).count()
        self.assertEqual(euro_rates, actual_amount_of_dates)

        # Check a few samples.
        rate = self.mongo_collection.find_one({
            'currency': 'Chinese Yuan',
            'date': datetime.datetime(2018, 2, 1, 0, 0)
        })['rate']
        self.assertEqual(rate, 6.3021)

        rate = self.mongo_collection.find_one({
            'currency': 'Colombian Peso',
            'date': datetime.datetime(2018, 2, 7, 0, 0)
        })['rate']
        self.assertEqual(rate, 2844.83)

        rate = self.mongo_collection.find_one({
            'currency': 'Kuwaiti Dinar',
            'date': datetime.datetime(2018, 2, 26, 0, 0)
        })['rate']
        self.assertEqual(rate, None)

        rate = self.mongo_collection.find_one({
            'currency': 'Nuevo Sol',
            'date': datetime.datetime(2018, 2, 28, 0, 0)
        })['rate']
        self.assertEqual(rate, 3.259)

        rate = self.mongo_collection.find_one({
            'currency': 'Chinese Yuan',
            'date': datetime.datetime(2018, 3, 1, 0, 0)
        })['rate']
        self.assertEqual(rate, 6.3418)

        rate = self.mongo_collection.find_one({
            'currency': 'U.A.E. Dirham',
            'date': datetime.datetime(2018, 3, 30, 0, 0)
        })['rate']
        self.assertEqual(rate, 3.6725)

        rate = self.mongo_collection.find_one({
            'currency': 'New Zealand Dollar',
            'date': datetime.datetime(2018, 3, 29, 0, 0)
        })['rate']
        self.assertEqual(rate, 0.7203)

    def test_stop_if_known_option(self):
        # Make sure a rate from the latest month is already known.
        doc = {
            'currency': 'Euro',
            'date': datetime.datetime(2018, 3, 1, 0, 0),
            'rate': 1.2171
        }
        self.mongo_collection.insert_one(doc)

        os.system('python -m scripts.scrape_imf '
            '--back-until 2-2018 '
            '--up-from 3-2018 '
            '--stop-if-known '
            # '--quiet '
            f"--database-name {self.DATABASE_NAME}"
        )

        # Make sure only the dates of the latest month were parsed.
        euro_rates = self.mongo_collection.find({'currency': 'Japanese Yen'}).count()
        self.assertEqual(euro_rates, 22)

if __name__ == '__main__':
    unittest.main()
