import requests
import json
import re
import bs4 as bs
import datetime
import calendar
import itertools
import ssl
from lxml.html import fromstring
from requests.auth import HTTPProxyAuth
import cloudscraper
import sys
import os
from twocaptcha import TwoCaptcha



def log(event):
    d = datetime.datetime.now().strftime("%x %H:%M:%S")
    print("[Raffle Logs] :: " + str(d) + " :: " + event)

class Raffle(object):
    file_proxies = "/root/proxies.txt"
    def __init__(self):
        self.r = requests.session()
        self.scraper = cloudscraper.create_scraper()
        self.i = 5
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
            }
        self.json_headers = {
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
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
                'http': f'http://{ip}:{port}/',
            }
            auth=None
        elif len(proxy_parts) == 4:
            ip, port, user, password = proxy_parts
            formatted_proxy = {
                'http': f'http://{user}:{password}@{ip}:{port}/',
            }
            auth=None
        formatted_proxy = formatted_proxy['http']
        return formatted_proxy, auth

    def get_sitekey(self,url,proxy,auth=None):
        page = self.scraper.get(url, proxies={"http": proxy, "https": proxy})
        soup = bs.BeautifulSoup(page.text, 'lxml')
        log('Scraping token')
        formlist =  soup.find('input' ,attrs={"name":"token"})
        sitetoken = formlist['value']
        log('Scraping SiteKey token')
        signuplist = soup.find('button' ,attrs={"class":"g-recaptcha"})
        sitekey=signuplist['data-sitekey']
        return sitekey, sitetoken

    def twocaptcha(self,sitekey,url):
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        api_key = os.getenv('APIKEY_2CAPTCHA', 'YOUR_API_KEY')
        log(api_key)
        solver = TwoCaptcha(api_key)
        try:
            result = solver.recaptcha(
                sitekey=sitekey,
                url=url)
        except Exception as e:
            sys.exit(e)
        else:
            print('Solved: ' + str(result))

    def raffle_entry(self,url,proxy,auth=None):
        try:
            log('Entering raffle')
            tk, siky = self.get_sitekey(url,proxy)
            payload = {
                'tags[]': '75612',
                'token': '{}'.format(tk),
                'rule_email': 'petejames@gmail.com',
                'fields[Raffle.Instagram Handle]': 'pete',
                'fields[Raffle.Phone Number]': '+33612334455',
                'fields[Raffle.First Name]': 'pete',
                'fields[Raffle.Last Name]': 'james',
                'fields[Raffle.Shipping Address]': '76 rue Porte dOrange',
                'fields[Raffle.Postal Code]': '97300',
                'fields[Raffle.City]': 'Cayenne',
                'fields[Raffle.Country]': 'FR',
                'fields[SignupSource.ip]': '192.0.0.1',
                'fields[SignupSource.useragent]': 'Mozilla'
            }
            submit = self.scraper.post(url,headers=self.headers,data=payload,proxies={"http": proxy, "https": proxy})
            log(submit.status_code)
            with open("output.txt", 'w') as outfile:
                outfile.write(submit.text)
            log("Successfuly completed the transaction!")
        except requests.exceptions.RequestException as err:
            print(err)
            pass

if __name__ == '__main__':
    ra = Raffle()
    url = 'https://www.nakedcph.com:443/xx/904/nike-dunk-hi-retro-prm-fcfs-raffle'
    accounts = [
    {"fname":"pete","lname":"james","mail":"petejames@gmail.com","phone":"+33612334455","birthdate":"01/01/1998","shoesize":"42",},
    ]
    option=input("Enter the proxy type [Manual/Online]: ")
    if option == "Manual":
        for rafflesubmit in range(ra.i):
            proxy = next(ra.proxy_swm)
            proxyparse, httpauth = ra.proxy_parse(proxy)
            log('Using the PROXY [ ' + proxyparse + '] for the raffle entries')
            ra.raffle_entry(url,proxyparse,httpauth)
            ra.r.cookies.clear()
    elif option == "Online":
        freeproxy = ra.freeproxylist()
        print(freeproxy)
        for freelist in freeproxy:
            freeproxyparse, freehttpauth = ra.proxy_parse(freelist)
            log('Using the PROXY [ ' + freeproxyparse + '] for the raffle entries')
            ra.raffle_entry(url,freeproxyparse)
            ra.r.cookies.clear()
    else:
        log("Please choose either Manual or Online proxy")

