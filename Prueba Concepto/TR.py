import sys, time, json, random

def guardar_mensaje(dato, id_men):
	print "Estoy ecribiendo con id de mensaje : " + str(id_men)
	archivo = open("TR\\Id TR - " + str(id_TR) + " - Id Mensaje - "+ str(id_men) + ".tr", "w")
	informacion = datos_auditoria(id_men, 'DATOS')
	informacion['Contenido'] = dato
	dato_json = json.dumps(informacion)
	archivo.write(dato_json)
	archivo.close()	

def datos_auditoria(id_men, tipo_mensaje):
	informacion = {'Id TR' : id_TR}
	informacion['Timestamp'] = time.time()
	informacion['Id Mensaje'] = id_men
	informacion['Id Parte'] = 1
	informacion['Tipo Mensaje'] = tipo_mensaje
	return informacion

id_TR = sys.argv[1]
i = 0
id_mensaje = 0

while i < 4:
	time.sleep(1)
	temperatura = random.random()
	humedad = random.randint(0, 100)
	datos = {'Temperatura' : temperatura, 'Humedad' : humedad}
	guardar_mensaje(datos, id_mensaje)
	i += 1
	id_mensaje += 1

	
#def inicializar_alarma():
	


#raw_input("Pulsa una tecla para continuar...") 