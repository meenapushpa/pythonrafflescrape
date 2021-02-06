import requests
import json
import re
import bs4 as bs
import datetime
import calendar
import itertools
import cfscrape
import ssl
from lxml.html import fromstring
from requests.auth import HTTPProxyAuth
import cloudscraper
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from requests.packages.urllib3.poolmanager import PoolManager

#log method is used to print the raffle logs with date and time
def log(event):
    d = datetime.datetime.now().strftime("%x %H:%M:%S")
    print("[Raffle Logs] :: " + str(d) + " :: " + event)
#Raffle class is used to read the proxies and parse them to allow raffle proxies
class Raffle(object):
    file_proxies = "/root/proxies.txt"
    def __init__(self):
        self.r = requests.session()
        self.i = 10
        self.headers = {
            ':authority': 'www.nakedcph.com',
            ':method': 'GET',
            ':path': '/xx/904/nike-dunk-hi-retro-prm-fcfs-raffle',
            ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'host': 'nakedcph.com'
            }
        self.json_headers = {
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
            }
#freeproxylist method is used to search the proxies from internet(online)
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
#read_proxies method is used to read the proxies from the file(manually)
    def read_proxies(file_path):
        with open(file_path) as txt_file:
            proxies = txt_file.read().splitlines()
        return proxies

    proxies = read_proxies(file_proxies)
    proxy_swm = itertools.cycle(proxies)#itertools is used to iterate through proxies in the list
#proxy_parse method is used to split the username,ip,port,password from online and manual list
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
#get_csrf is used to get the anticsrftoken in order to send the token along with the fields
    def get_csrf(self,url,proxy,auth=None):
        page = self.r.get(url, headers = self.headers, proxies={"http": proxy, "https": proxy}, auth=auth, verify=False, timeout=10)
        log(page.text)
        soup = bs.BeautifulSoup(page.text, 'lxml')
        log('Scraping csrf token')
        csrf = soup.find('input', {'name': '_AntiCsrfToken'}).get('value')
        log(csrf)
        return csrf
#raffle_entry is used to enter the raffle(form) to fill the fields
    def raffle_entry(self,url,proxy,auth=None):
        try:
            log('Entering raffle')
            #raffle_token = self.r.get(url,headers = self.headers, proxies={"http": proxy, "https": proxy}, auth=auth, verify=False, timeout=10)
            #raffle_token = str(raffle_token.text)
            #cloudscrapper module is used to bypass the proxies to reach the url
            scraper = cloudscraper.create_scraper(debug=True)#create_scrapper will return the cloudscrapper instance
            response= scraper.get(url, proxies={"http": proxy, "https": proxy})
            print(response)
            #payload is used to send the data to request module
            """payload = {
                'form[language]': 'en',
                'form[textfield:FhF0pPr4gdHO]': fname,
                'form[textfield:HjWDPHuvQXDW]': lname,
                'form[email:xS8rv0ZpuFDg]': email,
                'form[dropdown:PzvBvJMvRXrd]': country,
                'form[landed_at]': '{}'.format(calendar.timegm(time.gmtime())),
                'form[token]': raffle_token,
            }
            submit = r.post(url, headers = self.headers, proxies={"http": proxy, "https": proxy}, auth=auth, verify=False, timeout=10)
            log(submit.text)"""
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
    #user need to enter the option to search proxies via manually or online
    option=input("Enter the proxy type [Manual/Online]: ")
    if option == "Manual":
        #iterate through manual proxy list
        for rafflesubmit in range(ra.i):
            proxy = next(ra.proxy_swm)
            #parse the proxy from manual list using proxy_parse method
            proxyparse, httpauth = ra.proxy_parse(proxy)
            log('Using the PROXY [ ' + proxyparse + '] for the raffle entries')
            #pass the url,proxies to enter the url
            ra.raffle_entry(url,proxyparse,httpauth)
            ra.r.cookies.clear()
    elif option == "Online":
        #search and iterate through online proxies
        freeproxy = ra.freeproxylist()
        print(freeproxy)
        for freelist in freeproxy:
            #parse the proxy from online using proxy_parse method
            freeproxyparse, freehttpauth = ra.proxy_parse(freelist)
            log('Using the PROXY [ ' + freeproxyparse + '] for the raffle entries')
            #pass the url,proxies to enter the url
            ra.raffle_entry(url,freeproxyparse)
            ra.r.cookies.clear()
    else:
        log("Please choose either Manual or Online proxy")
