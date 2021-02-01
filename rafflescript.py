import requests
import json
import re
import bs4 as bs
import datetime
import calendar
import itertools
import traceback
import cfscrape
from lxml.html import fromstring
from requests.auth import HTTPProxyAuth


def log(event):
    d = datetime.datetime.now().strftime("%x %H:%M:%S")
    print("[Raffle Logs] :: " + str(d) + " :: " + event)

class Raffle(object):
    file_proxies = "C:\\Users\\Administrator\\Documents\\Projects\\NakedCPH\\proxies.txt"
    def __init__(self):
        self.r = requests.session()
        self.i = 10
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'
            }
        self.json_headers = {
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54'
            }

    def freeproxylist(self):
        freeurl = 'https://free-proxy-list.net/anonymous-proxy.html'
        freeresponse = requests.get(freeurl)
        freeparser = fromstring(freeresponse.text)
        freeproxies = []
        for i in freeparser.xpath('//tbody/tr')[:20]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                freeproxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            try:
                t = requests.get("https://www.google.com/", proxies={"http": freeproxy, "https": freeproxy}, timeout=5)
                if t.status_code == requests.codes.ok:
                    freeproxies.append(freeproxy)
            except:
                pass
        return freeproxies

    def read_proxies(file_path):
        with open(file_path) as txt_file:
            proxies = txt_file.read().splitlines()
        return proxies

    proxies = read_proxies(file_proxies)
    proxy_swm = itertools.cycle(proxies)

    def proxy_parse(self,proxy):
        proxy_parts = proxy.split(':')
        if len(proxy_parts) == 2:
            ip, port = proxy_parts
            formatted_proxy = {
                'http': f'https://{ip}:{port}/',
            }
        elif len(proxy_parts) == 4:
            ip, port, user, password = proxy_parts
            formatted_proxy = {
                'http': f'https://{ip}:{port}/',
            }
            auth = HTTPProxyAuth(user, password)
        formatted_proxy = formatted_proxy['http']
        return formatted_proxy, auth

    def raffle_entry(self,proxy,auth=None):
        log("Entering raffle")
        raffle_token_request = 'https://www.nakedcph.com/en/898/nike-x-ambush-dunk-hi-cu7544-600-fcfs-raffle'
        """tokens, user_agent = cfscrape.get_tokens("https://www.nakedcph.com/en/898/nike-x-ambush-dunk-hi-cu7544-600-fcfs-raffle", proxies={"http": proxy, "https": proxy}, auth=auth, verify=False)"""
        raffle_token = self.r.get(raffle_token_request, headers = self.headers, proxies={"http": proxy, "https": proxy}, auth=auth, verify=False, timeout=10)
        raffle_token = str(raffle_token.status_code)
        print(raffle_token)
        """
        payload = {
            'form[language]': 'en',
            'form[textfield:FhF0pPr4gdHO]': fname,
            'form[textfield:HjWDPHuvQXDW]': lname,
            'form[email:xS8rv0ZpuFDg]': email,
            'form[dropdown:PzvBvJMvRXrd]': country,
            'form[landed_at]': '{}'.format(calendar.timegm(time.gmtime())),
            'form[token]': raffle_token,
        }
        raffle_url = 'URL'
        submit = r.post(raffle_url, headers = headers, data=payload, proxies={"http": proxy, "https": proxy})
        print(submit.text)
        """


if __name__ == '__main__':
    ra = Raffle()
    accounts = [
    {"fname":"pete","lname":"james","mail":"petejames@gmail.com","phone":"+33612334455","birthdate":"01/01/1998","shoesize":"42",},
    ]
    for rafflesubmit in range(ra.i):
        proxy = next(ra.proxy_swm)
        proxyparse, httpauth = ra.proxy_parse(proxy)
        freeproxy = ra.freeproxylist()
        for freelist in freeproxy:
            try:
                log('Using ' + freelist + ' for the registration and raffle entries')
                ra.raffle_entry(freelist)
                ra.r.cookies.clear()
                time.sleep(1)
            except:
                log("No luck, Trying next...")
