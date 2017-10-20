#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Login in website Linkedin
@autor Marcos Magno
@Email marcosf40@hotmail.com
 
Depedences:
pip install selenium==2.43.0
pip install webdriver
 
Note.: Version of the Firefox: <= 45.0
 
'''
 
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
from logging.config import fileConfig

 
 
class dataSearch():
	"""def construct"""
	 
	def __init__(self):
		self.fp = webdriver.FirefoxProfile()
		self.browser = webdriver.Firefox(firefox_profile=self.fp)
		self.browser.set_window_size(1068, 1050)
		self.browser.get("https://www.linkedin.com/uas/login?session_redirect=%2Fschool%2F636119%2Falumni%2F&fromSignIn=true&trk=uno-reg-join-sign-in") 
		time.sleep(2)
		
		#https://www.linkedin.com/search/results/companies/?origin=SWITCH_SEARCH_VERTICAL&q=jserpAll
		

	def login(self):
		 
		self.username = self.browser.find_element_by_id("session_key-login") # field of login
		self.password = self.browser.find_element_by_id("session_password-login") # filed of password
		self.username.send_keys("jonasfissicaro@hotmail.com") # change your e-mail
		self.password.send_keys("Ib!turun@1320") # change your password
		self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
		self.login_attempt.submit() #apply button submit
		time.sleep(3)
		
 
	def search(self):
		self.url = []
		self.linkProfile = "https://www.linkedin.com/search/results/companies/"
		self.lista_empresa = []
		self.lista_empresa_func = []
 
		#self.browser.execute_script("window.open()")
		#self.browser.switch_to.window(self.browser.window_handles[1])
		self.browser.get(self.linkProfile)
		self.browser.execute_script("window.scrollTo(0, 1024)")
 
		try:
			self.all_spans = self.browser.find_elements_by_xpath("//a[@class='search-result__result-link ember-view']")
				
			#self.url = self.browser.find_elements_by_xpath("//a[@href]")

		except NoSuchElementException:
			logging.info("Close browse:")
			logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
			return
		time.sleep(5)
				
		# Get DIV
		for self.span in self.all_spans:
			#print "....."
			print self.span.get_attribute("id")
			self.lista_empresa.append(str(self.span.get_attribute("href")))
			#print self.lista_empresa

		for i in self.lista_empresa:
			self.browser.get(i)

		'''	
		try:
			self.all_spans2 = self.browser.find_elements_by_xpath("//a[@class='org-company-employees-snackbar__details-highlight snackbar-description-see-all-link link-without-visited-state ember-view']")
	  		
		except NoSuchElementException:
			logging.info("Close browse:")
			logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
			return
		time.sleep(5)

		for self.span in self.all:
			#print "....."
			self.empresas = self.span.get_attribute("href")
			print self.empresas


		
			
		try:
			self.all_spans = self.browser.find_elements_by_xpath("//a[@class='org-company-employees-snackbar__details-highlight snackbar-description-see-all-link link-without-visited-state ember-view']")
	  		
		except NoSuchElementException:
			logging.info("Close browse:")
			logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
			return
		time.sleep(5)

		for self.span in self.all_spans:
			#print "....."
			lista_empresa_func = self.span.get_attribute("href")
			print(type(lista_empresa_func))
			print lista_empresa_func
		'''

		'''# Get URL
		for elem in self.url:
			self.lista_empresa.append(elem.get_attribute("href"))
			
			
		for i in self.lista_empresa:
			company = i.find("company")
			if(company != -1):
				print i
		
			
		'''
		
		
		
			
		
def main():
	obj = dataSearch()
	obj.login()
	obj.search()
	
if __name__ == '__main__':
	main()