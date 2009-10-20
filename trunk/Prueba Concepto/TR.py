import sys, time

def guardar_mensaje(dato):
	print "Estoy ecribiendo " + str(dato)
	archivo = open("TR\\ID " + str(id_TR) + " - "+str(dato)+".txt", "w")
	archivo.write("Esto es un sms de una TR con id " + str(id_TR))
	archivo.write(str(dato))
	archivo.close()	

def prueba():
	print 'hoal esto paso despues'

id_TR = sys.argv[1]
i = 0
while i < 10:
	time.sleep(1)
	guardar_mensaje(i)
	i = i + 1
	
#def inicializar_alarma():
	


#raw_input("Pulsa una tecla para continuar...") 