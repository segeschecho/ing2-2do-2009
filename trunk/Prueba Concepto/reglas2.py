def prom_variable(variable):
    # Calculo promedio de una variable
    acumProm = 0
    cantTr = 0
    for medicion in datos
        mediciones = medicion[variable] 
        acumTempTr = 0
        for dato in mediciones
            acumTr += dato
        promTr = acumTr / len(mediciones)
        acumProm+=promTr
        cantTr++
    promTot = acumProm / cantTr

    
promTemp = prom_variable("Temperatura")
print "La temperatura promedio es ", promTemp, "/n"
promHumedad = prom_variable("Humedad")
print "La humedad promedio es ", promHumedad, "/n"
promPresion = prom_variable("Presion")
print "La presion promedio es ", promPresion, "/n"
promViento = prom_variable("Viento")
print "La velocidad promedio del viento es ", promViento, "/n"

#Reglas
if (promTemp > 33 and promHumedad < 60): print 'Debido a la alta temperatura y baja humedad hay probabilidades de incendios forestales'
if (promTemp < -2 and promHumedad > 98): print 'Se preveen fuertes nevadas con posibles avalanchas'
if (promTemp > 33 and promHumedad > 98 and promPresion > 1000): print 'Se preveen lluvias fuertes y posbiles innundaciones'
if (promTemp > 33 and promHumedad > 98 and promPresion > 1000 and promViento > 20): print 'Se preveen tsunamis en las ciudades costeras'
if (promPresion > 1020 and promViento > 40) print 'Altas probabilidades de tornados y huracanes'


