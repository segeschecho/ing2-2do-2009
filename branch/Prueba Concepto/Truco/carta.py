from errores import idMayorACero

class Carta():

    def __init__(self, id, palo): # Una carta tiene un valor y un palo(string no la clase palo).
        
        try:
            if id < 0:
                raise idMayorACero()
        except idMayorACero, e:
            print e
            return 
        self.id = id
        self.palo = palo    
    
    def __eq__(self, carta): # Igualdad de cartas.
        
        return (self.id == carta.id) & (self.palo == carta.palo)
        
    
    def __str__(self): # Muestra una carta.
        
        return "#-" + str(self.id) + "-# \n"  + "#-" + self.palo + "-#"
        
        
    def valorEnvido():
        if self.id < 10:
            return self.id
        else:
            return 0
            
    def valorTruco():
        if carta.id == 1:
            if carta.palo == "ESPADA":
                return 1
            else
                if carta.palo == "BASTO":
                    return 2
                else:
                    return 7
        else:
            if carta.id == 7:
                if carta.palo == "ESPADA":
                    return 3
                else:
                    if carta.palo == "ORO":
                        return 4
                    else:
                        return 13
            else:
                if carta.id == 3:
                    return 5
                else:
                    if carta.id == 2:
                        return 6
                    else:
                        return 20 - carta.id
                