import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

#canal donde se escuchan los mensajes que envian las trs

def enviarAEC(datos):
    print "se recibieron: ", datos
    return 0

host = "localhost"
puerto = 5555

server = SimpleXMLRPCServer((host, puerto))
print "Escuchando en el puerto...", puerto
server.register_function(enviarAEC, "enviarAEC")
server.serve_forever()


