import time
import random
import time
import thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib import ServerProxy

host = "localhost"
puerto_canal = 5555
puerto_ec = 5557

proxy_canal = ServerProxy("http://%s:%s/"%(host,puerto_canal))

mensajes_pendientes = {}
for i in range(1, 10):
	mensajes_pendientes[i] = {'Mensajes':[], 'Ultimo Id Enviado':0, 'Ultimo Timestamp Recibido': time.time(), 'Esta Caida':False}




def verificarABMTR():
	while 1:
		for i in range(1, 10):
			diferencia_tiempo = time.time() - mensajes_pendientes[i]['Ultimo Timestamp Recibido']
			if mensajes_pendientes[i]['Esta Caida'] :
				if diferencia_tiempo < 120 : 
					mensajes_pendientes[i]['Esta Caida'] = False
					print "Se recupero la TR", i
			if diferencia_tiempo > 120 :
				mensajes_pendientes[i]['Esta Caida'] = True
				print "Se cayo TR", i
		time.sleep(2)		
		
thread.start_new_thread(verificarABMTR,())

def recibirDeTR(mensaje):
        mensaje_respuesta = respuesta_ack(mensaje)
        proxy_canal.enviarATR(mensaje_respuesta)
        guardarMensaje(mensaje)
        tratarDeEnpaquetarYMandar(mensaje['Id Mensaje'], mensaje['Id TR'])
        print "Estoy puteando ", mensaje
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
	
def guardarMensaje(mensaje):
	el_mensaje_esta = False
	mensajes_pendientes[mensaje['Id TR']]['Ultimo Timestamp Recibido'] = time.time()
	if mensaje['Id Mensaje'] > mensajes_pendientes[mensaje['Id TR']]['Ultimo Id Enviado'] : 
		for mensaje_viejo in mensajes_pendientes[mensaje['Id TR']]['Mensajes']:
			if mensaje_viejo['Id Mensaje'] == mensaje['Id Mensaje']:
				if mensaje_viejo['Id Parte'] == mensaje['Id Parte']:
					el_mensaje_esta = True
					break
	if el_mensaje_esta :
		mensajes_pendientes[mensaje['Id TR']].append(mensaje)

def tratarDeEnpaquetarYMandar(id_tr, id_mensaje):
	if id_mensaje == mensajes_pendientes[id_tr]['Ultimo Id Enviado'] + 1:
		mensajes = mensajes_pendientes[id_tr]['Mensajes']
		partes = [msg for msg in mensajes if msg['Id Mensaje'] == id_mensaje]
		if partes[0]['Cantidad Partes'] == partes.length:
			paquete = {}
			for key in partes[0].keys():
				paquete[key] = partes[0][key]

			del paquete['Contenido']
			paquete['Contenido'] = {}

			for parte in partes:
				for key in parte.keys():
					paquete['Contenido'][key] = parte[key]
					mensajes.remove(parte)
			
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
