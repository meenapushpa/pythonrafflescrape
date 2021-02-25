import requests
import json
import js2py
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
import codecs
import bs4
import jinja2
from bs4 import BeautifulSoup


def log(event,val=None):
    d = datetime.datetime.now().strftime("%x %H:%M:%S")
    if val:
        print("[Raffle Logs] :: " + str(d) + " :: " + event +  " :: " + val)
    else:
        print("[Raffle Logs] :: " + str(d) + " :: " + event)

class Raffle(object):
    file_proxies = "/root/proxies.txt"
    def __init__(self):
        self.r = requests.session()
        self.debug=input("Do you want to see verbose logs ? [y/n] : ")
        if self.debug == 'y':
            self.scraper = cloudscraper.create_scraper(debug=True)
        else:
            self.scraper = cloudscraper.create_scraper()
        self.i = 10
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
        self.subscriber_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'host': 'app.rule.io',
            'referer': 'https://www.nakedcph.com/'
        }
    # function to call public available proxy from free-proxy-list and test the availability against google.com
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
    # function to read proxy list from the user input which takes from the line number 24
    def read_proxies(file_path):
        with open(file_path) as txt_file:
            proxies = txt_file.read().splitlines()
        return proxies
    # Iterating the proxy using itertools and next function to test one by one if we have many in input list / file
    proxies = read_proxies(file_proxies)
    proxy_swm = itertools.cycle(proxies)
    # function to parse the proxy value for requests module to process the https requests in offline
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
    # Extracting the required secrets from the targetted site using BeautifulSoup and cloudscraper module
    def get_sitekey(self,url,proxy,auth=None):
        page = self.scraper.get(url, proxies={"http": proxy, "https": proxy})
        soup = bs.BeautifulSoup(page.text, 'lxml')
        log('Scraping SiteKey token')
        signuplist = soup.find('button' ,attrs={"class": "g-recaptcha"})
        sitekey=signuplist['data-sitekey']
        return sitekey
    # Returns all form tags found on a web page's `url`
    def get_all_forms(self,url,proxy):
        res = self.scraper.get(url, proxies={"http": proxy, "https": proxy}).text
        soup = bs4.BeautifulSoup(res,features="html.parser")
        return soup.find_all("form")
    # Returns the HTML details of a form,including action, method and list of form controls (inputs, etc)
    def get_form_details(self,form):
        details = {}
        action = form.attrs.get("action").lower()
        method = form.attrs.get("method", "get").lower()

        buttonlist=[]
        buttonname = form.find('button')
        button_class = buttonname.attrs.get("class")
        button_callback = buttonname.attrs.get("data-callback")
        button_sitekey = buttonname.attrs.get("data-sitekey")
        button_value =buttonname.attrs.get("value", "")
        buttonlist.append({"class": button_class[0], "data-callback": button_callback,"data-sitekey":button_sitekey, "value": button_value})

        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value =input_tag.attrs.get("value", "")
            inputs.append({"type": input_type, "name": input_name, "value": input_value})

        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        details["button"] = buttonlist
        return details
    # Initial template of two captcha but not completed fully yet **** IN PROGRESS****
    def twocaptcha(self,sitekey,url):
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        api_key = os.getenv('APIKEY_2CAPTCHA', 'xxxxx')
        solver = TwoCaptcha(api_key)
        try:
            result = solver.recaptcha(
                sitekey=sitekey,
                url=url)
        except Exception as e:
            sys.exit(e)
        else:
            return str(result['code'])

    def render_jinja_html(self,template_loc,file_name,**context):
        store= jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_loc+'/')
        ).get_template(file_name).render(context)
        return store

    # function is to process raffle entries by using all the outputs from previous functions
    def raffle_entry(self,url,suburl,proxy,accounts,auth=None):
        try:
            log('Entering raffle URL')
            i=0
            tk= self.get_sitekey(url,proxy)
            first_form = self.get_all_forms(url,proxy)[0]
            form_details = self.get_form_details(first_form)
            buttonvalue = form_details["button"]
            selectvalue = form_details["select"]
            log("Resolving Captcha")
            gresp=self.twocaptcha(tk,url) # Resolving 2Captch here !
            data = {}
            for individual_list in accounts:
                log("Constructing payload for the", individual_list[5])
                for input_tag,value_tag in zip(form_details["inputs"],individual_list):
                    if input_tag["type"] == "hidden":
                        data[input_tag["name"]] = input_tag["value"]
                    elif input_tag["type"] != "submit":
                        data[input_tag["name"]] = value_tag
                for button_tag in buttonvalue:
                    if button_tag["class"] == "g-recaptcha":
                        data["g-recaptcha-response"]=gresp
                data['fields[Raffle.Country]']="GB"
                log("Sending payload to the requested URL")
                parsedata=json.dumps(data)
                url = urljoin(url, form_details["action"])
                submit = self.scraper.post(url,data=parsedata,headers=self.json_headers,proxies={"http": proxy, "https": proxy})
                if submit.status_code == 200:
                    log("Your registration was sucessfull !!")
                    i += 1
                else:
                    log("Failed to register !!")
                with codecs.open("output.txt", 'w',encoding='utf-8') as outfile: # writing a text file with the ouput for future reference,
                    outfile.write(submit.text)
                soup = BeautifulSoup(submit.content, "html.parser")
                open("submit.html", "w").write(str(soup)) # writing a html file with the ouput for future reference,
            return i
        except cloudscraper.exceptions.CloudflareChallengeError as err:
            pass
        except requests.exceptions.RequestException as err:
            print(err)
def fiil_and_submit_form(input):
    form=self.raffle_entry(url,suburl,proxyparse,accounts,httpauth)

if __name__ == '__main__':
    ra = Raffle()
    url = input("Enter the URL to scrape: ")# hardcoded for testing and wil be variablised once we fully done
    suburl = 'https://app.rule.io/subscriber-form/subscriber' # hardcoded for testing and wil be variablised once we fully done
    accounts = [
    [None,None,"xxxx@gmail.com", "xxxx", "+44 7830633285", "xxxx", "xxx", "Queens Road", "NE61 2TE", "WEST EDINGTON", "1", None,None,"1",None],
    ]
    option=input("Enter the proxy type [Manual/Online]: ")
    # Processing the modules based on user request
    if option == "Manual":
        for rafflesubmit in range(ra.i):
            proxy = next(ra.proxy_swm)
            proxyparse, httpauth = ra.proxy_parse(proxy)
            a,b,c,d = proxy.split(':')
            log('Using the PROXY [ ' + d + '] for the raffle entries')
            status=ra.raffle_entry(url,suburl,proxyparse,accounts,httpauth)
            ra.r.cookies.clear()
            if status == len(accounts):
                break;
    elif option == "Online":
        freeproxy = ra.freeproxylist()
        print(freeproxy)
        for freelist in freeproxy:
            freeproxyparse, freehttpauth = ra.proxy_parse(freelist)
            log('Using the PROXY [ ' + freeproxyparse + ' ] for the raffle entries')
            ra.raffle_entry(url,suburl,freeproxyparse,accounts)
            ra.r.cookies.clear()
    else:
        log("Please choose either Manual or Online proxy")
