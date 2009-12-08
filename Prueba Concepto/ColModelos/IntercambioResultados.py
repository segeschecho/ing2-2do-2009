import time
import random
import threading
import sys
import copy
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import json
            
# publica los resultados a los que se suscribieron
def publicar(resultado):
    
    suscriptos = serverPublicador.suscriptos()
    for unaEc in suscriptos.keys():
        if resultado[0] in suscriptos[unaEc]:
            print "Estoy publicando el resultado numero: " + str(resultado[2]) +" de tipo: " + resultado[0] + " a la EC: " + unaEc
            unaEcI = int(unaEc)
            host = 'localhost'
            port = 6000 + unaEcI
            serverOtraEc = xmlrpclib.ServerProxy("http://%s:%s/"%(host, port))
            serverOtraEc.recibir(resultado, idEc)
    return 0    

# recibe resultados de otros modelos    
def recibir(resultado, otraEc):
    archivo = open("Resultados\\Id EC - " + str(idEc) + " Resultado De " + str(otraEc) + " Num - " + str(resultado[2]) + " Tipo - " + resultado[0] + ".ec", "w")
    dato_json = json.dumps(resultado[1])
    archivo.write(dato_json)
    archivo.close()
    return 0

# se suscribe a los resultados de otros modelos
def suscribirme():
    print "Me voy a suscribir a las ECs", publicadoresEcs.keys()
    for idS in publicadoresEcs.keys():
        idI = int(idS)
        host = 'localhost'
        port = 8000 + idI
        serverPublicadorOtraEc = xmlrpclib.ServerProxy("http://%s:%s/"%(host, port))
        serverPublicadorOtraEc.suscribir(idEc,publicadoresEcs[idS])
        
    
# inicializo el servidor
def inicializar(idEcNvo, publicadoresEcsNvo):
    # SERVER        
    
    global idEc
    global publicadoresEcs
    global serverPublicador
    
    idEc = int(idEcNvo)
    publicadoresEcs = publicadoresEcsNvo
    
    host = "localhost"
    puertoEc = 6000 + idEc
    puertoPublicador = 8000 + idEc
    
    print "Soy la EC con id =", idEc
    
    serverPublicador = xmlrpclib.ServerProxy("http://%s:%s/"%(host,puertoPublicador))
    
    server = SimpleXMLRPCServer((host, puertoEc), SimpleXMLRPCRequestHandler, False)
    
    print "Escuchando en el puerto... ", puertoEc
    
    server.register_function(publicar, "publicar")
    server.register_function(recibir, "recibir")
    
    suscribirme()
    
    server.serve_forever()    



