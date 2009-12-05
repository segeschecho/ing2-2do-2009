import time
import random
import threading
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from xmlrpclib import ServerProxy
import Encriptador
import json

tiempo_caida = int(sys.argv[1])
idEC = int(sys.argv[2])
publicadores = json.loads(sys.argv[3])

print "Los publicadores son eran", publicadores  
for id in publicadores.keys():
    sensores_unicode = publicadores[id]
    sensores_str = []
    for sensor_unicode in sensores_unicode:
        sensores_str.append(str(sensor_unicode))
    del publicadores[id]
    publicadores[str(id)] = sensores_str

print "Los publicadores son", publicadores    
#print sys.argv[3]
print "Soy la Recepcion Segura de la EC con id =", idEC
host = "localhost"
puerto_canal = 5555
puerto_ec = 7000 + idEC


# deberia ser 120
proxy_canal = ServerProxy("http://%s:%s/"%(host,puerto_canal))

mensajes_pendientes = {}
for i in range(1, 6):
    mensajes_pendientes[i] = {'Mensajes':[], 'Ultimo Id Enviado':100, 'Ultimo Timestamp Recibido': time.time(), 'Esta Caida':False}


def verificarABMTR():
    while 1:
        for i in range(1, 6):
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

un_thread = threading.Thread(target = verificarABMTR, args = ())
un_thread.setDaemon(True)
un_thread.start()

def recibirDeTR(mensaje):
    enc = Encriptador.Encriptador()
    
    print "Estoy recibiendo de TR",
    #desencripto el mensaje que llega para poder tratarlo
    mensaje_desencriptado = enc.desencriptar(mensaje)
    print mensaje_desencriptado['Id TR'],
    print " mensaje: ", mensaje_desencriptado['Id Mensaje'],
    print " parte: ",mensaje_desencriptado['Id Parte']
    
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
            archivo = open("EC\\Id EC - " + str(IdEC) + " - Id TR - " + str(paquete['Id TR']) + " - Id Mensaje - "+ str(paquete['Id Mensaje']) + ".ec", "w")
            dato_json = json.dumps(paquete)
            archivo.write(dato_json)
            archivo.close()
           
            print "Me llego el mensaje: %s de la TR: %s completo y lo mande como paquete"%(id_mensaje,id_tr_page)
            tratarDeEnpaquetarYMandar(id_mensaje + 1, id_tr_page)

def suscribirme():
    print "Me voy a suscribir a", len(publicadores.keys()), "TRs"
    for id_TR_str in publicadores:
        id_TR = int(id_TR_str)
        sensores = publicadores[id_TR_str]
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
        proxy_canal.enviarATR(msj['Id TR'], mensaje_encriptado)
        
def main():
    # SERVER        
    server = SimpleXMLRPCServer((host, puerto_ec), SimpleXMLRPCRequestHandler, False)
    print "Escuchando en el puerto... ", puerto_ec
    server.register_function(recibirDeTR, "recibirDeTR")
    suscribirme()
    server.serve_forever()    

if __name__ == '__main__':
    main()

