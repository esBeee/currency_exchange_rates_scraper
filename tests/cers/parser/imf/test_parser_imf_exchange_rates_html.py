import unittest
import os
import datetime
from cers.parser.imf.exchange_rates_html import ParserIMFExchangeRatesHTML


class TestImfExchangeRatesParser(unittest.TestCase):

    def __imf_exchange_rates_source__(self):
        path = os.path.join('tests', 'fixtures', 'imf_exchange_rates_source.html')
        with open(path, 'r') as file:
            html = file.read()

        return html

    def test_exchange_rates_for_month(self):
        html = self.__imf_exchange_rates_source__()
        parser = ParserIMFExchangeRatesHTML(html=html)
        exchange_rates = parser.exchange_rates()

        self.assertEqual(len(exchange_rates), 51)

        example = exchange_rates['Chinese Yuan'][0]
        self.assertIsInstance(example[0], datetime.date)
        self.assertEqual(example[0].day, 1)
        self.assertEqual(example[0].month, 3)
        self.assertEqual(example[0].year, 2018)
        self.assertEqual(example[1], 6.341800)

        example = exchange_rates['Botswana Pula'][6]
        self.assertIsInstance(example[0], datetime.date)
        self.assertEqual(example[0].day, 9)
        self.assertEqual(example[0].month, 3)
        self.assertEqual(example[0].year, 2018)
        self.assertEqual(example[1], 0.104300)

        example = exchange_rates['Iranian Rial'][21]
        self.assertIsInstance(example[0], datetime.date)
        self.assertEqual(example[0].day, 30)
        self.assertEqual(example[0].month, 3)
        self.assertEqual(example[0].year, 2018)
        self.assertEqual(example[1], 37743.000000)

        example = exchange_rates['Bolivar Fuerte'][12]
        self.assertIsInstance(example[0], datetime.date)
        self.assertEqual(example[0].day, 19)
        self.assertEqual(example[0].month, 3)
        self.assertEqual(example[0].year, 2018)
        self.assertEqual(example[1], None)

if __name__ == '__main__':
    unittest.main()
