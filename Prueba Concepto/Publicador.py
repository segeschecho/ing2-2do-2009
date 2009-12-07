import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import time
import sys

bd = {}       
puerto_general = 9000  # hay que sumarle el id de la tr
host = 'localhost'

def suscribir(un_suscriptor, conjunto_sensores) :
    print "Estoy suscribiendo a", un_suscriptor, "para estos sensores:",conjunto_sensores
    bd[str(un_suscriptor)] = conjunto_sensores
    return 1   
def suscriptos():
    print "Existen", len(bd), "suscriptos"
    return bd.copy()

def inicializarRPC(id_tr):
    puerto = puerto_general + id_tr
    serverPublicador = SimpleXMLRPCServer((host, puerto), SimpleXMLRPCRequestHandler, False)
    print "Levanto el publicador...",puerto
    
    #registro las funciones que necesito

    serverPublicador.register_function(suscriptos, "suscriptos")
    serverPublicador.register_function(suscribir, "suscribir")

    serverPublicador.serve_forever()


        
def inicializarPublicador(id_tr):
    inicializarRPC(id_tr) 