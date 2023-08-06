import time
import random
import os
from colorama import Fore

cls = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")

def wrd():
  cls()
  palabra_del_dia = [
'abeto', 'altar', 'agudo', 'bache', 'bajar', 'beben', 'catar', 'camas',
'cosas', 'dedos', 'dejar', 'domar', 'error', 'ellos', 'enojo', 'fallo',
'feria', 'finca', 'gafas', 'galas', 'giras', 'halos', 'hasta', 'hielo',
'ideas', 'india', 'julio', 'jefas', 'lento', 'logro', 'lente', 'marco',
'morro', 'menos', 'negro', 'narco', 'orcos', 'preso', 'prosa', 'pinto',
'queso', 'rosas', 'retar', 'solos', 'salon', 'sabio', 'tonto', 'tomar',
'tabla', 'vagos', 'vacas', 'valor', 'yemas', 'yates', 'zurda', 'zorro'
  ]

  colors = {
'green': '\033[92m',
'yellow': '\033[93m',
'red': '\033[91m',
'ENDC': '\033[0m'
  }


  def color_letter(letter, color):
    return colors[color] + letter + colors['ENDC']


# init game
  print("Bienvenid@ al juego del Wordle!")
  time.sleep(1.5)
  eval = input('Sabes como funciona el juego: ')
  choice = eval.lower()
  time.sleep(1)
  win = False
  word = random.choice(palabra_del_dia)

  while choice == 'no':
    time.sleep(1)
    cls()
    print(
    "Basicamente, tienes que adivinar una palabra random en menos de 5 intentos\n"
    )
    time.sleep(2)
    print(
      Fore.GREEN +
      "Cuando las letras de la palabra que escribas coincidan con las de la palabra random, estas se pintarán de verde.\n"
    )
    time.sleep(2)
    print(
      Fore.YELLOW +
      "Si no están en la posición que debería pero si pertenecen a la palabra, estas se teñiran de amarillo\nTen cuidado, que la dificultad aumenta, porque si una letra sale amarilla y coincide con una verde, puede que esa letra amarilla se refiera a esa verde\n"
    )
    time.sleep(4)
    print(Fore.RED +
        "Y, por último, las letras rojas no pertenecen a la palabra random.\n")
    time.sleep(1.5)
    print(Fore.RESET + "Una vez adivinada, ganarás. ¿Ha quedado claro?")
    choice = input('Respuesta: ')
    choice = choice.lower()
    cls()
    if choice == 'si':
      print("Entonces, empecemos :D.\nEscriba una palabra para empezar: \n")
  else:
    print("\nEn ese caso, empecemos :D\n")
    time.sleep(1)
    print("Escribe una palabra para empezar: ")
  board = []
  for i in range(6):
    board.append(['_' for l in range(5)])  #lista in.r se guarda
  contador = 0
  while (not win) and (contador < len(word)):
    text = input("")
    while len(text) != len(word):
      print(Fore.RED + f"\n¡La palabra debe tener {len(word)} caracteres!\n")
      text = input("")
  # ganar
    if word == text:
      board[contador] = [l for l in text]
      cls()
      print("\nFelicidades has ganado!")
      win = True

  # letter in word
    else:
      test_line = []
      for j in range(len(text)):
        if text[j] == word[j]:  # la letra está
          test_line.append(color_letter(text[j], 'green'))
          cls()

        elif text[j] in word:  # la letra en otro sitio
          test_line.append(color_letter(text[j], 'yellow'))
          cls()
        else:  # la letra no está
          test_line.append(color_letter(text[j], 'red'))
          cls()
      board[contador] = test_line

  #draw
    for i in range(5):
      print(
      " ".join(board[i])
      )  #cada elemento de mi lista board lo transforme en un string que esté separado por un espacio

    contador += 1

  if win:
    print(Fore.GREEN+"\nFelicidades lo has conseguido!!")
    time.sleep(1)
    print(Fore.RESET)
  else:
    print(Fore.RED+f"\nVaya, la palabra era {word}. La próxima vez tendrás más suerte¡¡")
    time.sleep(1)
    print(Fore.RESET)


