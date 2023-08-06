import logging
import argparse
from datetime import timedelta, datetime

from alphatools.backtesting_app import BackTestingApp

import instruments


class PriceArchiverStrat(BackTestingApp):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--underlying", nargs='+',
                        help="Instrument whose derivatives have to be recorded", required=True)
    args = parser.parse_args()
    strat = PriceArchiverStrat('/Users/jaskiratsingh/projects/smart-api-creds.ini')
    strat.set_start_date(datetime.now() - timedelta(days=1))
    strat.set_end_date(datetime.now() - timedelta(days=1))
    strat.logger.setLevel(logging.INFO)

    for underlying in args.underlying:
        nifty_token_list = instruments.get_derivatives(underlying)
        for token_info in nifty_token_list:
            token = token_info['token']
            exch_seg = token_info['exch_seg']
            strat.add_instrument(token, exch_seg)

    strat.load_data()
