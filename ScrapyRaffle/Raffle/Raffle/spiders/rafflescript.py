import re
import bs4 as bs
import datetime
import calendar
import itertools
import ssl
from lxml.html import fromstring
from requests.auth import HTTPProxyAuth
import sys
import os
from twocaptcha import TwoCaptcha
import codecs
import bs4
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from urllib.parse import urljoin
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser

class RafflescriptSpider(scrapy.Spider):
        name = 'rafflescript'
        allowed_domains = ['nakedcph.com']
        start_urls = ["https://app.rule.io/subscriber-form/subscriber"]

        def parse(self,response):
                data={'tags[]': '76713', 'token': 'c812c1ff-2a5a0fe-efad139-d754416-71e1e60-2ce', 'rule_email': 'priyalakshman15@gmail.com', 'fields[Raffle.Instagram Handle]': 'Lakshmanan', 'fields[Raffle.Phone Number]': '+44 78 3063 3285', 'fields[Raffle.First Name]': 'Lakshmanan', 'fields[Raffle.Last Name]': 'S', 'fields[Raffle.Shipping Address]': "Queens Road", 'fields[Raffle.Postal Code]': "NE61 2TD", 'fields[Raffle.City]': "WEST EDINGTON", 'fields[Raffle.Signup Newsletter]': '1', 'fields[SignupSource.ip]': '192.0.0.1', 'fields[SignupSource.useragent]': 'Mozilla', 'email_field': '1', 'language': 'sv', 'g-recaptcha-response': '03AGdBq26csmo47MS8grr0txAzzqpIXHAw3euzZzQ4HDYOInPXZK5S9dOqeWvdmVLKLQXQV4A85v4fydOvXByN1_SQCQmo4EInwriPF1uwhNXBxC6deErcUy50pw_vGnllfYoqO3EbyjLZGaXGg1WB9vQgDYC_Ir_KyiUnCCnQE4QZyktAtk_oZwD4oJDeUbRxs40XSwVyqUl24OwTO1HXQCugT3VKudLNbOLHgyy0ZVd5JedsAKHBb0J-wTN7c3puW0sOKA8jsZ2CdUx_dPhH6NlbfrAn2orypPJvskYCQVZpBSoIZ6Gjgy0BWu7wcs43Z0Dl6HdDG3EN5cmZ-rLNgofkpxL6BoqBKJd37MS93Ny_nmIgnJMs-7r8pcZFmr32YsdRKWXzQjARKK8obWWWmkA4d62AEyLZdj7qmG_Q4cg_oN5Bepy8hntmWGXYXe-vVGIENdlLhEfYIwiq6TQlfjL8r248F2R_ZxJ_AEkUcyAz1_0ExEBajqP3_yatRcRHoErUTj2j8Qd-fX1qWmOvftFx6D761FgCNg'}
                yield FormRequest.from_response(response,formnumber=1,formdata=data,clickdata={'name': 'Sign up!'},callback=self.parse1)

        def parse1(self,response):
                data = json.loads(response.body)
                print(data)
                open_in_browser(response)

                pass
