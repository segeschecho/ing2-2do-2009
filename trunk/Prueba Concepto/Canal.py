import xmlrpclib
import time
import random
from SimpleXMLRPCServer import SimpleXMLRPCServer

host = "localhost"
puerto_canal = 5555
puerto_ec = 5557
puerto_tr = 6000

probabilidad_perdida = 0.05
delay_min = 0.05
delay_max = 15 

def enviarAEC(mensaje):
	enviarMensaje(mensaje, proxy_ec.recibirDeTR)
	return 0

def enviarATR(mensaje):
	enviarMensaje(mensaje, proxys_tr[mensaje.IdTR].recibirDeEC)
	return 0
	
def enviarMensaje(mensaje, recibir):
	random = random.random()
	if(random > probabilidad_perdida):
		delay = random.uniform(delay_min, delay_max)
		time.sleep(delay)
		recibir(mensaje)
		
server = SimpleXMLRPCServer((host, puerto_canal))
print "Escuchando en el puerto... ", puerto_canal
server.register_function(enviarAEC, "enviarAEC")
server.register_function(enviarATR, "enviarATR")
server.serve_forever()

proxy_ec = ServerProxy("http://%s:%s/"%(host,puerto_ec))

proxys_tr = {}
for i in range(1, 10)
	puerto_actual = puerto_tr + i
	proxys_tr[i] = ServerProxy("http://%s:%s/"%(host, puerto_actual))
