import signal, os
import sys, time, json, random, Encriptador
from multiprocessing import Process



def guardar_mensaje(dato, id_men, id_TR):
	print "Estoy ecribiendo con id de mensaje : " + str(id_men)
	archivo = open("TR\\Id TR - " + str(id_TR) + " - Id Mensaje - "+ str(id_men) + ".tr", "w")
	informacion = datos_auditoria(id_men, 'DATOS',id_TR)
	informacion['Contenido'] = dato
	dato_json = json.dumps(informacion)
	un_encriptador = Encriptador.Encriptador()
	archivo.write(un_encriptador.encriptar(dato_json))
	archivo.close()	

def datos_auditoria(id_men, tipo_mensaje, id_TR):
	informacion = {'Id TR' : id_TR}
	informacion['Timestamp'] = time.time()
	informacion['Id Mensaje'] = id_men
	informacion['Id Parte'] = 1
	informacion['Tipo Mensaje'] = tipo_mensaje
	return informacion

def enviarMensaje(id_mensaje, id_TR):
	temperatura = random.random()
	humedad = random.randint(0, 100)
	datos = {'Temperatura' : temperatura, 'Humedad' : humedad}
	guardar_mensaje(datos, id_mensaje, id_TR)
	

def frecuenciaEnvio(veces, tiempo, id_TR):
    id_mensaje = 0
    for i in range(veces):  
        enviarMensaje(id_mensaje, id_TR)
        time.sleep(tiempo)
        id_mensaje = id_mensaje + 1

	

canTR = int(sys.argv[1])
tiempo = int(sys.argv[2])
veces = int(sys.argv[3])
#Vamos a simular 5 trs


if __name__ == '__main__':
    #creo las 5 trs
    trs = []
    for i in range(canTR):
        hacerXTiempo = Process(target = frecuenciaEnvio, args = (veces, tiempo, i))
        trs.append(hacerXTiempo)
    
    #las arranco
    for i in range(canTR):
        trs[i].start()

    # las termino
    for i in range(canTR):
        trs[i].join()


#def inicializar_alarma():
#raw_input("Pulsa una tecla para continuar...") 