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
from random import randint
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import hashlib
import sys
from log import *
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
 
class DataSearch():

     
    def __init__(self):

        self.strftime = '----------%H:%M:%S----------\n'           
        self.lista_empresa = {}
        self.lista_usuario = {}
        self.lista_novas_empresas  = {}
        

        
    def start_browser(self):
       
        self.fp = webdriver.FirefoxProfile()
        self.browser = webdriver.Firefox(firefox_profile=self.fp)
        self.browser.set_window_size(1068, 1050)
        self.browser.get("https://www.linkedin.com/uas/login?session_redirect=%2Fschool%2F636119%2Falumni%2F&fromSignIn=true&trk=uno-reg-join-sign-in") 
      
        ''' 
           Dicionario empresa 
        '''
    def close_browser(self):
        self.browser.close()      
    def login(self):

        try:
            self.username = self.browser.find_element_by_id("session_key-login") # field of login
            self.password = self.browser.find_element_by_id("session_password-login") # filed of password
            self.username.send_keys("datalabunibh@gmail.com") # Inserir seu usuário
            self.password.send_keys("unibh2017ic") # Inserir sua senha
            self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
            self.login_attempt.submit() #apply button submit
            logging.info("[  Page Down ] Try Login with: Marcos" +  str(datetime.datetime.now().strftime(self.strftime)))
        except NoSuchElementException:
            logging.info("Close browse:")
            logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
            return
  
    
    def _lista_empresa(self):
        logging.info("[  Page Down ] Visit List of Company" +  str(datetime.datetime.now().strftime(self.strftime)))
        self.linkEmpresa = "https://www.linkedin.com/search/results/companies/"
        self.browser.get(self.linkEmpresa)
        self.browser.execute_script("window.scrollTo(0, 1024)")
 
        try:
            self.all_spans = self.browser.find_elements_by_xpath("//a[@class='search-result__result-link ember-view']")
        except NoSuchElementException:
            logging.info("Close browse:")
            logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
            return
        time.sleep(5)
                
        # Pegar link e nome das empresas

        for self.empresa in self.all_spans:
            self.add_dic_empresa(self.empresa.text, self.empresa.get_attribute("href"))       


         
    def get_current_login(self):
        return self.browser.current_url        
            
    def add_dic_empresa(self, key, value):      
        new_key = self.converte_chave(key) 
        logging.info("[ Page Down ] Add Company: " + str(key) + str(datetime.datetime.now().strftime(self.strftime)))
        self.lista_empresa[new_key] = value

    def login_again(self):
        logging.info("[ Distributed Serve ] Change Login to : Jonas " + str(datetime.datetime.now().strftime(self.strftime)))
        self.browser.get("https://www.linkedin.com/uas/login?session_redirect=%2Fschool%2F636119%2Falumni%2F&fromSignIn=true&trk=uno-reg-join-sign-in")
        self.username = self.browser.find_element_by_id("session_key-login") # field of login
        self.password = self.browser.find_element_by_id("session_password-login") # filed of password
        self.username.send_keys("jonasfissicaro@hotmail.com") # 
        self.password.send_keys("Ib!turun@1320") # Inserir sua senha
        self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
        self.login_attempt.submit() #apply button submit

        time.sleep(3)
        
                                

        
    def get_list_empresa(self):
        return self.lista_empresa      

    def add_dic_usuario(self, key, value):
        new_key = self.converte_chave(key)
        
        self.lista_usuario[int(new_key)] = value
        
    
    def add_novas_empress(self,key, value):
        new_key = self.converte_chave(key)
                
        self.lista_novas_empresas[int(new_key)] = value
    
        
    def return_novas_empresas(self):
        print "tamanho de novas empresas:", len(self.lista_novas_empresas)
        return self.lista_novas_empresas
    
    
    def visita_lista_empresa(self, link_empresa):
        '''
            2 - Para cada empresa pega a lista de funcionarios
        '''
        link = self.link_funcionarios(link_empresa) # pega link da lista dos funcionarios de cada empresa
        print link
        self.get_funcionario(link)          
            
            
            
    def converte_chave(self,key):
        s = key
        y = int(hashlib.sha256(s).hexdigest(), 16) % (10 ** 6)
        return int(y)
        
          

    def link_funcionarios(self,link_Empresa):
        

        self.linkEmpresa = link_Empresa       
        self.browser.get(self.linkEmpresa)
        
        self.browser.execute_script("window.scrollTo(0, 1024)") 
        
        try:
            self.all_spans = self.browser.find_elements_by_xpath("//a[@class='org-company-employees-snackbar__details-highlight snackbar-description-see-all-link link-without-visited-state ember-view']")       
            self.url = self.browser.find_elements_by_xpath("//a[@href]")
        except NoSuchElementException:
            logging.info("Close browse:")
            logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
            return
        time.sleep(5)     
         
        
        # Get Link to user profile
        for self.span in self.all_spans:            
            return self.span.get_attribute("href")
            
       

    def get_funcionario(self, link_funcionarios):
        self.linkFuncionarios = link_funcionarios
        self.u = []
        self.l = []
        self.browser.get(self.linkFuncionarios)
        self.browser.execute_script("window.scrollTo(0, 1024)")
 
        try:
            self.all_spans_fun = self.browser.find_elements_by_xpath("//a[@class='search-result__result-link ember-view']")
            
            self.nome_func = self.browser.find_elements_by_xpath("//span[@class='name actor-name']")

        except NoSuchElementException:
            logging.info("Close browse:")
            logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
            return
        time.sleep(5)
                
        # Get DIV
        cont = 0
        emp = 0
        for self.nome_usuario in self.all_spans_fun:            
            #self.u.append(self.nome_usuario.text.split("\n")[0]) 
            
            '''if cont % 2 != 0:
                #print self.nome_usuario.get_attribute("href")
                self.l.append(self.nome_usuario.get_attribute("href"))
            cont = cont + 1
            '''
            print "ADCIONAR LISTA DE USAURIOS"
            self.add_dic_usuario(self.nome_usuario.text.split("\n")[0], self.nome_usuario.get_attribute("href")) # metodo para converter chave

    def get_lista_funcionario(self):
        print "Tamanho da lista de Usuario", len(self.lista_usuario)        
        return self.lista_usuario       
        
    def visita_lista_funcionario(self, lista_usuario):
        print "VISITA LISTA FUNCIONARIOS [ PEGAR NOVAS EMPRESAS ]"
      
        self.pegar_novas_empresas(lista_usuario)
         
            
            
    
    def pegar_novas_empresas(self, perfil_usuario):
        print "pegar novas empresas"
        self.linkUsuario = perfil_usuario
        self.browser.get(self.linkUsuario)
        self.browser.execute_script("window.scrollTo(0, 1024)")
        
        n = randint(0,9)
        self.lista_novas_empresas[n] = 'https://www.linkedin.com/company/5390798/'
            
        print "NOVAS EMPRESAS", self.lista_novas_empresas
        
        
        '''try:
            self.all_spans = self.browser.find_elements_by_xpath("//div[@class='pv-entity__summary-info']")
        except NoSuchElementException:
            logging.info("Close browse:")
            logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
            return
                     
        for self.span in self.all_spans:
            print self.span.text  
        '''