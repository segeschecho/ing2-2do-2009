def max_variable(variable):
    # Calculo max de una variable
    acummax = -50
    for medicion in datos.values():
        mediciones = medicion[variable] 
        medMax = max(mediciones)
        if (medMax > acummax): 
            acummax = medMax
    return acummax

    
maxTemp = max_variable('T')
print "La temperatura maxima es ", maxTemp
maxHumedad = max_variable('H')
print "La humedad maxima es ", maxHumedad
maxPresion = max_variable('P')
print "La presion maxima es ", maxPresion
maxViento = max_variable('V')
print "La velocidad maxima del viento es ", maxViento

#Reglas
#Reglas
if (maxTemp > 25 and maxHumedad < 40): print 'Debido a la alta temperatura y baja humedad hay probabilidades de incendios forestales'
if (maxTemp < -2 and maxHumedad > 90): print 'Se preveen fuertes nevadas con posibles avalanchas'
if (maxTemp > 25 and maxHumedad > 98 and maxPresion < 1000): print 'Se preveen lluvias fuertes y posibiles innundaciones'
if (maxTemp > 28 and maxHumedad > 98 and maxPresion < 1000 and maxViento > 20): print 'Se preveen tsunamis en las ciudades costeras'
if (maxPresion > 1020 and maxViento > 40): print 'Altas probabilidades de tornados y huracanes'
if (maxViento > 100 and maxPresion > 960): print 'Se preveen vientos muy fuertes'
if (maxTemp > 10 and maxTemp <= 25 and maxViento < 40 and maxHumedad < 90): print 'Tiempo despejado, condiciones normales'
if (maxTemp > 6 and maxTemp < 24 and maxHumedad > 90): print 'Se pronostica niebla, y visibilidad cuasi nula en rutas y caminos'
if (maxTemp >= 6 and maxTemp <= 24 and maxHumedad <= 60): print 'No se preveen grandes variaciones de presion y temperatura en los proximos minutos.'


