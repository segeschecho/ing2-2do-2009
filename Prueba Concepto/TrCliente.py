import socket
#ejemplo de tr enviando cosas


host = "localhost"
puerto = 5555

conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conexion.connect((host, puerto))
conexion.send("Gonza puto )

conexion.close()
print "sali"