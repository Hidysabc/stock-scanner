#!/usr/bin/env python
"""

Usage:
    scan_stocks.py --f filename.json --span timespan --logging info/debug/warn
    --apikey apikey.json
    ex: ./scan_stocks.py --f "stock_watchlist.json" --span 90 --logging debug

    --f: filename storing the list of hold and behold stocks
         (Default:"stock_watchlist.json")
    --span: Time span to trace back in days (Default: 90 days)

    --apikey: filepath containing apikey for Alphavantage service
"""

import argparse
import logging
import numpy as np
import os
import datetime
import json
from alphavantage import get_historical_prices, get_price

FORMAT = '%(asctime)-15s %(name)-8s %(levelname)s %(message)s'
LOG_MAP = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warn": logging.WARNING
}
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stock_scanner')


def two_sigma(symbol,end_date, span, apikey_filename):
    # end_date represents day closer to the present
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    start_date_parse = end_date_parse -datetime.timedelta(span)
    close = get_historical_prices(symbol,end_date, str(start_date_parse), apikey_filename)
    span_avg = close.mean()
    span_std = close.std()
    two_sigma_above = span_avg + span_std*2
    two_sigma_below = span_avg - span_std*2
    logger.info('SYMBOL: {}'.format(symbol))
    logger.info('{} day average: {:.2f}'.format(span, span_avg))
    logger.info('2 sigma above: {:.2f}'.format(two_sigma_above))
    logger.info('2 sigma below: {:.2f}'.format(two_sigma_below))

    return symbol, span_avg, two_sigma_above, two_sigma_below

class SuggestStock(object):
    def __init__(self, sym, p):
        self.symbol = sym
        self.todays_price = p


class SuggestBuy(SuggestStock):
    def __init__(self, sym, p, two_sig_p):
        super(SuggestBuy, self).__init__(sym, p)
        self.two_sigma_below = two_sig_p

class SuggestSell(SuggestStock):
    def __init__(self, sym, p, two_sig_p):
        super(SuggestSell, self).__init__(sym, p)
        self.two_sigma_above = two_sig_p



def read_stock_list(fname, span, apikey_filename):
    symbol_dict = json.load(open(fname,"r"))
    suggest_selling_list = []
    suggest_buying_list = []

    for i in symbol_dict:
        if i == "HOLD":
            logger.info("Query held stocks...")
            for j in symbol_dict[i]:
                symbol = j
                logger.debug(symbol)
                end_date = str(datetime.datetime.today().date())
                symbol_name,span_avg,two_sigma_above,two_sigma_below = two_sigma(symbol,end_date, span, apikey_filename)
                symbol_current_price = np.float(get_price(symbol, apikey_filename))
                if symbol_current_price >= two_sigma_above:
                    suggest_selling_list.append(
                        SuggestSell(symbol, symbol_current_price,
                                    two_sigma_above)
                    )
        elif i == "BEHOLD":
            logger.info("Query stocks in watchlist...")
            for j in range(len(symbol_dict[i])):
                symbol = symbol_dict[i][j]
                logger.debug(symbol)
                end_date = str(datetime.datetime.today().date())
                symbol_name, span_avg, two_sigma_above, two_sigma_below = two_sigma(symbol, end_date, span, apikey_filename)
                symbol_current_price = np.float(get_price(symbol, apikey_filename))
                if symbol_current_price <= two_sigma_below:
                    suggest_buying_list.append(
                        SuggestBuy(symbol, symbol_current_price,
                                   two_sigma_below)
                    )
    return suggest_selling_list, suggest_buying_list


def main(args):
    fname = args.f
    span = args.span
    apikey_filename = args.apikey
    logger.setLevel(LOG_MAP[args.logging.lower()])
    suggest_selling_list, suggest_buying_list = read_stock_list(fname, span, apikey_filename)
    if suggest_selling_list:
        logger.info("Suggest stocks to sell")
        for ss in suggest_selling_list:
            logger.info("{sym}: {p} ({two_sig})".format(
                sym=ss.symbol,
                p=ss.todays_price,
                two_sig=ss.two_sigma_above
            ))
    else:
        logger.info("No stock to sell.")
    if suggest_buying_list:
        logger.info("Suggest stocks to buy")
        for sb in suggest_buying_list:
            logger.info("{sym}: {p} ({two_sig})".format(
                sym=sb.symbol,
                p=sb.todays_price,
                two_sig=sb.two_sigma_below
            ))
    else:
        logger.info("No stock to buy.")

    logger.info("Done :)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--f",
        metavar="FNAME",
        type=str,
        help = "File for reading data (xxx.json)",
        default = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "stock_watchlist.json")
    )
    parser.add_argument(
        "--span",
        metavar="SPAN",
        type=int,
        help = "Time span to trace back in days",
        default = 90
    )
    parser.add_argument(
        "--logging",
        metavar="LOG_LEVEL",
        type=str,
        help = "Log level",
        default = "info"
    )
    parser.add_argument(
        "--apikey",
        metavar="APIKEY_FILENAME",
        type=str,
        help = "File path containing API key",
        default = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "apikey.json")
    )
    args = parser.parse_args()
    main(args)
