def prom_variable(variable):
    # Calculo promedio de una variable
    acumProm = 0
    cantTr = 0
    for medicion in datos.values():
        mediciones = medicion[variable] 
        acumTr = 0
        for dato in mediciones:
            acumTr += dato
        promTr = acumTr / len(mediciones)
        acumProm+=promTr
        cantTr += 1
    promTot = acumProm / cantTr
    return promTot
    
promTemp = prom_variable('T')
print "La temperatura promedio es ", promTemp
promHumedad = prom_variable('H')
print "La humedad promedio es ", promHumedad
promPresion = prom_variable('P')
print "La presion promedio es ", promPresion
promViento = prom_variable('V')
print "La velocidad promedio del viento es ", promViento, "\n"

#Reglas
if (promTemp > 25 and promHumedad < 40): print 'Debido a la alta temperatura y baja humedad hay probabilidades de incendios forestales... \n'
if (promTemp < -2 and promHumedad > 90): print 'Se preveen fuertes nevadas con posibles avalanchas... \n'
if (promTemp > 25 and promHumedad > 98 and promPresion < 1000): print 'Se preveen lluvias fuertes y posibles innundaciones...\n'
if (promTemp > 28 and promHumedad > 98 and promPresion < 1000 and promViento > 20): print 'Se preveen tsunamis en las ciudades costeras...\n'
if (promPresion > 1020 and promViento > 40): print 'Altas probabilidades de tornados y huracanes...\n'
if (promViento > 100 and promPresion > 960): print 'Se preveen vientos muy fuertes...\n'
if (promTemp > 10 and promTemp <= 25 and promViento < 40 and promHumedad < 90): print 'Tiempo despejado, condiciones normales...\n'
if (promTemp > 6 and promTemp < 24 and promHumedad > 90): print 'Se pronostica niebla, y visibilidad cuasi nula en rutas y caminos...\n'
if (promTemp >= 6 and promTemp <= 24 and promHumedad <= 60): print 'No se preveen grandes variaciones de presion y temperatura en los proximos minutos...\n'

