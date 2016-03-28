'''
Created on Jul 24, 2014

@author: Jim D'Souza

Description : Reads csv file for list of companies, and downloads stock market data for that company
'''


import csv;
import zipfile;
import datetime;
import StringIO;
import httplib;

def read_csv(path, filename):
    reader = csv.reader(open(path + filename, "r"), delimiter = ",");
    return reader;

def last_working_day():
    dt = datetime.date.today();
    break_var = 0;

    while break_var == 0:
        dt = dt + datetime.timedelta(days=-1);
        if dt.weekday() != 5 and dt.weekday() != 6:
            break_var = 1;

    return dt;

def bhavcopy_bse(date, path, filename):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) '
                            + 'AppleWebKit/534.7 (KHTML, like Gecko) '
                            + 'Chrome/7.0.517.44 Safari/534.7',
               'Accept':'application/xml,application/xhtml+xml,text/html;q=0.9,'
                        + 'text/plain;q=0.8,image/png,*/*;q=0.5',
               'Accept-Encoding':'gzip,deflate,sdch',
               'Referer':'http://www.bseindia.com'};
    url = "www.bseindia.com";
    reqstr = "/download/BhavCopy/Equity/EQ" \
          + str(date.strftime("%d%m%y")) + "_CSV.ZIP";

    conn = httplib.HTTPConnection(url);
    conn.request("GET", reqstr, None, headers);
    response = conn.getresponse();
    if response.status != 200:
        print "Response status != 200 \nCould not download";
        return;
    data = response.read()
    sdata = StringIO.StringIO(data)
    z = zipfile.ZipFile(sdata)
    csv = z.read(z.namelist()[0])
    outfile = path + filename + "_" \
              + str(last_working_day().strftime("%d%m%y")) + ".csv";
    if not csv:
        print "Could not download";
        return
    else:
        stream = open(outfile, "w");
        stream.write(csv);
        stream.close();

def bhavcopy_nse(date, path, filename):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) '
                            + 'AppleWebKit/534.7 (KHTML, like Gecko) '
                            + 'Chrome/7.0.517.44 Safari/534.7',
               'Accept':'application/xml,application/xhtml+xml,text/html;q=0.9,'
                        + 'text/plain;q=0.8,image/png,*/*;q=0.5',
               'Accept-Encoding':'gzip,deflate,sdch',
               'Referer':'http://www.nseindia.com/archives/archives.htm'};
    url = "www.nseindia.com";
    reqstr = "/content/historical/EQUITIES/" \
          + str(date.strftime("%Y")) + "/" \
          + str(date.strftime("%b")).upper() + "/" + "cm" \
          + str(date.strftime("%d%b%Y")).upper() + "bhav.csv.zip";

    conn = httplib.HTTPConnection(url);
    conn.request("GET", reqstr, None, headers);
    response = conn.getresponse();
    if response.status != 200:
        print "Response status != 200 \nCould not download";
        return;
    data = response.read()
    sdata = StringIO.StringIO(data)
    z = zipfile.ZipFile(sdata)
    csv = z.read(z.namelist()[0])
    outfile = path + filename + "_" \
              + str(last_working_day().strftime("%d%m%y")) + ".csv";
    if not csv:
        print "Could not download";
        return
    else:
        stream = open(outfile, "w");
        stream.write(csv);
        stream.close();

def extract_ysymbol(content):
    start = content.find("<title>");
    end = content.find("</title>");

    return content[start+7:end].split(":");

def extract_changed(content):
    chk = content.find("Changed Ticker Symbol");
    c_symbol = "";

    if chk >= 0:
        start = content.find("<a", chk+1);
        end = content.find("</a>", start);
        str = content[start:end+4];
        start = str.find(">");
        end = str.find("<", start);
        c_symbol = str[start+1:end];

    return c_symbol;

