
# Author: Marcos Magno de Carvalho (marcoscarvalho@dcc.ufmg.br)

import matplotlib.pyplot as plt

import networkx as nx
import time
import sys
from networkx.algorithms.bipartite.basic import color
from atk import ROLE_MARQUEE
from page_down import DataSearch
from posix import link

class Grafo():
    def __init__(self):
        self.color_write = "write"
        self.color_grey = "grey"
        self.color_black = "black"
        self.G = nx.Graph()
        self.count = 0
        self.pilha = []
        self.lista_empresa = {}  
        
        
        self.obj_pageDown = DataSearch()
        self.obj_pageDown.login()
        self.obj_pageDown._lista_empresa() # pega a lista de empresa e add no dict empresa
 
        


    
    def add_nodes(self, recv_node):
        print recv_node
        
        self.G.add_node(int(recv_node))
        print "add"
        print self.G.nodes()
        
        
            
    def add_edges(self):
        edges = self.read_edge()
        for j in edges:
            string = j
            a = str(string).split(";")    
            i = a[0]
            k = a[1]
            e = i.split("\r")[0]
            p = k.split("\r")[0]
            self.G.add_edge(int(e),int(p))
            
              
    def draw_graph(self):
        self.pos = nx.spring_layout(self.G)
        self.cf = plt.figure(1, figsize=(8,8))
        
        
    
    def run(self):
        self.draw_graph()   
        self.node = 0
        self.lista_empresa = self.obj_pageDown.get_list_empresa()     
        for k,v in self.lista_empresa.iteritems():            
            self.node = k
            
        
        
        self.add_nodes(self.node)                   
        self.G.node[int(self.node)]['color'] = node_color = self.color_write
        #self.G.node[int(node)]['draw'] = nx.draw_networkx_nodes(self.G,pos=nx.spring_layout(self.G), with_labels=True,node_size=3,alpha=1, node_color='b') 
        d = self.G.node[self.node]['color'] # get color 
            
        if d == "write": # Verifica se ja foi visitado                 
            self.busca_em_largura(self.node)
            
            #plt.pause(0.00000001)
        #self.plot()
    
    
    def busca_em_largura(self, node):
        print "busca em largura"
        print self.G.nodes[node]
        print self.G.number_of_nodes()
        #self.G.node[int(node)]['draw'] = nx.draw_networkx_nodes(self.G,pos=nx.spring_layout(self.G), with_labels=True,node_size=3,alpha=1, color = 'b')        
        #self.G.node[int(node)]['draw'].set_color('Grey')                    # Marcar v com a vor cinza
       
        self.G.node[int(node)]['color'] = node_color = self.color_grey
        self.pilha.append(int(node))
        
        
        while self.pilha:
            print "Pilha:",  self.pilha
            self.link_empresa = ''
            
            u = self.pilha.pop(0)
            print "Desempilha", u
            self.G.node[u]['color'] = node_color = self.color_black
            print "COLOR NODE U", self.G.node[u]['color']
            _link_empresa = [(k,v) for k,v in self.lista_empresa.iteritems() if k == u]
             
            for link in _link_empresa:                
                self.link_empresa = link[1]
                print "Link empresa", self.link_empresa 
            
            print "VISITA LISTA DE EMPRESA"
            self.obj_pageDown.visita_lista_empresa(self.link_empresa)
            
            print " LISTA DE ADD USUARIOS"
            for perfil_usuario in self.obj_pageDown.get_lista_funcionario().values():
                print "USUARIOS:", perfil_usuario
                self.obj_pageDown.visita_lista_funcionario(perfil_usuario)
                time.sleep(2)        
                
                # Lista de empresa
            w = self.obj_pageDown.return_novas_empresas()
            print "novs empresas: adj", w  
            time.sleep(2)  
            for n,v in w.iteritems():
                print n, v
                print "verifica se value[node] ja esta na lista empresa", n
                if str(n) not in self.link_empresa:
                    print "n nao esta na lista"
                    self.lista_empresa[int(n)] = v
                    self.add_nodes(int(n))
                    self.G.node[int(n)]['color'] = node_color = self.color_write
                    print "lista empresa", self.lista_empresa                 
                    get_color_w = self.G.node[n]['color']
                    print "color node nd", get_color_w 
                    if get_color_w == "write":
                        self.G.node[n]['color'] = node_color = self.color_grey
                        
                        print "W: ", n
                        self.pilha.append(n) 
                        #self.visitar(node, u)                
                            
            time.sleep(5)
                #self.dic_componente[v_inicial] = self.count_componente
        return        
           
        
    def visitar(self,v,w,v_inicial):    
        # Funcao visitar
        
  
        
        plt.pause(0.00000001)    
        nx.draw_networkx_edges(self.G,self.pos,edgelist=[(v,w)])
        plt.draw()
        
        '''
        if v_inicial not in self.vertice_inicial:
            self.vertice_inicial.append(v_inicial)
            v_inicial = 0          
        else:
            v_inicial = v_inicial + 1        
            print "dictonario: ", self.vertice_inicial
            time.sleep(2)
            print "vertices count", v_inicial
        
'''

    def plot(self):
        plt.draw()
            


 