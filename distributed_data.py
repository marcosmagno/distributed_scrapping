import mysql.connector
import threading
import time
import struct
import commands
import sys
from random import *
import zipfile
import os
import socket
import datetime
import logging
from page_down_distributed import DataSearch
from random import randint
from selenium import webdriver
from threading import Thread
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import hashlib
import json
reload(sys)
sys.setdefaultencoding('utf-8')


class Data_recv_company(Thread):


    def __init__(self,data):
        ''' Constructor. ''' 
        Thread.__init__(self)
        self.strftime = '----------%H:%M:%S----------\n'  
        self.lista_empresa = {}
        self.lista_novas_empresas = {}        
        self.data_recv = data
        self.lista_usuario = {}
        self.lista_usuario_send = {}
        self.fp = webdriver.FirefoxProfile()
        self.browser = webdriver.Firefox(firefox_profile=self.fp)
        self.browser.set_window_size(1068, 1050)   
        self.browser.set_window_size(1068, 1050)      

    def run(self):
        print "eun"
        l = json.loads(self.data_recv)
        
        if not l:
            logging.info("[ Distributed Data ] List is empty " +  str(datetime.datetime.now().strftime(self.strftime)))
        else:
            
            for k,v in l.iteritems():
                if k not in self.lista_empresa:
                    logging.info("[ Distributed Data ] Add List of Company in Hash " + str(k) + str(datetime.datetime.now().strftime(self.strftime)))
                    self.lista_empresa[k] = v
                    logging.info("[ Distributed Data ] Visiting " + str(k) + str(datetime.datetime.now().strftime(self.strftime)))                  
                    self.visita_lista_empresa(v)
                    
                    self.create_socket(self.lista_usuario_send, 2, '192.168.43.125') # 11
                else:                    
                    logging.info("[ Distributed Data ] Company already visited. " + str(k) + str(datetime.datetime.now().strftime(self.strftime)))
            
            # When terminate loop, send to other computer.
            logging.info("[ Distributed Data ] Witdh of list user to send. " + str(len(self.lista_usuario_send)) + str(datetime.datetime.now().strftime(self.strftime)))
  
        
                
    

    def visita_lista_empresa(self, link_empresa):        
        link = self.link_funcionarios(link_empresa) # pega link da lista dos funcionarios de cada empresa
        
        if link == None:
            logging.info("[ Distributed Data ] Invalid Link " + str(datetime.datetime.now().strftime(self.strftime)))
            logging.info("[ Distributed Data ] Login again " + str(datetime.datetime.now().strftime(self.strftime))) 
            self.login_again()
            link = self.link_funcionarios(link_empresa) # pega link da lista dos funcionarios de cada empresa 
        else:
            self.set_funcionario(link)          

    def link_funcionarios(self,link_Empresa):

        self.linkEmpresa = link_Empresa
        
        if self.linkEmpresa == None:            
            return
        
        else:       
            self.browser.get(self.linkEmpresa)
            
            self.browser.execute_script("window.scrollTo(0, 1024)") 
            
            try:
                self.all_spans = self.browser.find_elements_by_xpath("//a[@class='org-company-employees-snackbar__details-highlight snackbar-description-see-all-link link-without-visited-state ember-view']")       
                self.url = self.browser.find_elements_by_xpath("//a[@href]")
            except NoSuchElementException:
                logging.info("Close browse:")
                logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
                return
        # Get Link to user profile
        for self.span in self.all_spans:            
            return self.span.get_attribute("href")
            
    def set_funcionario(self, link_funcionarios):        
        self.linkFuncionarios = link_funcionarios
        if self.linkFuncionarios == None:
            return
        else:
            self.browser.get(self.linkFuncionarios)
            self.browser.execute_script("window.scrollTo(0, 1024)")
     
            try:
                self.all_spans_fun = self.browser.find_elements_by_xpath("//a[@class='search-result__result-link ember-view']")
            except NoSuchElementException:
                logging.info("Close browse:")
                logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
                return
    
            for self.nome_usuario in self.all_spans_fun:            
                self.add_dic_usuario(self.nome_usuario.text.split("\n")[0], self.nome_usuario.get_attribute("href")) # metodo para converter chave
        
    def add_dic_usuario(self, key, value):
        
        if key == None or value == None:
            return
        else:
            new_key = self.converte_chave(key)
            logging.info("[ Distributed Data ] Add User :" + str(key)  + " - Node : " + str(new_key) + " - "+ str(datetime.datetime.now().strftime(self.strftime)))
            if int(new_key) not in self.lista_usuario.keys():
                # if new_key not in list of user, add.
                self.lista_usuario[int(new_key)] = value
                # add too in list user to send.
                self.lista_usuario_send[int(new_key)] = value
            else:
                logging.info("[ Distributed Data ] User already visited")
            
        print "creat socket to :"
        
            
    
        
    def converte_chave(self,key):
        s = key
        y = int(hashlib.sha256(s).hexdigest(), 16) % (10 ** 4)
        
        return int(y)       
    
    def login_again(self):
        self.browser.get("https://www.linkedin.com/uas/login?session_redirect=%2Fschool%2F636119%2Falumni%2F&fromSignIn=true&trk=uno-reg-join-sign-in")
        self.username = self.browser.find_element_by_id("session_key-login") # field of login
        self.password = self.browser.find_element_by_id("session_password-login") # filed of password
        self.username.send_keys("datalabunibh@gmail.com") # 
        self.password.send_keys("unibh2017ic") # Inserir sua senha
        self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
        self.login_attempt.submit() #apply button submit

        time.sleep(3)
            
    
    def create_socket(self, lista_empresa, msg_type, ip_recv):        
        server_address = (''+str(ip_recv)+'', 10000)
        logging.info("[ Distributed Data ] Witdh of list user send. " + str(len(lista_empresa)) + str(datetime.datetime.now().strftime(self.strftime)))
        try:
            # Create a TCP/IP socket
            socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print >>sys.stderr, 'connecting to %s port %s' % server_address
            socks.connect(server_address)
            data= struct.pack("!H",msg_type)
            data+= struct.pack("!I",len(lista_empresa)) #assumes len(body) fits into a integer
            data+= json.dumps(lista_empresa) #assumes body is a string            
            socks.send(data)
            socks.close()
            
            # trocar para uma lista generica 
            self.lista_usuario_send.clear()
            
        except socket.error, exc:
            logging.info("[ Distributed Data ] Caught exception socket.error : %s" % exc)
            return            
                  
class Data_recv_user(Thread):    

    def __init__(self,data):
        ''' Constructor. ''' 
        Thread.__init__(self)
        self.strftime = '----------%H:%M:%S----------\n'      
        self.data_recv = data   
        #self.connection_socket = ''
        #self.lista_empresa = {}
        self.lista_novas_empresas = {}
        self.lista_usuario = {}
        self.lista_usuario_send = {}
        self.fp = webdriver.FirefoxProfile()
        self.browser = webdriver.Firefox(firefox_profile=self.fp)
        self.browser.set_window_size(1068, 1050) 
        self.browser.get("https://www.linkedin.com/uas/login?session_redirect=%2Fschool%2F636119%2Falumni%2F&fromSignIn=true&trk=uno-reg-join-sign-in")          
 
    # msg type 2recv_list_usuarios
    def run(self):
        self.login()
        if (str(self.get_current_login()) != "https://www.linkedin.com/school/636119/alumni/"):    
            self.login_again()         
        #time.sleep(5)
        user = json.loads(self.data_recv)

        if not user:
            logging.info("Dict User is empyt")

        else:
                
            for k,v in user.iteritems():
                if k not in self.lista_usuario:
                    self.lista_usuario[k] = v
                    logging.info("[ Distributed Data ] Visiting :" + str(k)  + str(datetime.datetime.now().strftime(self.strftime)))                  
                    self.pegar_novas_empresas(v)
                    
                else:
                    logging.info("[ Distributed Data ] User aleardy visited :" + str(k)  + str(datetime.datetime.now().strftime(self.strftime)))
 
 
    def login(self):
        # Login 
        self.username = self.browser.find_element_by_id("session_key-login") # field of login
        self.password = self.browser.find_element_by_id("session_password-login") # filed of password
        self.username.send_keys("jonasfissicaro@hotmail.com") # 
        self.password.send_keys("Ib!turun@1320") # Inserir sua senha
        self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
        self.login_attempt.submit() #apply button submit

        time.sleep(3) 
    def pegar_novas_empresas(self, perfil_usuario):

        self.linkUsuario = perfil_usuario

        self.browser.get(self.linkUsuario)
        self.browser.execute_script("window.scrollTo(0, 1024)")
        self.browser.execute_script("window.scrollTo(1024, 2048)")
        
        try:
            self.all_spans = self.browser.find_elements_by_xpath("//a[@class='ember-view']")
    
        except NoSuchElementException:
            logging.info("Close browse:")
            logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
            return
        time.sleep(5)

        # Get DIV
        for self.span in self.all_spans:
            print self.span.text
            try:
                d = self.span.text.split("\n")[2]
                print d   
                link = self.span.get_attribute("href")
                #self.add_novas_empress(d,link)

                self.add_novas_empresa(d, link)
                
            except IndexError:
                d = 'https://www.linkedin.com/company/203563/'
                print "erro"
                return
            
                                
        
    def add_novas_empresa(self,key, value):
        logging.info("[ Distributed Data ] Add new company :" + str(key)  + str(datetime.datetime.now().strftime(self.strftime)))     

        new_key = self.converte_chave(key)                
        self.lista_novas_empresas[int(new_key)] = value
        print "lista nova empresas"
        

        
        self.create_socket(self.lista_novas_empresas, 1, '192.168.43.175')    
        self.browser.close()        
            
             
        
    def login_again(self):
        self.browser.get("https://www.linkedin.com/uas/login?session_redirect=%2Fschool%2F636119%2Falumni%2F&fromSignIn=true&trk=uno-reg-join-sign-in")
        self.username = self.browser.find_element_by_id("session_key-login") # field of login
        self.password = self.browser.find_element_by_id("session_password-login") # filed of password
        self.username.send_keys("datalabunibh@gmail.com") # 
        self.password.send_keys("unibh2017ic") # Inserir sua senha
        self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
        self.login_attempt.submit() #apply button submit

        time.sleep(3)
        
                
    def get_current_login(self):
        return self.browser.current_url
 
        
    def create_socket(self, lista_empresa, msg_type, ip_recv):        
        server_address = (''+str(ip_recv)+'', 10000)
        logging.info("[ Distributed Data ] Witdh of list user send. " + str(len(lista_empresa)) + str(datetime.datetime.now().strftime(self.strftime)))
        try:
            # Create a TCP/IP socket
            socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print >>sys.stderr, 'connecting to %s port %s' % server_address
            socks.connect(server_address)
            data= struct.pack("!H",msg_type)
            data+= struct.pack("!I",len(lista_empresa)) #assumes len(body) fits into a integer
            data+= json.dumps(lista_empresa) #assumes body is a string            
            socks.send(data)
            socks.close()
            
            # trocar para uma lista generica 
            self.lista_usuario_send.clear()
            
        except socket.error, exc:
            logging.info("[ Distributed Data ] Caught exception socket.error : %s" % exc)
            return            
                  
    def converte_chave(self,key):
        s = key
        y = int(hashlib.sha256(s).hexdigest(), 16) % (10 ** 4)
        
        return int(y)                  
             
class Data_recv(object):    
    def __init__(self):    
        self.strftime = '----------%H:%M:%S----------\n'   
        #self.connection_socket = ''
        #self.lista_empresa = {}
        self.lista_novas_empresas = {}
        self.lista_usuario = {}
        self.lista_usuario_send = {}
        
 
    # msg type 2recv_list_usuarios
    def recv_list_usuarios(self, lista_usuarios_recv):
        
        user = json.loads(lista_usuarios_recv)

        if not user:
            logging.info("Dict User is empyt")

        else:
                
            for k,v in user.iteritems():
                if k not in self.lista_usuario:
                    self.lista_usuario[k] = v
                    logging.info("[ Distributed Data ] Visiting :" + str(k)  + str(datetime.datetime.now().strftime(self.strftime)))                  
                    self.pegar_novas_empresas(v)
                    
                else:
                    logging.info("[ Distributed Data ] User aleardy visited :" + str(k)  + str(datetime.datetime.now().strftime(self.strftime)))
 
    
    def pegar_novas_empresas(self, perfil_usuario):

        self.linkUsuario = perfil_usuario

        self.browser.get(self.linkUsuario)
        self.browser.execute_script("window.scrollTo(0, 1024)")
        self.browser.execute_script("window.scrollTo(1024, 2048)")
        
        try:
            self.all_spans = self.browser.find_elements_by_xpath("//a[@class='ember-view']")
    
        except NoSuchElementException:
            logging.info("Close browse:")
            logging.info("Finished" +  str(time.strftime("%d/%m/%Y %H:%M:%S")))
            return
        time.sleep(5)

        # Get DIV
        for self.span in self.all_spans:
            print self.span.text
            try:
                d = self.span.text.split("\n")[2]
                print d   
                link = self.span.get_attribute("href")
                #self.add_novas_empress(d,link)

                self.add_novas_empresa(d, link)
                
            except IndexError:
                d = 'https://www.linkedin.com/company/203563/'
                print "erro"
                return
            
            
        
    def add_novas_empresa(self,key, value):
        logging.info("[ Distributed Data ] Add new company :" + str(key)  + str(datetime.datetime.now().strftime(self.strftime)))     

        new_key = self.converte_chave(key)                
        self.lista_novas_empresas[int(new_key)] = value
        print "lista nova empresas"
        

        
        self.create_socket(self.lista_novas_empresas, 1, '192.168.0.60')    
                    
                      
        
    def start_browser(self):
        logging.info("[ Distributed Server ] Start Browser : " + str(datetime.datetime.now().strftime(self.strftime)))
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
        # Login 
        self.username = self.browser.find_element_by_id("session_key-login") # field of login
        self.password = self.browser.find_element_by_id("session_password-login") # filed of password
        self.username.send_keys("jonasfissicaro@hotmail.com") # 
        self.password.send_keys("Ib!turun@1320") # Inserir sua senha
        self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
        self.login_attempt.submit() #apply button submit

        time.sleep(3)
        
    def login_again(self):
        self.browser.get("https://www.linkedin.com/uas/login?session_redirect=%2Fschool%2F636119%2Falumni%2F&fromSignIn=true&trk=uno-reg-join-sign-in")
        self.username = self.browser.find_element_by_id("session_key-login") # field of login
        self.password = self.browser.find_element_by_id("session_password-login") # filed of password
        self.username.send_keys("datalabunibh@gmail.com") # 
        self.password.send_keys("unibh2017ic") # Inserir sua senha
        self.login_attempt = self.browser.find_element_by_xpath("//*[@type='submit']") #find a element of type submit
        self.login_attempt.submit() #apply button submit

        time.sleep(3)
        
                
    def get_current_login(self):
        return self.browser.current_url
 
        
    def create_socket(self, lista_empresa, msg_type, ip_recv):        
        server_address = (''+str(ip_recv)+'', 10000)
        logging.info("[ Distributed Data ] Witdh of list user send. " + str(len(lista_empresa)) + str(datetime.datetime.now().strftime(self.strftime)))
        try:
            # Create a TCP/IP socket
            socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print >>sys.stderr, 'connecting to %s port %s' % server_address
            socks.connect(server_address)
            data= struct.pack("!H",msg_type)
            data+= struct.pack("!I",len(lista_empresa)) #assumes len(body) fits into a integer
            data+= json.dumps(lista_empresa) #assumes body is a string            
            socks.send(data)
            socks.close()
            
            # trocar para uma lista generica 
            self.lista_usuario_send.clear()
            
        except socket.error, exc:
            logging.info("[ Distributed Data ] Caught exception socket.error : %s" % exc)
            return            
                  
    
    def recv_new_empresa(self, data):
        print data
    
    def decode_msg(self, recv_data):
        """ Deconde mensegge
            Unpack packet of mensege
            msg_type of width 3
            and data recv > of 6
        """      
        msg_type = struct.unpack('!Hs',recv_data[:3])[0]
        data_recv = recv_data[6:]
        logging.info("[ Distributed Data ] Rev Data - Type Message: " + str(msg_type) + str(datetime.datetime.now().strftime(self.strftime)))

        if (msg_type == 1):
            #self.add_lista_empresa(data_recv)
            myObj = Data_recv_company(data_recv)
            myObj.start()
            
        elif (msg_type == 2):

            #self.recv_list_usuarios(data_recv)
            myThread = Data_recv_user(data_recv)
            myThread.start()
            
        elif(msg_type == 3):
            self.recv_new_empresa(data_recv)
            
        else:
            print "Tipo de mensagem Invalido."


