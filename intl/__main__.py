import argparse, sys, os, time, traceback
import pandas as pd, numpy as np
from multiprocessing.dummy import Pool as ThreadPool
from app import *
from er import *
from trend import *
from fire import *


script_dir = os.path.dirname(__file__)
urls = os.path.join(script_dir, 'urls')
debug_log = os.path.join(script_dir, 'debug.log')

pool = ThreadPool(4)

# init objects
foreign = Foreign()
trend = Trend()
fire = Fire()
er = Er()


# iter through urls
def url_list():
    for the_url in fire.urls_stripped():
        print the_url


# scrape urls & use pandas to print the daily data
def overview_daily():
    foreign.scrape_multi(fire.urls_stripped())
    syms = [sym for sym in foreign.final_d]
    df = pd.DataFrame(syms, columns=['symbol', 'price', 'change', 'pct_change', 'high', 'low',  
    'volume', 'avg_volume', 'volume_pct_avg'])
    df = df.rename(columns={'symbol': 'Symbol', 'price': 'Price', 'change': 'Change', 'pct_change': 'Percent Change', 'high': 'High', 'low': 'Low', 
    'volume': 'Vol', 'avg_volume': 'Avg Vol', 'volume_pct_avg': '% Avg Vol'})
    df = df.sort_values('Symbol')
    df.index = np.arange(1, len(df) + 1)
    print df


# scrape urls & use pandas to print fundamental data
def overview_fundamentals():
    foreign.scrape_multi(fire.urls_stripped())
    syms = [sym for sym in foreign.final_f]
    df = pd.DataFrame(syms, columns=['symbol', 'country', 'currency', 'exchange', 'er',   
    'pe ratio', 'yield'])
    df = df.rename(columns={'symbol': 'Symbol', 'country': 'Country', 'currency': 'Currency', 'exchange': 'Exchange', 
    'er': 'Earnings Date', 'pe ratio': 'PE (TTM)', 'yield': 'Yield'})
    df = df.sort_values('Symbol')
    df.index = np.arange(1, len(df) + 1)
    print df


# argparse logic
def main():
    ap = argparse.ArgumentParser()

    ap.add_argument('-u', '--urls',
    help='List all urls to pull data from.',
    action='store_true')

    ap.add_argument('-vd', '--viewdaily',
    help='View daily price data of all symbols in the list.',
    action='store_true')

    ap.add_argument('-vf', '--viewfunds',
    help='View fundamental data of all symbols in the list.',
    action='store_true')

    ap.add_argument('-t', '--trending', 
    help='View trending symbols that traders are discussing.',
    action='store_true')

    ap.add_argument('-a', '--addu', type=str, nargs='*',
    help='Add URL to list.')

    ap.add_argument('-r', '--removeu', type=str, nargs='*',
    help='Remove URL by symbol. (ie: intl -r san)')

    ap.add_argument('-er', '--earnings', type=str, nargs='*',
    help='Find the earnings date for tickers.')

    ap.add_argument('-c', '--clear',
    help='Clear list of URLs.',
    action='store_true')

    args = ap.parse_args()

    if args.viewdaily:
        overview_daily()

    if args.viewfunds:
        overview_fundamentals()
    
    if args.earnings:
        er.er_multi(args.earnings)

    if args.urls:
        url_list()

    if args.trending:
        trend.trending_print()
    
    if args.addu:
        fire.add_url(args.addu)
    
    if args.removeu:
        fire.remove_url(args.removeu)
    
    if args.clear:
        fire.clear_urls()


if __name__ == '__main__':
    _start = time.time()

    print ""

    try:
        main()
        
    except Exception as e:
        with open(debug_log, 'a') as d:
            now = time.ctime()
            msg = "{}: {}\n\n{}\n\n".format(now, e, traceback.format_exc())
            d.write(msg)
    
    _end = time.time()

    print ""
    # print (float(_end) - float(_start))
