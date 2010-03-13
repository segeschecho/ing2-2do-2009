from carta import Carta
from palo import Palo
from mazo import Mazo
from partida import Partida

palos = [Palo(12,"Copa"),Palo(12,"Basto"),Palo(12,"Oro"),Palo(12, "Espada")]
mazo = Mazo(palos)

print mazo

for i in range(5):
    cartaElegida = mazo.tomarUna()
    print "\n \n La carta elegida fue: ", cartaElegida
    mazo.mezclar()
    #print mazo
    
    
    
class Juego():

    def __init__(self, nombre_jugador):
        self.jugador = nombre_jugador
        self.puntajePropio = 0
        self.puntajeJugador = 0
        self.turno = 0
          
    def jugar(self):
        while puntajePropio < 15 and puntajeJugador < 15:
            mazo = Mazo(palos) 
            mazo.mezclar()
            partida = Partida(mazo, self.turno)
            partida.jugar()
            self.turno = not self.turno
            puntajePropio += partida.puntajePropio()
            puntajeJugador += partida.puntajeJugador()
            print "Gonzalo: ",self.puntajePropio
            print self.jugador + self.puntajeJugador
        if puntajePropio > puntajeJugador:
            print "GANE YO !!!!!"
        else:
            print "Gano %s. Felicitaciones!!!" %self.jugador
            
            
            
def main():
    
    print "/---------------------------------------/"
    print "/               TRUCO                   /"
    print "/                by                     /"
    print "/              Gonzalo                  /"
    print "/              Castillo                 /"
    print "/---------------------------------------/"
    print "\n \n"
    
    salir = 0
    
    while not salir:
        print "Desea comenzar a juegar? "
        respuesta = raw_input("(S/N)")
        while((not(respuesta == 'S') and not(respuesta == 'N') and not(respuesta == 's') and not(respuesta == 'n'))):
            respuesta = raw_input("Por favor responda correctamente(S/N)")
        if respuesta == 'N'or respuesta == 'n' :
            salir = 1
        else:
            nombre_jugador = raw_input("Por favor ingrese su nombre: ")
            print nombre_jugador
        #nuevo = Juego(nombre_jugador)
        #nuevo.jugar()
    
    
main()