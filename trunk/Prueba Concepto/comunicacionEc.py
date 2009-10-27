import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import time
import sys


#creo el servidor para el enviador
hostCanal = "localhost"
puertoCanal = 5555
serverCanal = xmlrpclib.ServerProxy("http://%s:%s/"%(hostCanal,puertoCanal))

#estructura que guarda los datos en vuelo es un doble diccionario con ID_MSG y ID_PARTE
datosEnVuelo = {}

def pruebaEnviadorTR(mensaje):
    while 1:
        pass

def verificarDatos():
    """
    funcion que se encarga de ver si hay que reenviar mensajes de los que no se recibio ack
    """
    timeOutReenvio = 20 #tiempo en segundos
    
    while 1:
        for i in datosEnVuelo:
            for j in datosEnVuelo[i]:
                tiempoSalida = datosEnVuelo[i][j]['Timestamp']
                #me fijo si se vencio el timeout de la parte del mensaje
                if ( (time.time() - tiempoSalida) > timeOutReenvio ):
                    #modifico el tiempo de salida del mensaje con el tiempo actual
                    datosEnVuelo[i][j]['Timestamp'] = time.time()
                    #reenvio la parte del mensaje
                    serverCanal.enviarAEC(datosEnVuelo[i][j])
        time.sleep(0.5)

def enviarAEC(mensaje):
    """
    agrega el mensaje a los mensajes en vuelo y lo manda a la EC
    """
    
    #obtengo el id del mensaje y el id de la parte del mensaje
    idMsg = mensaje['Id Mensaje']
    idPar = mensaje['Id Parte']
    
    #veo que el idmsg este definido en datos en vuelo, si no esta lo creo
    if idMsg not in datosEnVuelo:
        datosEnVuelo[idMsg] = {idPar: mensaje}
    else:
        datosEnVuelo[idMsg][idPar] =  mensaje
    
    #lo envio a la estacion central
    serverCanal.enviarAEC(datosEnVuelo[idMsg][idPar])
    
    return 1
    

def recibirDeEC(mensaje):
    """
    funcion que recibe la TR de la estacion central y los procesa
    """
    #me fijo que el mensaje sea un respuesta y un ack y que sea para mi TR
    if ( (mensaje['Tipo Mensaje'] in ['RESPUESTA']) and mensaje['Contenido']['Respuesta'] in ['ACK'] and mensaje['Id TR'] == id_tr ):
        idMsg = mensaje['Contenido']['Id Mensaje']
        idPar = mensaje['Contenido']['Id Parte']
        #me fijo si la parte del mensaje ackeado esta en mis datos en vuelo, entonces la borro.
        if (idMsg in datosEnVuelo) and (idPar in datosEnVuelo[idMsg]):
                del datosEnVuelo[idMsg][idPar]
    return 1


def enviadorTR(id_tr):

    #defino el host y puerto donde va a escuchar para el sincronizador
    host = "localhost"
    puerto = 6000 + id_tr
    
    #defino el servidor donde escucha el canal
    serverCanal = xmlrpclib.ServerProxy("http://%s:%s/"%(hostCanal,puertoCanal))
    
    
    #creo un thread para la funcion que verifica si hay que reenviar los mensajes
    verificadorReenviador = threading.Thread(target = verificarDatos)
    verificadorReenviador.setDaemon(True)
    verificadorReenviador.start()
    
    #ejecuto el servidor de mensajes para la tr y el canal
    serverTr = SimpleXMLRPCServer((host, puerto))
    print "Escuchando en el puerto...", puerto
    #registro las funciones que necesito
    serverTr.register_function(enviarAEC, "enviarAEC")
    serverTr.register_function(recibirDeEC, "recibirDeEC")
    serverTr.serve_forever()