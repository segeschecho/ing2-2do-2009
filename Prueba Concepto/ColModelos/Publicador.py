import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import time
import sys
import json
import copy
import os

bd = {}       
puertoGeneral = 8000  # hay que sumarle el id de la EC
host = 'localhost'


def suscribir(unSuscriptor, tipoRes) :
    print "Estoy suscribiendo a", unSuscriptor, "para resultado:", tipoRes
    bd[str(unSuscriptor)] = tipoRes
    archivo = open(nombreArchivo(), "w")
    dato_json = json.dumps(bd)
    archivo.write(dato_json)
    archivo.close()
           
    return 1   

    
def suscriptos():
    
    if not os.path.exists(nombreArchivo()):
        return {}

    archivo = open(nombreArchivo(), "r")
    raid = archivo.read()
    archivo.close()
    publicadores = json.loads(raid)
    if publicadores == "":
        publicadores = {}
    
    bd = copy.deepcopy(publicadores)
    
    return copy.deepcopy(bd)

def nombreArchivo():
    return "BD\\Suscriptos - Publicador " + publicador + " - receptor  " + receptor + " - ID publicador "+ str(idPublicador)  + ".pu"

def inicializarRPC(idEc, publicadorEc, receptorEc):
    puerto = puertoGeneral + int(idEc)
    
    idPublicador = idEc
    publicador = publicadorEc
    receptor = receptorEc
    
    global idPublicador
    global publicador
    global receptor
    
    serverPublicador = SimpleXMLRPCServer((host, puerto), SimpleXMLRPCRequestHandler, False)
    
    print "Levanto el publicador para la EC: ",idEc, ", en el puerto", puerto 
    
    #registro las funciones que necesito
    
    serverPublicador.register_function(suscriptos, "suscriptos")
    serverPublicador.register_function(suscribir, "suscribir")

    serverPublicador.serve_forever()


#Inicializa el publicador de resultados para una ec.         
def inicializarPublicador(idEc, publicador, receptor):
    inicializarRPC(idEc, publicador, receptor) 