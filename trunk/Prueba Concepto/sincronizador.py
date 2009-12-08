import signal, os
import sys, time, json, random
from multiprocessing import Process #para  crear procesos a nivel del sistema operativo
import xmlrpclib

hostEnviador = "localhost"
puertoEnviador = 6000 #hay que sumarle el ID_TR


def guardar_mensaje(dato, id_men, id_TR):
    """
        Genera un archivo con el ID de la TR y el ID del mensaje y guarda los datos
    """
    print "Estoy ecribiendo con id de mensaje : " + str(id_men)
    archivo = open("TR\\Id TR - " + str(id_TR) + " - Id Mensaje - "+ str(id_men) + ".tr", "w")
    informacion = datos_auditoria(id_men, 'DATOS',id_TR)
    informacion['Contenido'] = dato
    dato_json = json.dumps(informacion)
    #un_encriptador = Encriptador.Encriptador()
    archivo.write(dato_json)
	#un_encriptador.encriptar(dato_json))
    archivo.close()
    return informacion

def datos_auditoria(id_men, tipo_mensaje, id_TR):
    """
        Genera informacion de auditoria como timespam y partes del mensaje
    """
    informacion = {'Id TR' : id_TR}
    informacion['Timestamp'] = time.time()
    informacion['Id Mensaje'] = id_men
    informacion['Id Parte'] = 1
    informacion['Cantidad Partes'] = 1
    informacion['Tipo Mensaje'] = tipo_mensaje
    return informacion

def enviarMensaje(id_mensaje, id_TR):
    """
        Genera informacion al azar para enviar
    """
    temperatura = random.random()
    humedad = random.randint(0, 100)
    presion = random.randint(0, 100)
    datos = {'Temperatura' : temperatura, 'Humedad' : humedad, 'Presion' : presion}
    return guardar_mensaje(datos, id_mensaje, id_TR)


def recolectarDatos(veces, tiempo, id_TR):
    """
        Funcion que se encarga de enviar informacion de una TR
        cada cierto tiempo y cierta cantidad de veces

    """
    
    time.sleep(5.0)
    #defino el puerto donde escucha el enviador de esta TR
    puertoEnviador = 6000 + id_TR

    #me conecto al enviador para pasarle los mensajes que recolecto de los sensores.
    proxy = xmlrpclib.ServerProxy("http://%s:%s/"%(hostEnviador,puertoEnviador))
    
    id_mensaje = 101
    for i in range(veces):
        res = enviarMensaje(id_mensaje, id_TR)
        proxy.publicar(res)
        time.sleep(tiempo)
        id_mensaje = id_mensaje + 1