from dateutil import parser
import re
from cers.parser.engine.html import HTMLParser


class ParserIMFExchangeRatesHTML(HTMLParser):
    """
    Provides methods to access information in the HTML of an exchange rates page
    of IMF.
    """

    def __date_string_to_date__(self, date_string):
        # The date parser might get it wrong if there's no space after the
        # comma, as in `February 29,2016`. Therefore, make sure that there
        # always is one.
        date_string = str.replace(date_string, ',', ', ')

        date = parser.parse(date_string)

        return date

    def __float_string_to_float__(self, float_string):
        float_string = str.replace(float_string, ',', '')

        try:
          fl = float(float_string)
        except ValueError:
          return None

        return fl

    def exchange_rates(self):
        exchange_rates = {}

        for tbody in self.html.xpath('//tbody'):
            trs = tbody.xpath('./tr')

            if len(trs) < 2:
                continue

            second_tr_ths = trs[1].xpath('./th')

            if len(second_tr_ths) == 0:
                continue

            if 'Currency' not in second_tr_ths[0].text_content():
                continue

            # Get all dates from header row.
            dates = []
            for th in second_tr_ths[1:]:
                date_string = th.text_content().strip()
                date = self.__date_string_to_date__(date_string)
                dates.append(date)

            # Get rates.
            for tr in trs[2:]:
                tds = tr.xpath('./td')
                first_td = tds[0]
                tcc = first_td.text_content()

                currency = re.search(r"\A[\w\s\.-]*", tcc).group(0).strip()

                if currency not in exchange_rates:
                    exchange_rates[currency] = []

                rates = []
                for index, td in enumerate(tds[1:]):
                    date = dates[index]
                    float_string = td.text_content().strip()
                    float = self.__float_string_to_float__(float_string)
                    package = (date, float)
                    exchange_rates[currency].append(package)

        return exchange_rates
