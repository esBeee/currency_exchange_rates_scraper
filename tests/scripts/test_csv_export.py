import unittest
import os
import csv
import shutil
import datetime
import config
from pymongo import MongoClient


class TestCSVExport(unittest.TestCase):

    TMP_DIRECTORY = 'tmp'
    DATABASE_NAME = 'test_csv_export'

    def setUp(self):
        self.mongo_client = MongoClient(f"mongodb://{config.MONGO_DB_URL}/")
        self.mongo_database = self.mongo_client[self.DATABASE_NAME]
        self.mongo_collection = self.mongo_database[config.EXCHANGE_RATES_TABLE_NAME]

        os.makedirs(self.TMP_DIRECTORY)

    def tearDown(self):
        self.mongo_client.drop_database(self.DATABASE_NAME)

        shutil.rmtree(self.TMP_DIRECTORY)

    def __insert__(self, currency, date, rate):
        doc = {
            'currency': currency,
            'date': datetime.datetime(*date, 0, 0),
            'rate': rate
        }

        self.mongo_collection.insert_one(doc)

    def test_csv_export(self):
        self.__insert__('Euro', (2017, 11, 23), 35.1)
        self.__insert__('AUD', (2017, 11, 23), 134.1)
        self.__insert__('Euro', (2018, 3, 1), 1.2171)
        self.__insert__('USD', (2018, 3, 20), 367)
        self.__insert__('Euro', (2018, 5, 2), 134)
        self.__insert__('AUD', (2019, 12, 31), 832)

        csv_location = os.path.join(self.TMP_DIRECTORY, 'test_csv_export.csv')

        os.system(f"python -m scripts.csv_export "
            f"--database-name {self.DATABASE_NAME} "
            f"{csv_location}"
        )

        with open(csv_location, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_rows = list(csv_reader)

            # Make sure the header is correct.
            self.assertEqual(csv_rows[0], ['Date', 'AUD', 'Euro', 'USD'])

            # Make sure the rates are correct.
            self.assertEqual(csv_rows[1], ['2017-11-23', '134.1', '35.1', ''])
            self.assertEqual(csv_rows[2], ['2018-3-1', '', '1.2171', ''])
            self.assertEqual(csv_rows[3], ['2018-3-20', '', '', '367'])
            self.assertEqual(csv_rows[4], ['2018-5-2', '', '134', ''])
            self.assertEqual(csv_rows[5], ['2019-12-31', '832', '', ''])

if __name__ == '__main__':
    unittest.main()
