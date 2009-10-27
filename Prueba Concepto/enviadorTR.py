import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import time
import sys


#creo el servidor para el enviador
hostCanal = "localhost"
puertoCanal = 5555

datosEnVuelo = {}

def verificarDatos():
    timeOutReenvio = 20 #tiempo en segundos
    
    while 1:
        for i in datosEnVuelo:
            for j in datosEnVuelo[i]:
                tiempoSalida = datosEnVuelo[i][j]['Timestamp']
                if ( (time.time() - tiempoSalida) > timeOutReenvio ):
                    #reenvio por que se vencio el timeout
                    serverCanal.enviarAEC(datosEnVuelo[i][j])
        time.sleep(0.5)

def enviarAEC(mensaje):
    idMsg = mensaje['Id Mensaje']
    idPar = mensaje['Id Parte']
    
    if idMsg not in datosEnVuelo:
        datosEnVuelo[idMsg] = {idPar: mensaje}
    else:
        datosEnVuelo[idMsg][idPar] =  mensaje
    serverCanal.enviarAEC(datosEnVuelo[idMsg][idPar])
    
    return 1
    

def recibirDeEC(mensaje):
    #me fijo que el mensaje sea un respuesta y un ack
    if ( (mensaje['Tipo Mensaje'] in ['RESPUESTA']) and mensaje['Contenido']['Respuesta'] in ['ACK'] and mensaje['Id TR'] == id_tr ):
        idMsg = mensaje['Contenido']['Id Mensaje']
        idPar = mensaje['Contenido']['Id Parte']
        if idMsg in datosEnVuelo:
            if idPar in datosEnVuelo[idMsg]:
                del datosEnVuelo[idMsg][idPar]
    return 1

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Falta el argumento del numero de TR"
        sys.exit(1)
        
    id_tr = sys.argv[1]
    
    host = "localhost"
    puerto = 6000 + int(id_tr)
    
    #defino el servidor donde escucha el canal
    serverCanal = xmlrpclib.ServerProxy("http://%s:%s/"%(hostCanal,puertoCanal))
    
    #creo un thread para la funcion que verifica si hay que reenviar los mensajes
    verificadorReenviador = threading.Thread(target = verificarDatos)
    verificadorReenviador.start()
    
    #ejecuto el servidor de mensajes para la tr y el canal
    serverTr = SimpleXMLRPCServer((host, puerto))
    print "Escuchando en el puerto...", puerto
    #registro las funciones que necesito
    serverTr.register_function(enviarAEC, "enviarAEC")
    serverTr.register_function(recibirDeEC, "recibirDeEC")
    serverTr.serve_forever()
    
