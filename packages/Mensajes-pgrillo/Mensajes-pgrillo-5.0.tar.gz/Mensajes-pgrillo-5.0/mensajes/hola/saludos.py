import numpy as np

def saludar():
    print("Hola, te estoy saludando desde la funcion saludar del módulo saludos")

def prueba():
    print("Esto de una prueba de la nueva versión")

def generar_array(numeros):
    return np.arange(numeros)

class Saludo():
    def __init__(self):
        print("Hola, te estyo saludando desde el init de la clase Saludo")



if __name__ == '__main__':
    print(generar_array(5))