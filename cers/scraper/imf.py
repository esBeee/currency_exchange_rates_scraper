from cers.scraper.engine.chromedriver import Chromedriver
from cers.parser.imf.exchange_rates_html import ParserIMFExchangeRatesHTML
from cers.auxiliary.imf_uri_builder import IMFUriBuilder


class IMFScraper(Chromedriver):
    """
    A collection of scraping methods for host IMF.
    """

    def __init__(self, chromedriver_url):
        # Initialize required engines.
        Chromedriver.__init__(self, chromedriver_url)

        self.imf_uri_builder = IMFUriBuilder()

    def exchange_rates(self, year_and_month):
        url = self.imf_uri_builder.exchange_rates_for_month(year_and_month)

        self.driver.get(url)
        page_source = self.driver.page_source

        try:
            parser = ParserIMFExchangeRatesHTML(html=page_source)
            exchange_rates = parser.exchange_rates()
        except ValueError:
            # Save current page source for debugging purposes.
            path = os.join.path('debug', 'last_failed_page_source.html')
            with open(path, 'w') as file:
                file.write(page_source)

            # Raise the catched error.
            raise

        return exchange_rates
