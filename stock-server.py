#!/usr/bin/env python

# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
KMyMoney Stock Server

A simple http server to be a single Online Quote Source for stock market info for KMyMoney.
-------------------

Run as a regular python script:
$ ./server.py
"""

import time
import sys
import requests
from datetime import datetime
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

br_stock_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{code}.SA?formatted=true&crumb=5zlPOxz.vH.&lang=pt-BR&region=BR&modules=price'
usa_stock_url = 'https://query1.finance.yahoo.com/v8/finance/chart/{code}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
currency_url = 'https://query1.finance.yahoo.com/v8/finance/chart/{code}=X'

ignore_urls = ['/favicon.ico']

def handle_br_stock(json, status_code):
    return (json.get('quoteSummary').get('result')[0].get('price').get('regularMarketPrice').get('raw'), status_code)
    
def handle_currency(json, status_code):
    return (json.get('chart').get('result')[0].get('meta').get('regularMarketPrice'), status_code)
    
def handle_usa_stock(json, status_code):
    return (json.get('chart').get('result')[0].get('meta').get('regularMarketPrice'), status_code)
    
    

class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if '/stock/br' in self.path:
                url = br_stock_url
                process_fn = handle_br_stock
            elif '/stock/usa' in self.path:
                url = usa_stock_url
                process_fn = handle_usa_stock
            elif '/currency' in self.path:
                url = currency_url
                process_fn = handle_currency
            elif self.path in ignore_urls:                
                return
            else:
                print "'%s' not found!" % str(self.path) 
                return
                
            code = self.path.split('/')[-1]
            price, status_code = self.get_info(url, code, process_fn)
            response = "{}|{}".format(price, datetime.now().strftime('%Y-%m-%d'))
            self.send(response, status_code)
            
        
        def send(self, response, status_code):
            self.send_response(status_code)                          
            self.send_header('Content-length',str(len(response)))
            self.send_header('Content-Type','text/plain')
            self.end_headers()
            self.wfile.write(response)
            
        def get_info(self, url, code, process_fn):
            url = url.replace('{code}', code)
            print "Getting Stock info... url=%s" % url
            sys.stdout.flush()
            resp = requests.get(url)
            print "Request done!"
            sys.stdout.flush()
            if(resp.status_code == 200):
                return process_fn(resp.json(), 200)                
            else:
                return ("", 404)
            



def main():
    host = '0.0.0.0'
    port = 1203
    httpd = HTTPServer((host, port), SimpleHandler)

    print time.asctime(), 'Server Starts - %s:%s' % (host, port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print time.asctime(), 'Server Stops - %s:%s' % (host, port)


if __name__ == '__main__':
    main()

