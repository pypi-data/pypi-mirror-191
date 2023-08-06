import random
import time
from colorama import Fore
import os

cls= lambda:os.system("cls" if os.name in("nt","dos")else "clear")

def ppt():
    objeto = (['Piedra', 'Papel', 'Tijeras'])
    solucion = random.choice(objeto)
 
    print("Bienvenid@ al juego de piedra, papel o tijeras.")
    time.sleep(2)
    choice = input("¿Estás list@ para desafiar a la IA?: ")
 
    while choice == 'si' or choice == 's' or choice == 'Si':
        print("\nPerfecto.")
        time.sleep(1.5)
        cls()
        time.sleep(0.5)
        print("""Elija uno de los tres objetos (escribe la primera letra mayúscula):\n""")
        time.sleep(1)
        print("--> Piedra")
        time.sleep(0.5)
        print("--> Papel")
        time.sleep(0.5)
        print("--> Tijeras")
        time.sleep(2) #deja este así
        cls()
        obj = input("\nEscoja: ")
        while obj == solucion:
            time.sleep(1.5)
            print(f"\nTú oponente ha sacado {solucion} y tú has sacado {obj}")
            time.sleep(1)
            print(Fore.YELLOW + "\nVaya, ha habido un empate.")
            print(Fore.RESET + "")
            break


        while obj == 'Tijeras' and solucion == 'Piedra' or obj == 'Papel' and solucion == 'Tijeras' or obj == 'Piedra' and solucion == 'Papel':
            time.sleep(2)
            print(f"\nTú oponente ha sacado {solucion} y tú {obj}")
            time.sleep(1)
            print(Fore.RED + "\nVaya, me temo que has perdido.")
            print(Fore.RESET + "")
            time.sleep(1)
            break

        while obj == 'Piedra' and solucion == 'Tijeras' or obj == 'Tijeras' and solucion == 'Papel' or obj == 'Papel' and solucion == 'Piedra':
            time.sleep(2)
            print(f"\nTú oponente ha sacado {solucion} y tú {obj}")
            time.sleep(1)
            print(Fore.GREEN + "\nHas ganado!!")
            print(Fore.RESET + "")
            time.sleep(1)
            break
    
        choice = input("¿Desea continuar?: ")
        if choice == 'no' or choice == 'No':
            time.sleep(1)
            print(Fore.BLUE + "\nHasta pronto!!")
            print(Fore.RESET + "")
            break