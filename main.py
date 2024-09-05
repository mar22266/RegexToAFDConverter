"""
Proyecto 1 de Teoría de la Computación
Desarrollado por:
- Andre Marroquin
- Sofia Mishell
- Nicolle Gordillo
"""

# Importar las funciones y clases necesarias
from defs import *
from classes import *
from pprint import pprint
from colorama import Fore, Style
import time

# Función para la animación de puntos suspensivos
def print_with_dots(message, duration=5):
    print(Fore.BLUE + message, end="")
    for _ in range(duration):
        for _ in range(3):
            print(Fore.BLUE + '.', end='', flush=True)
            time.sleep(0.3)
        print(Fore.BLUE + '\b\b\b   \b\b\b', end='', flush=True)  
    print(Style.RESET_ALL)
    
def main():
    # Leer las expresiones regulares desde el archivo
    data = leer_regex()

    for i in range(len(data)):
        print(Fore.CYAN + '---------------------------------------------------------  PROCESO INICIADO  -----------------------------------------------------------' + Style.RESET_ALL)
        print(Fore.YELLOW + f'Trabajando con la expresión regular: {data[i]}\n' + Style.RESET_ALL)

        # Paso 1: Conversión de infix a postfix
        postfix = infijo_a_postfijo(data[i])
        print(Fore.YELLOW + f'Conversión de infix a postfix: {postfix}' + Style.RESET_ALL + '\n')
        
        # Pasos 2, 3 y 4: Construcción del AFN, AFD y AFD simplificado desde la expresión postfix
        print_with_dots(Fore.BLUE + 'Construcción del AFN, AFD y AFD simplificado en progreso')
        afn = construir_afn(postfix)
        dibujar_afn(afn, i)
        afd = calcular_subconjuntos(afn)
        dibujar_afd(afd, i)
        afd_simplificado = reducir_afd(afd)
        dibujar_afd(afd_simplificado, i, simplificado=True)
        print(Fore.BLUE + 'Construcción completada!\n' + Style.RESET_ALL)

        # Solicitar la cadena a probar con los autómatas
        print(Fore.MAGENTA + "Ingrese la cadena que desea verificar si es aceptada:" + Style.RESET_ALL)  
        cadena = input()

        # Paso 5: Simulación del AFN con la cadena ingresada
        print(Fore.MAGENTA + 'Simulación del AFN' + Style.RESET_ALL)
        print(simular_afn(afn, cadena), '\n')

        # Paso 6: Simulación del AFD con la cadena ingresada
        print(Fore.MAGENTA + 'Simulación del AFD' + Style.RESET_ALL)
        print(ejecutar_afd(afd, cadena), '\n')

        # Paso 7: Simulación del AFD simplificado con la cadena ingresada
        print(Fore.MAGENTA + 'Simulación del AFD simplificado' + Style.RESET_ALL)
        print(ejecutar_afd(afd_simplificado, cadena), '\n')
        print(Fore.CYAN + '---------------------------------------------------------  PROCESO FINALIZADO  ---------------------------------------------------------\n\n' + Style.RESET_ALL)

if __name__ == "__main__":
    main()
