import signal, os
import sys, time, json, random, Encriptador

def guardar_mensaje(dato, id_men):
	print "Estoy ecribiendo con id de mensaje : " + str(id_men)
	archivo = open("TR\\Id TR - " + str(id_TR) + " - Id Mensaje - "+ str(id_men) + ".tr", "w")
	informacion = datos_auditoria(id_men, 'DATOS')
	informacion['Contenido'] = dato
	dato_json = json.dumps(informacion)
	un_encriptador = Encriptador.Encriptador()
	archivo.write(un_encriptador.encriptar(dato_json))
	archivo.close()	

def datos_auditoria(id_men, tipo_mensaje):
	informacion = {'Id TR' : id_TR}
	informacion['Timestamp'] = time.time()
	informacion['Id Mensaje'] = id_men
	informacion['Id Parte'] = 1
    informacion['Cantidad partes'] = 1
	informacion['Tipo Mensaje'] = tipo_mensaje
	return informacion

def handler(a, b):
	id_mensaje += 1
	hacer(id_mensaje)
	
id_TR = sys.argv[1]
id_mensaje = 0

def hacer(id_mensaje):
	temperatura = random.random()
	humedad = random.randint(0, 100)
	datos = {'Temperatura' : temperatura, 'Humedad' : humedad}
	guardar_mensaje(datos, id_mensaje)
	id_mensaje += 1
	if ( id_mensaje < 5 ):
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(1)

hacer(id_mensaje)

#def inicializar_alarma():
#raw_input("Pulsa una tecla para continuar...") 