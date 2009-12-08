import time
import xmlrpclib

host = 'localhost'
puertoGeneral = 6000

#simula procesamiento
def procesar(idEc):
    print 'Se levanta el procesador de la EC: ', idEc
    
    puerto = puertoGeneral + int(idEc)
    serverIntercambio = xmlrpclib.ServerProxy("http://%s:%s/"%(host,puerto))
    
    #Simulo un calculo de promedio de los pares de 1 a 100
    
    time.sleep(3)
    for i in xrange(1,6):
        
        datos = [x for x in xrange (1,101) if x % 2 == 0]
        resParcial = ['PARCIAL',sum(datos),i]
        serverIntercambio.publicar(resParcial)
        resTotal = ['TOTAL',sum(datos)/len(datos),i]
        serverIntercambio.publicar(resTotal) 
        time.sleep(3)     
    
    return 0