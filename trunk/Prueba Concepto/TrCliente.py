import xmlrpclib
import time

#ejemplo de tr enviando cosas

host = "localhost"
puerto = 5555

proxy = xmlrpclib.ServerProxy("http://%s:%s/"%(host,puerto))

proxy.enviarAEc("gonza trolo, que no la ve ni en fotos")
time.sleep(5)
proxy.enviarAEc("gonza trolo, que no la ve ni en fotos")
time.sleep(5)
proxy.enviarAEc("gonza trolo, que no la ve ni en fotos")
time.sleep(5)
proxy.enviarAEc("gonza trolo, que no la ve ni en fotos")
    
print "sali"