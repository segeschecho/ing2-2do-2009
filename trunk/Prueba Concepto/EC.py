import sys
import time
import json
from multiprocessing import Process
from sincronizador import recolectarDatos #def recolectarDatos(veces, tiempo, id_TR):
from RecepcionSegura import inicializar
from comunicacionEc import enviadorTR #def enviadorTR(id_tr):
from Publicador import inicializarPublicador

#TR.py simula una tr, con una parte que se encarga de simular el sensado de los datos de los sensores
#y otra parte que se encarga del envio de los datos hacia la EC


if __name__ == '__main__':
    #parte que genera una TR y hace que envie informacion.
    #obtengo los parametros que me pasan para que todo ande bien
    if len(sys.argv) < 4:
        print "faltan parametros..."
        print "1 - Tiempo para detectar caida"
        print "2 - Id ec"
        print "3 - Dicc de idTR a array de sensores"
        sys.exit(1)
            
    tiempo = int(sys.argv[1])
    id_ec = int(sys.argv[2])
    dicc = json.loads(sys.argv[3])
   
    #genero un proceso que representa el recepcionSegura
    publicador = Process(target = inicializarPublicador, args = (id_ec, "EC", "EC"))
    
    #genero un proceso que representa al  recolectorTR
    #enviador = Process(target = recolectarDatos, args = (veces, tiempo, i+1))
    recepcion_segura = Process(target = inicializar, args = (tiempo, id_ec, dicc))
        
    #corro los 3 procesos
    publicador.start()
    recepcion_segura.start()
