import time
import datetime
import random
from cers.data_importer.mongo_db import MongoDBDataImporter
from cers.scraper.imf import IMFScraper


class IMFScrapingOrganizer:
    """
    Organizes the scraping and data storing over multiple IMF pages using the
    available scraper methods for IMF.
    """

    def __init__(self, chromedriver_url, mongo_db_url, mongo_database_name, exchange_rates_table, pauses, quiet):
        self.chromedriver_url = chromedriver_url
        self.pauses = pauses
        self.quiet = quiet
        self.data_importer = MongoDBDataImporter(
            mongo_db_url=mongo_db_url,
            mongo_database_name=mongo_database_name,
            exchange_rates_table=exchange_rates_table
        )

    def __log__(self, message=''):
        if not self.quiet:
            print(message)

    def __pause_between_page_loads__(self):
        pause_length = random.randint(*self.pauses)
        self.__log__(f"Sleeping for {pause_length} seconds.")
        time.sleep(pause_length)

    def __process_exchange_rates__(self, exchange_rates):
        import_status = self.data_importer.import_exchange_rates(exchange_rates)
        saw_known_rate = import_status['saw_known_rate']

        return saw_known_rate

    def __months_between__(self, back_until, up_from):
        back_to_year, back_to_month = back_until
        up_until_year, up_until_month = up_from
        months = []

        for year in range(back_to_year, up_until_year + 1):
            to_month = up_until_month if year == up_until_year else 12
            from_month = back_to_month if year == back_to_year else 1

            for month in range(from_month, to_month + 1):
                months.append((year, month))

        return reversed(months)

    def scrape_exchange_rates_between(self, back_until, up_from, stop_if_known=False):
        relevant_months = self.__months_between__(back_until, up_from)

        with IMFScraper(chromedriver_url=self.chromedriver_url) as imf_scraper:
            for year_and_month in relevant_months:
                self.__log__()
                self.__log__(f"Parsing exchange rates for {year_and_month[1]}/{year_and_month[0]}.")

                exchange_rates = imf_scraper.exchange_rates(year_and_month)
                saw_known_rate = self.__process_exchange_rates__(exchange_rates)

                if stop_if_known and saw_known_rate:
                    self.__log__("Stopping scraping because known exchange rates have been encountered.")
                    break

                self.__pause_between_page_loads__()
