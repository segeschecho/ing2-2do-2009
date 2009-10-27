import sys 

reglas = sys.argv[1]
T =  int(sys.argv[2]) 
V =  int(sys.argv[3]) 
P =  int(sys.argv[4]) 
H =  int(sys.argv[5]) 


#if values.len() < 4:
#    print 'No se encuentran los valores apropiados'

archivo = open(reglas)
arrReglas = []

#for linea in archivo.readlines():
#    exec linea

exec archivo.read()
    