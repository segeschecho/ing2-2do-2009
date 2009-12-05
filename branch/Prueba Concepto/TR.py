import sys
import time
from multiprocessing import Process
from sincronizador import recolectarDatos #def recolectarDatos(veces, tiempo, id_TR):
from comunicacionEc import enviadorTR #def enviadorTR(id_tr):

#TR.py simula una tr, con una parte que se encarga de simular el sensado de los datos de los sensores
#y otra parte que se encarga del envio de los datos hacia la EC


if __name__ == '__main__':
    #parte que genera una TR y hace que envie informacion.
    #obtengo los parametros que me pasan para que todo ande bien
    if len(sys.argv) < 5:
        print "faltan parametros..."
        print "1 - Intervalo de tiempo para el envio (usual 60)"
        print "2 - Cantidad de mensajes que enviara la TR"
        print "3 - ID de la TR"
        print "4 - Tiempo de vida de la TR"
        sys.exit(1)
            
    tiempo = int(sys.argv[1])
    veces = int(sys.argv[2])
    id_tr = int(sys.argv[3])
    vida = int(sys.argv[4])
   
    #genero un proceso que representa al  recolectorTR
    #enviador = Process(target = recolectarDatos, args = (veces, tiempo, i+1))
    recolector = Process(target = recolectarDatos, args = (veces, tiempo, id_tr))
        
    #genero un proceso que representa al enviador de la tr
    enviador = Process(target = enviadorTR, args = (id_tr,))
    
    #corro los 2 procesos
    enviador.start()
    #time.sleep(3.0)
    recolector.start()
    
    
    #espero hasta que me digan que apague la TR
    #x = raw_input("los procesos estan corriendo, presione una tecla para terminar \n")
    time.sleep(vida)
    recolector.terminate()
    enviador.terminate()
    print "la TR se apago"
