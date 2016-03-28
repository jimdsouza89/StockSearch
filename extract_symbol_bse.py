'''
@author: Jim D'Souza

Description : Finding the tickers of a list of companies on the BSE (Bombay Stock Exchange)
Scrapes Yahoo Finance.
'''

import udf;
import csv;
import httplib2;
import re;

path = "D:\\Web Scraper\\TwitterStockSearch\\Stocks\\Data\\";
bse = "bse_211014.csv";

headers = httplib2.Http(".cache");

### Create your list of companies here###
file = open(path + bse, "r");
reader = csv.reader(file, delimiter = ",");

symbols = [];
rownum = 0;
for row in reader:
    if rownum > 0:
        symbol1 = row[0];
        symbol2 = row[1];
        m = re.findall("\w", symbol2);
        symbol2 = "".join(m);

        iter = 0;
        while iter < 3:
            y_symbol = "";
            url = "http://finance.yahoo.com/q?s=" \
                  + symbol1.replace("&", "%26").strip() \
                  + ".BO";
            resp, content = headers.request(url, "GET");
            y_list = udf.extract_ysymbol(content);

            if len(y_list) > 1:
                y_symbol = y_list[0];
            else:
                url = "http://finance.yahoo.com/q?s=" \
                      + symbol2.replace("&", "%26").strip() \
                      + ".BO";
                resp, content = headers.request(url, "GET");
                y_list = udf.extract_ysymbol(content);

                if len(y_list) > 1:
                    y_symbol = y_list[0];
                else:
                    y_list = "";

            if y_symbol == "":
                iter += 1;
            else:
                c_symbol = udf.extract_changed(content);
                if c_symbol != "":
                    y_symbol = c_symbol;
                iter = 3;

        # print "%s, %s, %s" % (symbol1, symbol2, y_symbol);
        symbols.append([symbol1, symbol2, y_symbol]);

    rownum += 1;

# print symbols;
outfile = open(path + "yahoo_bse.csv", "w");
for row in symbols:
    outfile.write(",".join(row) + "\n");
