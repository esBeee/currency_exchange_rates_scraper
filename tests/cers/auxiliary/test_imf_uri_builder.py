import unittest
from cers.auxiliary.imf_uri_builder import IMFUriBuilder


class TestImfUriBuilder(unittest.TestCase):

    def setUp(self):
        self.uri_builder = IMFUriBuilder()

    def test_exchange_rates_for_month(self):
        self.assertEqual(
            self.uri_builder.exchange_rates_for_month((2018, 4)),
            'https://www.imf.org/external/np/fin/data/rms_mth.aspx?SelectDate=2018-04-30&reportType=REP'
        )

        self.assertEqual(
            self.uri_builder.exchange_rates_for_month((2018, 2)),
            'https://www.imf.org/external/np/fin/data/rms_mth.aspx?SelectDate=2018-02-28&reportType=REP'
        )

        self.assertEqual(
            self.uri_builder.exchange_rates_for_month((2012, 2)),
            'https://www.imf.org/external/np/fin/data/rms_mth.aspx?SelectDate=2012-02-29&reportType=REP'
        )

        self.assertEqual(
            self.uri_builder.exchange_rates_for_month((2010, 12)),
            'https://www.imf.org/external/np/fin/data/rms_mth.aspx?SelectDate=2010-12-31&reportType=REP'
        )

if __name__ == '__main__':
    unittest.main()
