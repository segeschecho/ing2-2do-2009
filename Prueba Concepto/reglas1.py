def max_variable(variable):
    # Calculo max de una variable
    acummax = -50
    for medicion in datos
        mediciones = medicion[variable] 
        medMax = max(mediciones)
        if (medMax > acummax) acummax = medMax
    

    
maxTemp = max_variable("Temperatura")
print "La temperatura maxedio es ", maxTemp, "/n"
maxHumedad = max_variable("Humedad")
print "La humedad maxedio es ", maxHumedad, "/n"
maxPresion = max_variable("Presion")
print "La presion maxedio es ", maxPresion, "/n"
maxViento = max_variable("Viento")
print "La velocidad maxedio del viento es ", maxViento, "/n"

#Reglas
if (maxTemp > 33 and maxHumedad < 60): print 'Debido a la alta temperatura y baja humedad hay probabilidades de incendios forestales'
if (maxTemp < -2 and maxHumedad > 98): print 'Se preveen fuertes nevadas con posibles avalanchas'
if (maxTemp > 33 and maxHumedad > 98 and maxPresion > 1000): print 'Se preveen lluvias fuertes y posbiles innundaciones'
if (maxTemp > 33 and maxHumedad > 98 and maxPresion > 1000 and maxViento > 20): print 'Se preveen tsunamis en las ciudades costeras'
if (maxPresion > 1020 and maxViento > 35) print 'Altas probabilidades de tornados y huracanes'


