class DataImporter:
    """
    Base class for different types of importers.
    """

    def import_exchange_rates(self, exchange_rates):
        saw_known_rate = False

        for currency, rates in exchange_rates.items():
            for date, rate in rates:
                if self.__exchange_rate_already_imported__(currency, date):
                    saw_known_rate = True
                    continue

                self.__save_exchange_rate__(currency, date, rate)

        import_status = {'saw_known_rate': saw_known_rate}

        return import_status
