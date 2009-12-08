import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import time
import sys
import json
import copy
import os
bd = {}       
puerto_general = 9000  # hay que sumarle el id de la tr
host = 'localhost'
def suscribir(un_suscriptor, conjunto_sensores) :
    print "Estoy suscribiendo a EC", un_suscriptor, "para estos sensores:",conjunto_sensores
    bd[str(un_suscriptor)] = conjunto_sensores
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
        
    # for id in publicadores.keys():
        # sensores_unicode = publicadores[id]
        # sensores_str = []
        # for sensor_unicode in sensores_unicode:
            # sensores_str.append(str(sensor_unicode))
        # del publicadores[id]
        # publicadores[str(id)] = sensores_str
    
    bd = copy.deepcopy(publicadores)
    print "Existen", len(bd), "suscriptos"
    return copy.deepcopy(bd)

def nombreArchivo():
    return "BDESTADO\\Suscriptos - Publicador " + publicador + " - receptor  " +receptor+ " - ID publicador "+ str(id_publicador)  + ".pu"

def inicializarRPC(id, publicador_par, receptor_par):
    puerto = puerto_general + int(id)
    id_publicador = id
    publicador = publicador_par
    receptor = receptor_par
    global id_publicador
    global publicador
    global receptor
    serverPublicador = SimpleXMLRPCServer((host, puerto), SimpleXMLRPCRequestHandler, False)
    print "Levanto el publicador...",puerto
    
    #registro las funciones que necesito
    
    serverPublicador.register_function(suscriptos, "suscriptos")
    serverPublicador.register_function(suscribir, "suscribir")

    serverPublicador.serve_forever()


        
def inicializarPublicador(id_tr, publicador, receptor):
    inicializarRPC(id_tr, publicador, receptor) 