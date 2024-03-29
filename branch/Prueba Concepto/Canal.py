import time
import random
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from xmlrpclib import ServerProxy
import Encriptador
import sys


print "Soy el Canal"
host = "localhost"
puerto_canal = 5555
puerto_ec = 5557
puerto_tr = 6000

probabilidad_perdida = 0.05
delay_min = 0.05
delay_max = 2 # antes era 15 

# CLIENTE
proxy_ec = ServerProxy("http://%s:%s/"%(host,puerto_ec))

proxys_tr = {}
for i in range(1, 6):
    puerto_actual = puerto_tr + i
    proxys_tr[i] = ServerProxy("http://%s:%s/"%(host, puerto_actual))


def enviarAEC(mensaje):
    #proceso = Process(target = enviarMensaje, args = (mensaje))
    #proceso.start()
    print 'Me llego un mensaje de la TR'
    un_thread = threading.Thread(target = enviarMensaje, args = (mensaje, proxy_ec.recibirDeTR))
    un_thread.setDaemon(True)
    un_thread.start()
    return 0

def enviarATR(id_tr, mensaje):
    print 'Me llego una repuesta de la EC'
    otro_thread = threading.Thread(target = enviarMensaje, args = (mensaje, proxys_tr[id_tr].recibirDeEC))
    otro_thread.setDaemon(True)
    otro_thread.start()
    return 0
    
def enviarMensaje(mensaje, receptor):
    
    probabilidad_perdida_actual = random.random()
    if probabilidad_perdida_actual > probabilidad_perdida :
        delay = random.uniform(delay_min, delay_max)
        time.sleep(delay)
        receptor(mensaje)
        print "Estoy enviando el mensaje...OK"
    else :
        print "Estoy enviando el mensaje...FAIL"

def main():
        # SERVER        
        server = SimpleXMLRPCServer((host, puerto_canal), SimpleXMLRPCRequestHandler, False)
        print "Escuchando en el puerto... ", puerto_canal
        server.register_function(enviarAEC, "enviarAEC")
        server.register_function(enviarATR, "enviarATR")

        server.serve_forever()

if __name__ == '__main__':
        main()
