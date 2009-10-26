import socket
#canal donde se escuchan los mensajes que envian las trs

host = ""
puerto = 5555

escucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
escucha.bind((host,puerto))

escucha.listen(1)

cliente, direccion = escucha.accept()

print "se conectaron desde",direccion

datos = cliente.recv(1024)
cliente.close

print "se recibio del cliente: ", datos