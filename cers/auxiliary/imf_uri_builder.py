import cers.auxiliary.functions as auxiliary_functions


class IMFUriBuilder:

    HOST = 'www.imf.org'

    def exchange_rates_for_month_until_day(self, year_month_and_day, scheme='https', report_type='REP'):
        year, month, day = year_month_and_day

        day = auxiliary_functions.two_digit_str(day)
        month = auxiliary_functions.two_digit_str(month)
        date = f"{year}-{month}-{day}"
        base = f"{scheme}://{self.HOST}"

        url = base + ('/external/np/fin/data/rms_mth.aspx?'
            f"SelectDate={date}&reportType={report_type}")

        return url

    def exchange_rates_for_month(self, year_and_month, scheme='https', report_type='REP'):
        """Get the URI for the exchange rates of a certain month

        year (integer) - The year of the desired month
        month (integer) - The desired month in the year
        scheme (string) - The HTML scheme
        report_type (string) - One of the formats the IMF offers

        And so on...
        """

        year, month = year_and_month

        day = auxiliary_functions.last_day_of_month((year, month))
        url = self.exchange_rates_for_month_until_day((year, month, day), scheme=scheme, report_type=report_type)

        return url
