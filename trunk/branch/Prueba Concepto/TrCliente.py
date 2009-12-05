import xmlrpclib
import time

#ejemplo de tr enviando cosas

host = "localhost"
puerto = 6001

proxy = xmlrpclib.ServerProxy("http://%s:%s/"%(host,puerto))

proxy.enviarAEC(3)
time.sleep(5)
proxy.enviarAEC(3)
time.sleep(5)
proxy.enviarAEC(3)
time.sleep(5)
proxy.enviarAEC(3)
    
print "sali"