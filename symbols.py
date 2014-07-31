

import json
import sys
import urllib
import datetime
import os
import re

class YahooCSV:
    now = datetime.datetime.now()
    from_date = {
        'day': 1,
        'month': 1,
        'year': 2000,
    }
    until_date = {
        'day': now.day,
        'month': now.month,
        'year': now.year,
    }

    def set_from(self, month, day, year):
        self.from_date = {
            'day': day,
            'month': month,
            'year': year,
        }

    def set_until(self, month, day, year):
        self.until_date = {
            'day':  day,
            'month': month,
            'year': year,
        }

    def fetch_stock(self, stock):
        params = {
            'a': self.from_date.month,
            'b': self.from_date.day,
            'c': self.from_date.year,
            'd': self.until_date.month,
            'e': self.until_date.day,
            'f': self.until_date.year,
        }

        q = urllib.urlencode(params)
        url = "http://ichart.finance.yahoo.com/table.csv?%s" % q
        get = urllib2.urlopen(url)
        header = url_get.readline()


def fetch_industries():
    # Download JSON blob of all Yahoo Symbols and save as symbols.json:
    # http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.industry%20where%20id%20in%20(select%20industry.id%20from%20yahoo.finance.sectors)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&format=json
    # Open symbols file
    blob = open("symbols.json").read()
    # Json decode blob
    data = json.loads(blob)
    # Return industries list
    return data['query']['results']['industry']


def fetch_companies(industries, industry_ids=[]):
    companies = []
    company_symbols = []
    for industry in industries:
        industry_companies = []
        file_path = "symbols/" + industry['id'] + "_" + industry['name'].replace(" ", "_").replace("/", "-") + ".txt"
        print file_path
        if os.path.isfile(file_path):
            os.unlink(file_path)
        if 'company' in industry and 'id' in industry:
            # Restrict companies to certain industry (optional)
            if len(industry_ids) > 0 and int(industry['id']) not in industry_ids:
                continue
            for company in industry['company']:
                if isinstance(company, dict) == False:
                    continue
                if re.search(r'\.', company['symbol'], re.M|re.I):
                    continue
                companies.append(company)
                industry_companies.append(company['symbol'])
                company_symbols.append(company['symbol'])
            with open(file_path,'w+') as f:
                f.seek(0)
                while (len(industry_companies) > 0):
                    f.write (industry_companies.pop(0) + "\n")
    all_file_path = "symbols/100_All_Companies.txt"
    if os.path.isfile(all_file_path):
        os.unlink(all_file_path)
    with open(all_file_path,'w+') as f:
            f.seek(0)
            while (len(company_symbols) > 0):
                f.write (company_symbols.pop(0) + "\n")

    return companies




def main():
    print "\n\n-- Sharpefolio v0.0.1 --\n\n"

    # Check optional industry_id argument
    list_industries = False
    industry_ids = []
    if len(sys.argv) > 1:
        if sys.argv[1] == 'industries':
            list_industries = True
        else:
            industry_ids = [int(i) for i in sys.argv[1:]]

    industries = fetch_industries()

    if list_industries:
        for industry in industries:
            if 'company' in industry:
                print industry['id'], "-", industry['name']
                # print industry['id']
                industry['id']
        return

    companies = fetch_companies(industries, industry_ids)

    for company in companies:
        if 'symbol' in company and 'name' in company:
            # print company['symbol'], "-", company['name']
            # print company['symbol']
            print company['symbol']
            # print company['name']

    # print "\n", industry_ids, "\n"

if __name__ == '__main__':
    main()
