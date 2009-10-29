import time
import threading


def holass():
	print 'que choto'

def mensajes(veces, tiempo):
	print 'ejecutando holass %s veces cada %s segundos'%(veces,tiempo)
	for i in range(veces):
		holass()
		time.sleep(tiempo)

veces = 2
tiempo = 1
hiloLoco = threading.Thread(target = mensajes, args = (veces, tiempo))

hiloLoco.start()

hiloLoco.join()

#t = threading.Timer(1.0, holass)
#t.start()
#print 'mande el timer'