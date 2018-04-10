import argparse
import config
import cers.auxiliary.functions as auxiliary_functions
from cers.imf_scraping_organizer import IMFScrapingOrganizer


"""
Define script arguments.
"""
parser = argparse.ArgumentParser(
    description='Scrape currency exchange rates from IMF.org and store it in '
                'a MongoDB.'
)

parser.add_argument('--back-until',
    help='The oldest month that should be scraped in the format "(m)m-yyyy". '
         f"Defaults to \"{config.BACK_UNTIL_DEFAULT}\".",
    dest='back_until',
    default=config.BACK_UNTIL_DEFAULT,
    type=auxiliary_functions.year_and_month_from_string
)

parser.add_argument('--up-from',
    help='The latest month that should be scraped in the format "(m)m-yyyy". '
         f"Defaults to the current month.",
    dest='up_from',
    default=auxiliary_functions.current_month_year_string(),
    type=auxiliary_functions.year_and_month_from_string
)

parser.add_argument('--database-name',
    help='Name of the MongoDB database the scraped exchange rates should be '
        f"stored in. Defaults to \"{config.MONGO_DATABASE_NAME}\"",
    dest='database_name',
    default=config.MONGO_DATABASE_NAME
)

parser.add_argument('--stop-if-known',
    help='If set, stops after encountering rates that are already known.',
    dest='stop_if_known',
    action='store_true'
)

parser.add_argument('--quiet',
    help='If set, the program will not log any information to STDOUT. '
        'Defaults to "False".',
    dest='quiet',
    action='store_true'
)

parser.set_defaults(stop_if_known=False, quiet=False)


"""
Start scraping.
"""
# Get script arguments.
args = parser.parse_args()

# Order scraping.
imf_scraper = IMFScrapingOrganizer(
    chromedriver_url=config.CHROMEDRIVER_URL,
    mongo_db_url=config.MONGO_DB_URL,
    mongo_database_name=args.database_name,
    exchange_rates_table=config.EXCHANGE_RATES_TABLE_NAME,
    pauses=config.PAUSES_BETWEEN_PAGE_VISITINGS,
    quiet=args.quiet
)

imf_scraper.scrape_exchange_rates_between(
    args.back_until,
    args.up_from,
    stop_if_known=args.stop_if_known
)
