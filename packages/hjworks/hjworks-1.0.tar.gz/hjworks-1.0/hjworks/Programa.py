import time
import os
import webbrowser
from .TresEnRaya import ter
from .PiedraPapelTijeras import ppt
from .Wordle import wrd

cls=lambda:os.system("cls" if os.name in ("nt","dos") else "clear")

def programaa():
    contador=1
    while contador==1:
        cls()
        print(f"Hola, ¿qué deseas hacer hoy? \n")
        print("-Buscar Definiciones (introduce buscar) ")
        print("-Jugar a juegos (introduce jugar) \n")
        pg=input("Hoy quiero ")
        while pg=="buscar":
            cls()
            x=input("Dime la palabra que deseas buscar: ")
            webbrowser.open(f"https://dle.rae.es/{x}")
            sal=input("¿Deseas buscar más palabras? ")
            if (sal=="No") or (sal=="no"):
                break
        if pg=="jugar":
            cls()
            print("Vale, tenemos estos juegos disponibles de momento: \n")
            print("Juego 1-Tres en raya (necesitas dos jugadores)(introduce 1) ")
            print("Juego 2-Piedra,papel o tijera (Juegas contra la IA)(introduce 2) ")
            print("Juego 3-Wordle (introduce 3) \n")
            ch=int(input("Elige el juego al que deses jugar: "))
            if ch==1:
                cls()
                ter()
            if ch==2:
                cls()
                ppt()
            if ch==3:
                cls()
                wrd()
