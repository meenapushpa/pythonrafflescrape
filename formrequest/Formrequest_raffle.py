# -*- coding: utf-8 -*-
import scrapy
import json
import re
import logging
import requests
import json
from scrapy.http import FormRequest
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

from urllib.parse import urljoin
from scrapy.selector import Selector


class RafflescriptSpider(scrapy.Spider):
	name = 'rafflescript'
	allowed_domains = ['nakedcph.com']
	start_urls = ['https://www.nakedcph.com/xx/904/nike-dunk-hi-retro-prm-fcfs-raffle']

	def __init__(self):
		super(RafflescriptSpider, self).__init__()
	# Extracting the required secrets from the targetted site using BeautifulSoup and cloudscraper module
	def get_sitekey(self,auth=None):
		yield scrapy.Request('https://www.nakedcph.com/xx/904/nike-dunk-hi-retro-prm-fcfs-raffle',callback=get_sitekeyval)

	def get_sitekeyval(response):
		soup = bs.BeautifulSoup(response.text, 'lxml')
		log('Scraping SiteKey token')
		signuplist = soup.find('button' ,attrs={"class": "g-recaptcha"})
		sitekey=signuplist['data-sitekey']
		log('Scraping CSRF token')
		return sitekey


	# Returns all form tags found on a web page's `url`
	def get_all_forms(self):
		yield scrapy.Request('https://www.nakedcph.com/xx/904/nike-dunk-hi-retro-prm-fcfs-raffle',callback=get_allformsval)

	def get_allformsval(response):
		soup = bs4.BeautifulSoup(response,features="html.parser")
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
	def twocaptcha(self,sitekey):
		sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
		api_key = os.getenv('APIKEY_2CAPTCHA', ' 791a83d1333d48429227d52e1a153ea3')
		solver = TwoCaptcha(api_key)
		try:
			result = solver.recaptcha(sitekey=sitekey,url='https://www.nakedcph.com/xx/904/nike-dunk-hi-retro-prm-fcfs-raffle')
		except Exception as e:
			sys.exit(e)
		return str(result['code'])

	def parse(self,response):
		#tk= self.get_sitekey()
		data={'tags[]': '76713', 'token': 'c812c1ff-2a5a0fe-efad139-d754416-71e1e60-2ce', 'rule_email': 'wlslakshman@gmail.com', 'fields[Raffle.Instagram Handle]': 'Lakshmanan', 'fields[Raffle.Phone Number]': '+44 78 3063 3285', 'fields[Raffle.First Name]': 'Lakshmanan', 'fields[Raffle.Last Name]': 'S', 'fields[Raffle.Shipping Address]': "Queens Road", 'fields[Raffle.Postal Code]': "NE61 2TD", 'fields[Raffle.City]': "WEST EDINGTON", 'fields[Raffle.Signup Newsletter]': '1', 'fields[SignupSource.ip]': '192.0.0.1', 'fields[SignupSource.useragent]': 'Mozilla', 'email_field': '1', 'language': 'sv', 'g-recaptcha-response': '03AGdBq26csmo47MS8grr0txAzzqpIXHAw3euzZzQ4HDYOInPXZK5S9dOqeWvdmVLKLQXQV4A85v4fydOvXByN1_SQCQmo4EInwriPF1uwhNXBxC6deErcUy50pw_vGnllfYoqO3EbyjLZGaXGg1WB9vQgDYC_Ir_KyiUnCCnQE4QZyktAtk_oZwD4oJDeUbRxs40XSwVyqUl24OwTO1HXQCugT3VKudLNbOLHgyy0ZVd5JedsAKHBb0J-wTN7c3puW0sOKA8jsZ2CdUx_dPhH6NlbfrAn2orypPJvskYCQVZpBSoIZ6Gjgy0BWu7wcs43Z0Dl6HdDG3EN5cmZ-rLNgofkpxL6BoqBKJd37MS93Ny_nmIgnJMs-7r8pcZFmr32YsdRKWXzQjARKK8obWWWmkA4d62AEyLZdj7qmG_Q4cg_oN5Bepy8hntmWGXYXe-vVGIENdlLhEfYIwiq6TQlfjL8r248F2R_ZxJ_AEkUcyAz1_0ExEBajqP3_yatRcRHoErUTj2j8Qd-fX1qWmOvftFx6D761FgCNg'}
		"""first_form = self.get_all_forms()
		form_details = self.get_form_details(first_form)
		buttonvalue = form_details["button"]
		log("Resolving Captcha")
		gresp=self.twocaptcha(tk) # Resolving 2Captch here !
		data = {}
		for input_tag,value_tag in zip(form_details["inputs"]):
			if input_tag["type"] == "hidden":
				data[input_tag["name"]] = input_tag["value"]
			elif input_tag["type"] != "submit":
				data[input_tag["name"]] = value_tag
			for button_tag in buttonvalue:
				if button_tag["class"] == "g-recaptcha":
					data["g-recaptcha-response"]=gresp
			data['fields[Raffle.Country]']="GB" """
		yield FormRequest.from_response(response,formnumber=1,formdata=data,clickdata={'name': 'Sign up!'})
