import time
import random
import time
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy

print "Soy la Recepcion Segura de la EC"
host = "localhost"
puerto_canal = 5555
puerto_ec = 5557
tiempo_caida = 30
# deberia ser 120
proxy_canal = ServerProxy("http://%s:%s/"%(host,puerto_canal))

mensajes_pendientes = {}
for i in range(1, 10):
	mensajes_pendientes[i] = {'Mensajes':[], 'Ultimo Id Enviado':0, 'Ultimo Timestamp Recibido': time.time(), 'Esta Caida':False}

def verificarABMTR():
	while 1:
		for i in range(1, 10):
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
	print "Estoy puteando ", mensaje
	mensaje_respuesta = respuesta_ack(mensaje)
	proxy_canal.enviarATR(mensaje_respuesta)
	guardarMensaje(mensaje)
	tratarDeEnpaquetarYMandar(mensaje['Id Mensaje'], mensaje['Id TR'])
	print "Termine de empaquetar"
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

def tratarDeEnpaquetarYMandar(id_tr, id_mensaje):
	print "Trato de empaquetar"
	if id_mensaje == mensajes_pendientes[id_tr]['Ultimo Id Enviado'] + 1:
		mensajes = mensajes_pendientes[id_tr]['Mensajes']
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
					
			for un_mensaje in mensajes_pendientes[id_tr]['Mensajes']:
				if un_mensaje['Id Mensaje'] == id_mensaje:
					mensajes_pendientes[id_tr]['Mensajes'].remove(un_mensaje)
					
			mensajes_pendientes[id_tr]['Ultimo Id Enviado']	+= 1	
			
			print "Me llego el mensaje completo", paquete
			
			

def main():
	# SERVER		
	server = SimpleXMLRPCServer((host, puerto_ec))
	print "Escuchando en el puerto... ", puerto_ec
	server.register_function(recibirDeTR, "recibirDeTR")
	server.serve_forever()

if __name__ == '__main__':
	main()