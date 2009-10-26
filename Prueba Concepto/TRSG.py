import signal, os
import sys, time, json, random, Encriptador
from multiprocessing import Process #para  crear procesos a nivel del sistema operativo
import xmlrpclib


def guardar_mensaje(dato, id_men, id_TR):
    """
        Genera un archivo con el ID de la TR y el ID del mensaje y guarda los datos
    """
    print "Estoy ecribiendo con id de mensaje : " + str(id_men)
    archivo = open("TR\\Id TR - " + str(id_TR) + " - Id Mensaje - "+ str(id_men) + ".tr", "w")
    informacion = datos_auditoria(id_men, 'DATOS',id_TR)
    informacion['Contenido'] = dato
    dato_json = json.dumps(informacion)
    un_encriptador = Encriptador.Encriptador()
    archivo.write(un_encriptador.encriptar(dato_json))
    archivo.close()
    return dato_json

def datos_auditoria(id_men, tipo_mensaje, id_TR):
    """
        Genera informacion de auditoria como timespam y partes del mensaje
    """
    informacion = {'Id TR' : id_TR}
    informacion['Timestamp'] = time.time()
    informacion['Id Mensaje'] = id_men
    informacion['Id Parte'] = 1
    informacion['Tipo Mensaje'] = tipo_mensaje
    return informacion

def enviarMensaje(id_mensaje, id_TR):
    """
        Genera informacion al azar para enviar
    """
    temperatura = random.random()
    humedad = random.randint(0, 100)
    datos = {'Temperatura' : temperatura, 'Humedad' : humedad}
    return guardar_mensaje(datos, id_mensaje, id_TR)
	

def frecuenciaEnvio(veces, tiempo, id_TR):
    """
        Funcion que se encarga de enviar informacion de una TR
        cada cierto tiempo y cierta cantidad de veces
    """
    host = "localhost"
    puerto = 5555

    proxy = xmlrpclib.ServerProxy("http://%s:%s/"%(host,puerto))
    
    id_mensaje = 0
    for i in range(veces):
        proxy.enviarAEc(enviarMensaje(id_mensaje, id_TR))
        time.sleep(tiempo)
        id_mensaje = id_mensaje + 1
    
	


if __name__ == '__main__':
    #parte que genera TR y hace que envien informacion.
    #obtengo los parametros que me pasan para que todo ande bien
    if len(sys.argv) < 4:
        print "faltan parametros..."
        print "1 - Cantidad de TRs a simular"
        print "2 - Intervalo de tiempo para el envio (usual 60)"
        print "3 - Cantidad de mensajes que enviaran cada TR"
        sys.exit(1)
            
    canTR = int(sys.argv[1])
    tiempo = int(sys.argv[2])
    veces = int(sys.argv[3])
    #Vamos a simular 5 trs

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
