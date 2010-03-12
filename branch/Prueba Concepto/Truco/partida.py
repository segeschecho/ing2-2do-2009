



class Partida():
    
    def __init__(self, mazo, turno):
        
        self.mazo = mazo
        self.puntosPropios = 0
        self.PuntosJugador = 0
        self.turno = turno
    
    
    def jugar():
       pass
      # if turno:
            
            
    def sumarEnvido(carta1, carta2, carta3):
        
        return max(sumar(carta1, carta2), sumar(carta1, carta3), sumar(carta2, carta3))
        
    def sumar(carta1, carta2):
            if carta1.palo == carta2.palo:
                return 20 + carta1.valorEnvido() + carta2.valorEnvido()
            else
                return max(carta1.valorEnvido(), carta2.valorEnvido())
    
    