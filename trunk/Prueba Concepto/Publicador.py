import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import time
import sys
import json
import copy
bd = {}       
puerto_general = 9000  # hay que sumarle el id de la tr
host = 'localhost'
def suscribir(un_suscriptor, conjunto_sensores) :
    print "Estoy suscribiendo a", un_suscriptor, "para estos sensores:",conjunto_sensores
    bd[str(un_suscriptor)] = conjunto_sensores
    archivo = open("BDESTADO\\Suscriptos - TR" +str(id_TR)  + ".tr", "w")
    dato_json = json.dumps(bd)
    archivo.write(dato_json)
    archivo.close()
           
    return 1   
def suscriptos():
    archivo = open("BDESTADO\\Suscriptos - TR" +str(id_TR)  + ".tr", "r")
    raid = archivo.read()
    publicadores = json.loads(raid)  
    for id in publicadores.keys():
        sensores_unicode = publicadores[id]
        sensores_str = []
        for sensor_unicode in sensores_unicode:
            sensores_str.append(str(sensor_unicode))
        del publicadores[id]
        publicadores[str(id)] = sensores_str
    
    bd = copy.deepcopy(publicadores)
    print "Existen", len(bd), "suscriptos"
    return copy.deepcopy(bd)

def inicializarRPC(id_tr):
    puerto = puerto_general + id_tr
    id_TR = id_tr
    global id_TR
    serverPublicador = SimpleXMLRPCServer((host, puerto), SimpleXMLRPCRequestHandler, False)
    print "Levanto el publicador...",puerto
    
    #registro las funciones que necesito
    
    serverPublicador.register_function(suscriptos, "suscriptos")
    serverPublicador.register_function(suscribir, "suscribir")

    serverPublicador.serve_forever()


        
def inicializarPublicador(id_tr):
    inicializarRPC(id_tr) 