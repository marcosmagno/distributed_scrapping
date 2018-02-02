"""Distributed Server Module."""
import select
import socket
import sys
import Queue
import logging
import time
from threading import Thread
from distributed_data import Data_recv
from page_down_distributed import DataSearch
import struct
import json
from log import *
import datetime
class RecvMinipc(object):
    """docstring for RecvMinipc"""
    
    def __init__(self):        
     
        initialize_logger('') 
        self.strftime = ' ----------%H:%M:%S----------\n'          
        try:
           
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            self.server_address = ('', 10000)
            logging.info("[ Distributed Server ] Bind Socket:" + str(self.server_address) + str(datetime.datetime.now().strftime(self.strftime)))
            self.server.bind(self.server_address)
            self.server.listen(5)
            
        except socket.error, exc:
            #self.socket_logger.info("Caught exception socket.error : %s" % exc)
            print "Caught exception socket.error : %s" % exc

        # Sockets from which we expect to read
        self.inputs = [ self.server ]

        # Sockets to which we expect to write
        self.outputs = [ ]

        # Outgoing message queues (socket:Queue)
        self.message_queues = {}
        self.connections_serv_telosb = {}



    
    def control(self):
        self.new_data = Data_recv()
        self.new_data.start_browser()
        self.new_data.login()
        logging.info("[ Distributed Serve ] Login: " + str(datetime.datetime.now().strftime(self.strftime)))
        time.sleep(5)
        if (str(self.new_data.get_current_login()) != "https://www.linkedin.com/school/636119/alumni/"):    
            self.new_data.login_again()        
        
        while self.inputs:
            # Wait for at least one of the sockets to be ready for processing
            logging.info("[ Distributed Server ] Waint for the new event.")
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

            # Handle inputs
            for s in readable:
                if s is self.server:
                    # A "readable" server socket is ready to accept a connection
                    
                    connection, client_address = s.accept()
                    logging.info("[ Distributed Server ] new connection from." + str(client_address))
                    #connection.setblocking(0)
                    self.inputs.append(connection)
                    
                    # Give the connection a queue for data we want to send
                    self.message_queues[connection] = Queue.Queue()
                    self.connections_serv_telosb.update({connection:client_address[0]})

                else:                    
                    try:
                        data = s.recv(1024)                        
                    except socket.error, ex:                        
                        logging.info("[ Distributed Server ] Data Recv Error:" + str(ex) + str(datetime.datetime.now().strftime(self.strftime)))
              
                    if data:  
                        # Check  message tyoe | self.decode_msg(data)
                        self.new_data.decode_msg(data)
                        # A readable client socket has data
                        self.message_queues[s].put(data)
                        
                        # Add output channel for response
                        if s not in self.outputs:
                            self.outputs.append(s)
                    else:
                        # Interpret empty result as closed connection
                        logging.info("[ Distributed Server ] closing after reading no data:" + str(client_address) + str(datetime.datetime.now().strftime(self.strftime)))
                        
                        if s in self.outputs:
                            self.outputs.remove(s)
                            self.connections_serv_telosb.pop(s)
                        self.inputs.remove(s)
                        s.close()
                        # Remove message queue
                        del self.message_queues[s]
                        # Handle outputs

            # Handle "exceptional conditions"
            for s in exceptional:
                logging.info("[ Distributed Server ] closing after reading no data:" + str(s.getpeername()) + str(datetime.datetime.now().strftime(self.strftime)))
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()

                # Remove message queue
                del self.message_queues[s]
    
class RunGrafo(Thread):

    def __init__(self):
        ''' Constructor. ''' 
        Thread.__init__(self)
 
    def run(self):
        # Crate Object of Class DataSearch
        # Start Browser
        # Login in Browser
        # list of company
        self.strftime = ' ----------%H:%M:%S----------\n'
        self.obj_page_down = DataSearch() 
        self.obj_page_down.start_browser() 
        self.obj_page_down.login() 
        self.obj_page_down._lista_empresa() 
        
        
        # Verivy is current login is diferent the companies.
        # If True, do login again and call method list_empresa
        if (str(self.obj_page_down.get_current_login()) != "https://www.linkedin.com/search/results/companies/"):
            self.obj_page_down.login_again()
            self.obj_page_down._lista_empresa()        
       
        self.create_socket(self.obj_page_down.get_list_empresa())
    
    def create_socket(self, lista_empresa):
        server_address = ('192.168.43.125', 10000)
        logging.info("[ Distributed Server ] Send Data to : " + str(server_address) + str(datetime.datetime.now().strftime(self.strftime)))
        logging.info("[ Distributed Server ] Width Data : " + str(len(lista_empresa)) + str(datetime.datetime.now().strftime(self.strftime)))
        try:
            socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.info("[ Distributed Server ] Connectiong to " + str(server_address))
            socks.connect(server_address)
            data= struct.pack("!H",1)
            data+= struct.pack("!I",len(lista_empresa)) #assumes len(body) fits into a integer
            data+= json.dumps(lista_empresa) #data serialized          
            
            socks.send(data)
            socks.close()
        except socket.error, exc:
            logging.info("Caught exception socket.error : %s" % exc)
            return
        
            

def main():   
  
    if len(sys.argv) < 2:
        pass    
    else: 
        
        if sys.argv[1] == 'run':
            myThreadOb = RunGrafo()
            myThreadOb.start()            
    c = RecvMinipc()
    c.control()
     

if __name__ == '__main__':
    main()
