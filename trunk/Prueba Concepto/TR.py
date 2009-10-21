import sys, time, json, random

def guardar_mensaje(dato, id_men):
	print "Estoy ecribiendo con id de mensaje : " + str(id_men)
	archivo = open("TR\\ID TR " + str(id_TR) + " - ID SMS "+ str(id_men)+".tr", "w")
	archivo.write("Esto es un sms de una TR con id " + str(id_TR) + "\n")
	dato_json = json.dumps(dato)
	archivo.write(dato_json)
	archivo.close()	
	

def prueba():
	print 'hoal esto paso despues'

id_TR = sys.argv[1]
i = 0
id_mensaje = 0

while i < 10:
	time.sleep(1)
	hora = time.time()
	temperatura = random.random()
	datos = {'TimeStamp': hora, 'Temperatura': temperatura}
	guardar_mensaje(datos, id_mensaje)
	i += 1
	id_mensaje += 1

	
#def inicializar_alarma():
	


#raw_input("Pulsa una tecla para continuar...") 