import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import threading
import time
import sys
import Encriptador
import Partidor


#creo el servidor para el enviador
hostCanal = "localhost"
puertoCanal = 5555
puertoPublicadorFalso = 9000
hostPublicador = "localhost"

# serverCanal = xmlrpclib.ServerProxy("http://%s:%s/"%(hostCanal,puertoCanal))
# serverPublicador = xmlrpclib.ServerProxy("http://%s:%s/"%(hostCanal, puertoPublicadorFalso))

#estructura que guarda los datos en vuelo es un doble diccionario con ID_MSG y ID_PARTE
datosEnVuelo = {}


def pruebaEnviadorTR(mensaje):
    while 1:
        pass

def verificarDatos():
    """
    funcion que se encarga de ver si hay que reenviar mensajes de los que no se recibio ack
    """
    enc = Encriptador.Encriptador()
    timeOutReenvio = 20 #tiempo en segundos
    
    while 1:
        # datos en vuelo es un dicc de (idEC, idMsg) a todas las partes de un Msg
        for i in datosEnVuelo:
            for j in datosEnVuelo[i]:
                tiempoSalida = datosEnVuelo[i][j]['Timestamp']
                #me fijo si se vencio el timeout de la parte del mensaje
                if ( (time.time() - tiempoSalida) > timeOutReenvio ):
                    #modifico el tiempo de salida del mensaje con el tiempo actual
                    datosEnVuelo[i][j]['Timestamp'] = time.time()
                    #reenvio la parte del mensaje
                    print "Reenviando mensaje: %s parte: %s"%(i,j)
                    msj_enc = enc.encriptar(datosEnVuelo[i][j])
                    serverCanal.enviarAEC(i[0], msj_enc)
        time.sleep(0.5)


def publicar(mensaje):
    """
    agrega el mensaje a los mensajes en vuelo lo manda a la EC que se suscribieron
    """
    enc = Encriptador.Encriptador()
    partidor = Partidor.Partidor()
    
    los_suscriptores = serverPublicador.suscriptos()
    
    print "Estoy publicado en mensaje", mensaje
    print "Existen", len(los_suscriptores.keys())," ECs suscriptas" 
    print "Los suscriptos son",los_suscriptores.keys()
    for un_suscriptor_str in los_suscriptores.keys():
        print "A"
        un_suscriptor = int(un_suscriptor_str)
        mensaje_nuevo = mensaje.copy()
        for un_sensor in mensaje_nuevo['Contenido'].keys():
            if not un_sensor in los_suscriptores[un_suscriptor_str]:
                del mensaje_nuevo['Contenido'][un_sensor]
        print "B"        
        #obtengo el id del mensaje y el id de la parte del mensaje
        idMsg = mensaje_nuevo['Id Mensaje']
        idEC = un_suscriptor
        #agarro el mensaje_nuevo y lo parto para que viajen por sms
        mensajePartido = partidor.partir(mensaje_nuevo)
        print "C"
        #encripto las partes  antes de enviar
        for i in mensajePartido.keys():
            idPar = mensajePartido[i]['Id Parte']
            
            #veo que el idmsg este definido en datos en vuelo, si no esta lo creo
            if (idEC, idMsg) not in datosEnVuelo:
                datosEnVuelo[(idEC, idMsg)] = {idPar : mensajePartido[i]}
            else:
                datosEnVuelo[(idEC, idMsg)][idPar] =  mensajePartido[i]
                
            msj_enc = enc.encriptar(mensajePartido[i])
        
            #lo envio a la estacion central
            print "Voy a enviar el mensaje :", msj_enc
            serverCanal.enviarAEC(un_suscriptor, msj_enc)
            print "Enviando a la EC : %s el mensaje_nuevo: %s, parte: %s"%(str(idEC),str(idMsg), str(idPar))
        print "D"
    return 1


def recibirDeEC(mensaje):
    """
    funcion que recibe la TR de la estacion central y los procesa
    """
    
    print "Estoy recibiendo mensaje de la EC"
    enc = Encriptador.Encriptador()
    #desencripto el mensaje
    msj_des = enc.desencriptar(mensaje)
    #me fijo que el mensaje sea un respuesta y un ack y que sea para mi TR
    if ( (msj_des['Tipo Mensaje'] in ['RESPUESTA']) and msj_des['Contenido']['Respuesta'] in ['ACK']):
        print "Recibo un ACK de la EC"
        idMsg = msj_des['Contenido']['Id Mensaje']
        idPar = msj_des['Contenido']['Id Parte']
        idEC  = msj_des['Id EC']
        #me fijo si la parte del mensaje ackeado esta en mis datos en vuelo, entonces la borro.
        
        if ((idEC,idMsg) in datosEnVuelo) and (idPar in datosEnVuelo[(idEC,idMsg)]):
                del datosEnVuelo[(idEC,idMsg)][idPar]
                print 'Borro datos al llegar ACK'
    
    if(msj_des['Tipo Mensaje'] in ['SUSCRIPCION']):
        print "Llego un mensaje de tipo suscripcion"
        print 'lo anterior a suscribir', msj_des['Contenido']['Id EC']
        print 'lo anterior a suscribir 2',msj_des['Contenido']['Sensores']
        serverPublicador.suscribir(msj_des['Contenido']['Id EC'],msj_des['Contenido']['Sensores'])
    return 1


def enviadorTR(id_tr):

    #defino el host y puerto donde va a escuchar para el sincronizador
    host = "localhost"
    puerto = 6000 + id_tr
    puerto_publicador = 9000 + id_tr
    
    
    #defino el servidor donde escucha el canal
    serverCanal = xmlrpclib.ServerProxy("http://%s:%s/"%(hostCanal,puertoCanal))
    serverPublicador = xmlrpclib.ServerProxy("http://%s:%s/"%(hostPublicador,puerto_publicador))
    global serverCanal
    global serverPublicador
    #creo un thread para la funcion que verifica si hay que reenviar los mensajes
    verificadorReenviador = threading.Thread(target = verificarDatos)
    verificadorReenviador.setDaemon(True)
    verificadorReenviador.start()
    
    #ejecuto el servidor de mensajes para la tr y el canal
    serverTr = SimpleXMLRPCServer((host, puerto), SimpleXMLRPCRequestHandler, False)
    print "Escuchando en el puerto...", puerto
    #registro las funciones que necesito

    serverTr.register_function(publicar, "publicar")
    serverTr.register_function(recibirDeEC, "recibirDeEC")

    serverTr.serve_forever()
