# Stock Scanner for Over-fluctuated Stocks

A simple application that queries stocks of interests and return the name of 
stocks whose fluctuation exceeded a certain moving standard deviation. 

## Installation

The script use `ystockquote` package. To install, do:

```bash
pip install ystockquote
```

The package contains a sample json file listing stocks of interest. Stocks in
`HOLD` are stocks the user currently holding, and their day of purchase.
Stocks in `BEHOLD` are stocks to watch out for possible buy. To try out, 
simply rename the sample file `stock_watchlist.sample.json` to `stock_watchlist.json`. Then run

```bash
python scan_stocks.py
```

Without any argument, the script will look for the file named
 `stock_watchlist.json` in the same directory where `scan_stocks.py` resides.
You can also point the script to the file by assigning the `-f` option.

```bash
$ python scan_stocks.py -h
usage: scan_stocks.py [-h] [--f FNAME] [--span SPAN] [--logging LOG_LEVEL]

Usage: scan_stocks.py --f filename.json --span timespan --logging
info/debug/warn ex: ./scan_stocks.py --f "stock_watchlist.json" --span 90
--logging debug --f: filename storing the list of hold and behold stocks
(Default:"stock_watchlist.json") --span: Time span to trace back in days
(Default: 90 days)

optional arguments:
  -h, --help           show this help message and exit
  --f FNAME            File for reading data (xxx.json) (default:
                       stock_watchlist.json)
  --span SPAN          Time span to trace back in days (default: 90)
  --logging LOG_LEVEL  Log level (default: info)
```


