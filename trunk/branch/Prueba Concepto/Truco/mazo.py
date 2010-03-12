from carta import Carta
from palo import *
from random import random, sample



class Mazo():
    
    def __init__(self, palos): # A un mazo se le pasa una coleccion de palos y su cantidad para generar cartas.
        
        self.cartas = []
        for eachPalo in palos:
            for eachCarta in range(eachPalo.cantidad):
                self.cartas.append(Carta(eachCarta + 1, eachPalo.descripcion))
        
            
    def __str__(self): # Muestra un mazo.
        
        res = ""
        for eachCarta in self.cartas:
            res = res + str(eachCarta) + "\n"
        return res
        
    def mezclar(self): # Mezcla un mazo.
        mezcla = sample(self.cartas, len(self.cartas))
        self.cartas = mezcla
            
    def tomarUna(self): # Toma la carta superior del mazo y la devuleve.
        return (self.cartas).pop()
               
    def vacio(self):
        return len(self.cartas) == 0