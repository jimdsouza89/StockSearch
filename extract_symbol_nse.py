'''
@author: Jim D'Souza

Description : Finding the tickers of a list of companies on the NSE (National Stock Exchange of India)
Scrapes Yahoo Finance.
'''


import udf;
import csv;
import httplib2;

path = "D:\\Web Scraper\\TwitterStockSearch\\Stocks\\Data\\"
nse = "nse_211014.csv"

headers = httplib2.Http(".cache")

### Create your list of companies here###
file = open(path + nse, "r");
reader = csv.reader(file, delimiter = ",")

symbols = [];

rownum = 0;

for row in reader:
    if rownum > 0:
        series = row[1];
        symbol = row[0];

        iter = 0;

        while iter < 3:
            y_symbol = "";
            if series == "EQ":
                url = "http://finance.yahoo.com/q?s=" \
                      + symbol.replace("&", "%26").strip() \
                      + "-EQ.NS";
                resp, content = headers.request(url, "GET");
                y_list = udf.extract_ysymbol(content);

                if len(y_list) > 1:
                    y_symbol = y_list[0];
                else:
                    url = "http://finance.yahoo.com/q?s=" \
                          + symbol.replace("&", "%26").strip() \
                          + ".NS";
                    resp, content = headers.request(url, "GET");
                    y_list = udf.extract_ysymbol(content);

                    if len(y_list) > 1:
                        y_symbol = y_list[0];
                    else:
                        url = "http://finance.yahoo.com/q?s=" \
                              + symbol[0:9].replace("&", "%26").strip() \
                              + ".NS";
                        resp, content = headers.request(url, "GET");
                        y_list = udf.extract_ysymbol(content);

                        if len(y_list) > 1:
                            y_symbol = y_list[0];
                        else:
                            y_symbol = "";
            else:
                url = "http://finance.yahoo.com/q?s=" \
                      + symbol.replace("&", "%26").strip() \
                      + "-" + series.strip() + ".NS";
                resp, content = headers.request(url, "GET");
                y_list = udf.extract_ysymbol(content);

                if len(y_list) > 1:
                    y_symbol = y_list[0];
                else:
                    url = "http://finance.yahoo.com/q?s=" \
                          + symbol.replace("&", "%26").strip() \
                          + ".NS";
                    resp, content = headers.request(url, "GET");
                    y_list = udf.extract_ysymbol(content);

                    if len(y_list) > 1:
                        y_symbol = y_list[0];
                    else:
                        url = "http://finance.yahoo.com/q?s=" \
                              + symbol[0:9].replace("&", "%26").strip() \
                              + ".NS";
                        resp, content = headers.request(url, "GET");
                        y_list = udf.extract_ysymbol(content);

                        if len(y_list) > 1:
                            y_symbol = y_list[0];
                        else:
                            y_symbol = "";

            print "%i:try no %i" %(rownum, (iter+1));

            if y_symbol == "":
                iter += 1;
            else:
                iter = 3;

        symbols.append([symbol, y_symbol]);

    rownum += 1;

outfile = open(path + "yahoo_nse.csv", "w");
for row in symbols:
    outfile.write(",".join(row) + "\n");
