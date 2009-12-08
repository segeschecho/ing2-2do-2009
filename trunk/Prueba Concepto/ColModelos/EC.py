import sys
import time
import json
from multiprocessing import Process
from IntercambioResultados import inicializar
from Publicador import inicializarPublicador
from Procesamiento import procesar

    
if __name__ == '__main__':
    #parte que genera una EC y hace que envie los resultados de los modelos.
    #obtengo los parametros que me pasan para que todo ande bien
    if len(sys.argv) < 3:
        print "faltan parametros..."
        print "1 - Id Ec"
        print "2 - Dicc de Ec y tipo de resultado(parcial o total)"
        sys.exit(1)
            
    idEc = int(sys.argv[1])
    diccSuscEcs = json.loads(sys.argv[2])
  
    #genero un proceso que representa el Publish Suscribe
    publicador = Process(target = inicializarPublicador, args = (idEc, "EC", "EC"))
    
    #genero un proceso que representa el IntercambioResultados
    intercambioResultados = Process(target = inicializar, args = (idEc, diccSuscEcs))
        
    #genero un proceso que simula procesamiento
    procesador = Process(target = procesar, args = (idEc,))
    
    #corro los 2 procesos
    publicador.start()
    intercambioResultados.start()
    procesador.start()