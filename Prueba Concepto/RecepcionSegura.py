import time
import random
import threading
import sys
import copy
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from xmlrpclib import ServerProxy
import Encriptador
import json


def verificarABMTR():
    while 1:
        for id in publicadores_a_tr.keys():
            i = int(id)
            diferencia_tiempo = time.time() - mensajes_pendientes[i]['Ultimo Timestamp Recibido']
            if mensajes_pendientes[i]['Esta Caida'] :
                if diferencia_tiempo < tiempo_caida : 
                    mensajes_pendientes[i]['Esta Caida'] = False
                    print "Se recupero la TR", i
            else :
                if diferencia_tiempo > tiempo_caida :
                    mensajes_pendientes[i]['Esta Caida'] = True
                    print "Se cayo TR", i
        time.sleep(5)        



def recibirDeTR(mensaje):
    enc = Encriptador.Encriptador()
    
    print "Estoy recibiendo de TR",
    #desencripto el mensaje que llega para poder tratarlo
    mensaje_desencriptado = enc.desencriptar(mensaje)
    
    print mensaje_desencriptado['Id TR'],
    print " mensaje: ", mensaje_desencriptado['Id Mensaje'],
    print " parte: ",mensaje_desencriptado['Id Parte']
    
    if mensaje_desencriptado['Tipo Mensaje'] in ['SUSCRIPCION']:
        suscribirOtraEC(mensaje_desencriptado)
        return 0
    if mensaje_desencriptado['Tipo Mensaje'] in ['DATOS DESDE EC']:
        guardarMensajeRecibidoDeEC(mensaje_desencriptado)
        return 0
        
    #genero el ack
    mensaje_respuesta = respuesta_ack(mensaje_desencriptado)
    
    #antes de enviar, encripto los datos, y agrego un campo con el id de la tr para que el canal lo direccione    
    mensaje_encriptado = enc.encriptar(mensaje_respuesta)
    proxy_canal.enviarATR(mensaje_respuesta['Id TR'], mensaje_encriptado)
    
    id_tr_actual = mensaje_desencriptado['Id TR']
    if mensajes_pendientes[id_tr_actual]['Esta Caida'] and mensaje_desencriptado['Id Mensaje'] == 101 :
        if mensaje_desencriptado['Timestamp'] > max_timestamp_de_mensaje_TR(mensaje_desencriptado['Id TR']):
            if max_timestamp_de_mensaje_TR(mensaje_desencriptado['Id TR']) != -1 :
                mensajes_pendientes[id_tr_actual]['Ultimo Id Enviado'] = 100
                del mensajes_pendientes[id_tr_actual]['Mensajes']
                mensajes_pendientes[id_tr_actual]['Mensajes'] = []
            
    guardarMensaje(mensaje_desencriptado)
    tratarDeEnpaquetarYMandar(mensaje_desencriptado['Id Mensaje'], mensaje_desencriptado['Id TR'])

    return 0

def max_timestamp_de_mensaje_TR(id_tr):
    max_timestamp = -1
    for men in mensajes_pendientes[id_tr]['Mensajes'] :
        if men['Timestamp'] > max_timestamp : 
            max_timestamp = men['Timestamp']
    return max_timestamp
            

def respuesta_ack(mensaje):
    rta = {}
    rta['Id TR'] = mensaje['Id TR']
    rta['Id EC'] = idEC
    rta['Timestamp'] = time.time()
    rta['Id Mensaje'] = 1
    rta['Id Parte'] = 1
    rta['Cantidad Partes'] = 1
    rta['Tipo Mensaje'] = 'RESPUESTA'
    rta['Contenido'] = {'Respuesta' : 'ACK','Id Mensaje': mensaje['Id Mensaje'],'Id Parte': mensaje['Id Parte']}  
    return rta
    
def guardarMensaje(mensaje):
    el_mensaje_esta = False
    mensajes_pendientes[mensaje['Id TR']]['Ultimo Timestamp Recibido'] = time.time()
    
    if mensajes_pendientes[mensaje['Id TR']]['Ultimo Id Enviado'] == None:
       mensajes_pendientes[mensaje['Id TR']]['Ultimo Id Enviado'] = mensaje['Id Mensaje'] - 1
    
    if mensaje['Id Mensaje'] > mensajes_pendientes[mensaje['Id TR']]['Ultimo Id Enviado'] : 
        for mensaje_viejo in mensajes_pendientes[mensaje['Id TR']]['Mensajes']:
            if mensaje_viejo['Id Mensaje'] == mensaje['Id Mensaje']:
                if mensaje_viejo['Id Parte'] == mensaje['Id Parte']:
                    el_mensaje_esta = True
                    break
    if not el_mensaje_esta :
        mensajes_pendientes[mensaje['Id TR']]['Mensajes'].append(mensaje)

def tratarDeEnpaquetarYMandar(id_mensaje, id_tr_page):
    #print "Trato de empaquetar", "Con id_mensaje", id_mensaje, "Y id_tr", id_tr_page
    if id_mensaje == mensajes_pendientes[id_tr_page]['Ultimo Id Enviado'] + 1:
        mensajes = mensajes_pendientes[id_tr_page]['Mensajes']
        partes = [msg for msg in mensajes if msg['Id Mensaje'] == id_mensaje]
        if len(partes) == 0:
            return
        if partes[0]['Cantidad Partes'] == len(partes):
            paquete = {}
            for key in partes[0].keys():
                paquete[key] = partes[0][key]

            del paquete['Contenido']
            paquete['Id Parte'] = 1
            paquete['Contenido'] = {}

            for parte in partes:
                for key in parte['Contenido'].keys():
                    paquete['Contenido'][key] = parte['Contenido'][key]
            
            for un_mensaje in mensajes_pendientes[id_tr_page]['Mensajes']:
                if un_mensaje['Id Mensaje'] == id_mensaje:
                    mensajes_pendientes[id_tr_page]['Mensajes'].remove(un_mensaje)
                    
            mensajes_pendientes[id_tr_page]['Ultimo Id Enviado'] += 1
            
            #una vez que tengo el paquete completo, lo guardo en el archivo
            archivo = open("EC\\Id EC - " + str(idEC) + " - Id TR - " + str(paquete['Id TR']) + " - Id Mensaje - "+ str(paquete['Id Mensaje']) + ".ec", "w")
            dato_json = json.dumps(paquete)
            archivo.write(dato_json)
            archivo.close()
            publicarDatoDeTR(paquete)
            print "Me llego el mensaje: %s de la TR: %s completo y lo mande como paquete"%(id_mensaje,id_tr_page)
            tratarDeEnpaquetarYMandar(id_mensaje + 1, id_tr_page)

def guardarMensajeRecibidoDeEC(mensaje):
    archivo = open("EC\\ECVecina Id EC - " + str(idEC) + " - Id TR - " + str(mensaje['Id TR']) + " - Id Mensaje - "+ str(mensaje['Id Mensaje']) + ".ec", "w")
    dato_json = json.dumps(mensaje)
    archivo.write(dato_json)
    archivo.close()
    
def publicarDatoDeTR(mensaje):
    enc = Encriptador.Encriptador()
    
    los_suscriptos = serverPublicador.suscriptos()
    print "Estoy publicando un mensaje, hay", len(los_suscriptos.keys()), "suscriptos"
    for una_ec in los_suscriptos.keys():
        print "La EC", una_ec, "Se suscribio a", len(los_suscriptos[una_ec].keys()), "TRS"
        for una_tr in los_suscriptos[una_ec].keys():
            if int(mensaje['Id TR']) == int(una_tr):
                sensores = los_suscriptos[una_ec][una_tr] # arreglo de sensores
                mensaje_nuevo = copy.deepcopy(mensaje)
        
                for un_sensor in mensaje_nuevo['Contenido'].keys():
                    if not un_sensor in sensores:
                        del mensaje_nuevo['Contenido'][un_sensor]
                
                mensaje_nuevo['Cantidad Partes'] = 1
                mensaje_nuevo['Tipo Mensaje'] = 'DATOS DESDE EC'
                mensaje_nuevo_encriptado = enc.encriptar(mensaje_nuevo)
                print "Estoy enviando a la EC", una_ec, "un mensaje"
                proxy_canal.enviarAEC(int(una_ec), mensaje_nuevo_encriptado, False)

    
def suscribirme():
    suscribimeATrs()
    suscribimeAEcs()
    
def suscribimeATrs():
    print "Me voy a suscribir a", len(publicadores_a_tr.keys()), " TRs"
    for id_TR_str in publicadores_a_tr:
        id_TR = int(id_TR_str)
        sensores = publicadores_a_tr[id_TR_str]
        print "me voy a suscribir a la TR", id_TR, "con los sensores:", sensores
        msj = {}
        msj['Id TR'] = id_TR
        msj['Id EC'] = idEC
        msj['Timestamp'] = time.time()
        msj['Id Mensaje'] = 1
        msj['Id Parte'] = 1
        msj['Cantidad Partes'] = 1
        msj['Tipo Mensaje'] = 'SUSCRIPCION'
        msj['Contenido'] = {'Id EC' : idEC, 'Sensores': sensores}
        
        enc = Encriptador.Encriptador()
        mensaje_encriptado = enc.encriptar(msj)
        proxy_canal.enviarATR(msj['Id TR'], mensaje_encriptado, False)

def suscribimeAEcs():
    print "Me voy a suscribir a", len(publicadores_a_ec.keys()), " Ecs"
    for id_EC_str in publicadores_a_ec:
        id_EC_destino = int(id_EC_str)
        trs_y_sensores = publicadores_a_ec[id_EC_str]
        print "me voy a suscribir a la EC", id_EC_destino, "con los trs y sensores:", trs_y_sensores
        msj = {}
        msj['Id TR'] = id_EC_destino
        msj['Id EC'] = idEC
        msj['Timestamp'] = time.time()
        msj['Id Mensaje'] = 1
        msj['Id Parte'] = 1
        msj['Cantidad Partes'] = 1
        msj['Tipo Mensaje'] = 'SUSCRIPCION'
        msj['Contenido'] = {'Id EC' : idEC, 'TRs Y Sensores': trs_y_sensores}
        
        enc = Encriptador.Encriptador()
        mensaje_encriptado = enc.encriptar(msj)
        proxy_canal.enviarAEC(id_EC_destino, mensaje_encriptado, False)
      
def suscribirOtraEC(msj):
    print "Suscribiendo la EC vecina: ", msj['Contenido']['Id EC'],
    serverPublicador.suscribir(msj['Contenido']['Id EC'], msj['Contenido']['TRs Y Sensores'])
    print "Ahora hay ", len(serverPublicador.suscriptos()), "ECs suscriptas"
    
def inicializar(tiempo_caida_nvo, idEC_nvo, publicadores_a_tr_par, publicadores_a_ec_par):
    # SERVER
    global mensajes_pendientes
    global tiempo_caida
    global idEC
    global publicadores_a_tr
    global publicadores_a_ec
    global proxy_canal
    global serverPublicador
    
    tiempo_caida = int(tiempo_caida_nvo)
    idEC = int(idEC_nvo)
    publicadores_a_tr = publicadores_a_tr_par
    publicadores_a_ec = publicadores_a_ec_par
    
    host = "localhost"
    puerto_canal = 5555
    puerto_ec = 7000 + idEC
    puerto_publicador = 9000 + idEC
    
    print "Soy la Recepcion Segura de la EC con id = ", idEC
    
    #creo el descriptor para comunicarme con el canal
    proxy_canal = ServerProxy("http://%s:%s/"%(host,puerto_canal))
    #creo el descriptor para el servidor que escucha suscripciones de otras ecs
    serverPublicador = xmlrpclib.ServerProxy("http://%s:%s/"%(host,puerto_publicador))
    
    #creo la estructura para mantener los mensajes pendientes de las trs
    mensajes_pendientes = {}
    for id in publicadores_a_tr.keys():
        i = int(id)
        mensajes_pendientes[i] = {'Mensajes':[], 'Ultimo Id Enviado':None, 'Ultimo Timestamp Recibido': time.time(), 'Esta Caida':False}

    #creo el descriptor para el servidor que escucha los mensajes que vienen por
    #medio del canal, de las trs.
    server = SimpleXMLRPCServer((host, puerto_ec), SimpleXMLRPCRequestHandler, False)
    
    print "Escuchando en el puerto... ", puerto_ec
    
    #registro las funciones para recibir info de las trs
    server.register_function(recibirDeTR, "recibirDeTR")
    
    #me suscribo a las ecs y a las trs que me pasaron por parametros
    suscribirme()
    
    #thread que se encarga de ver si se caen o levantan las trs
    un_thread = threading.Thread(target = verificarABMTR, args = ())
    un_thread.setDaemon(True)
    un_thread.start()
    
    server.serve_forever()    

#if __name__ == '__main__':
#    main()


