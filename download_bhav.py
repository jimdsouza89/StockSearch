'''
@author: Jim D'Souza

Description : Download the list of BSE and NSE companies from this link
'''

import udf;

path = "D:/Web Scraper/TwitterStockSearch/Stocks/Data/";

udf.bhavcopy_bse(udf.last_working_day(), path, "bse");
udf.bhavcopy_nse(udf.last_working_day(), path, "nse");
