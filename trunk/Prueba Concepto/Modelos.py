import sys 
import random
import json
# T  : Temperatura
# P : Presion
# H : Humedad
# V : Velocidad Vientos


reglas = sys.argv[1]

if len(sys.argv) < 3:
    #Asignacion De Datos
    datos = {} #Armara en un protocolo comun lo datos para llas reglas
    for i in range(1,10):
        datos[i] = {}
        datos[i]['T'] = []
        datos[i]['P'] = []
        datos[i]['V'] = []
        datos[i]['H'] = []

    for i in range(1,10):
        for j in range (1,5):
            datos[i]['T'].append(random.randint(-2,50))
            datos[i]['P'].append(random.randint(950,1050))
            datos[i]['V'].append(random.randint(30,300))
            datos[i]['H'].append(random.randint(0,100))
else:
    data = sys.argv[2]
    archData = open(data)
    datos = eval(archData.read()) 
       
print datos
archivo = open(reglas)
#arrReglas = []

#for linea in archivo.readlines():
#    exec linea

exec archivo.read()
    