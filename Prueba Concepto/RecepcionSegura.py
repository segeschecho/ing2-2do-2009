import time
import random
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy
import Encriptador

print "Soy la Recepcion Segura de la EC"
host = "localhost"
puerto_canal = 5555
puerto_ec = 5557
tiempo_caida = 30
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
    print mensaje_desencriptado['Id TR']
    
    #genero el ack
    mensaje_respuesta = respuesta_ack(mensaje_desencriptado)
    
    #antes de enviar, encripto los datos, y agrego un campo con el id de la tr para que el canal lo direccione    
    mensaje_encriptado = enc.encriptar(mensaje_respuesta)
	
    proxy_canal.enviarATR(mensaje_respuesta['Id TR'], mensaje_encriptado)
    guardarMensaje(mensaje_desencriptado)
    #print "Este es el mensaje que me llega", mensaje, "y este es el id", mensaje['Id Mensaje']
    tratarDeEnpaquetarYMandar(mensaje_desencriptado['Id Mensaje'], mensaje_desencriptado['Id TR'])
    return 0

def respuesta_ack(mensaje):
	rta = {}
	rta['Id TR'] = mensaje['Id TR']
	rta['Timestamp'] = time.time()
	rta['Id Mensaje'] = 1
	rta['Id Parte'] = 1
	rta['Cantidad Partes'] = 1
	rta['Tipo Mensaje'] = 'RESPUESTA'
	rta['Contenido'] = {'Respuesta' : 'ACK','Id Mensaje': mensaje['Id Mensaje'],'Id Parte': mensaje['Id Parte']}  
	return rta
	
def guardarMensaje(mensaje):
	print "Voy a guardar el mensaje"
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
	print "Trato de empaquetar", "Con id_mensaje", id_mensaje, "Y id_tr", id_tr_page
	if id_mensaje == mensajes_pendientes[id_tr_page]['Ultimo Id Enviado'] + 1:
		mensajes = mensajes_pendientes[id_tr_page]['Mensajes']
		partes = [msg for msg in mensajes if msg['Id Mensaje'] == id_mensaje]
		if len(partes) == 0:
			print "Esto no deberia pasar"
		if partes[0]['Cantidad Partes'] == len(partes):
			paquete = {}
			for key in partes[0].keys():
				paquete[key] = partes[0][key]

			del paquete['Contenido']
			paquete['Contenido'] = {}

			for parte in partes:
				for key in parte.keys():
					paquete['Contenido'][key] = parte[key]
					
			for un_mensaje in mensajes_pendientes[id_tr_page]['Mensajes']:
				if un_mensaje['Id Mensaje'] == id_mensaje:
					mensajes_pendientes[id_tr_page]['Mensajes'].remove(un_mensaje)
					
			mensajes_pendientes[id_tr_page]['Ultimo Id Enviado']	+= 1	
			
			print "Me llego el mensaje completo y lo mande como paquete"
			
			

def main():
	# SERVER		
	server = SimpleXMLRPCServer((host, puerto_ec))
	print "Escuchando en el puerto... ", puerto_ec
	server.register_function(recibirDeTR, "recibirDeTR")
	server.serve_forever()

if __name__ == '__main__':
	main()
