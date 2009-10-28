class Partidor:
"""
	informacion = {'Id TR' : id_TR}
    informacion['Timestamp'] = time.time()
    informacion['Id Mensaje'] = id_men
    informacion['Id Parte'] = 1
    informacion['Cantidad Partes'] = 1
    informacion['Tipo Mensaje'] = tipo_mensaje
    informacion['Contenido'] = {'Humedad' : caca}
    return informacion
"""
    def partir(self, transmision):
        cantPartes = len(transmision['Contenido'].keys())
		transmision_nueva = {}
        for i in range(cantPartes):
            claves = transmision['Contenido'].keys()
            transmision_nueva['Parte'+ str(i+1)] = {}
            transmision_nueva['Parte'+ str(i+1)]['Id TR'] = transmision['Id TR']
            transmision_nueva['Parte'+ str(i+1)]['Timestamp'] = transmision['Timestamp']
            transmision_nueva['Parte'+ str(i+1)]['Id Mensaje'] = transmision['Id Mensaje']
            transmision_nueva['Parte'+ str(i+1)]['Id Parte'] = i+1
            transmision_nueva['Parte'+ str(i+1)]['Cantidad Partes'] = cantPartes
            transmision_nueva['Parte'+ str(i+1)]['Tipo Mensaje'] = transmision['Tipo Mensaje']
            transmision_nueva['Parte'+ str(i+1)]['Contenido'] = transmision['Contenido'][claves[i]]
       
       return transmision_nueva
	
	