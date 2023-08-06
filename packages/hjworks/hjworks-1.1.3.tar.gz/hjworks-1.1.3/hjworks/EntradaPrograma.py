import time
import os
import colorama
from colorama import Fore

cls=lambda:os.system("cls" if os.name in ("nt","dos") else "clear")
def registro():
    cls()
    Users=[]
    Pss=[]
    rg=Users.append(input("Dime tu nombre: "))
    rg1=Pss.append(input("Dime tu contraseña: "))
    time.sleep(0.5)
    print("Registro Completo :D ")
    time.sleep(0.5)
    User=Users.copy()
    Pssw=Pss.copy()
    cls()