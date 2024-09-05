# Proyecto de Autómatas Finitos Deterministas (AFD)

Este proyecto implementa un conjunto de herramientas en Python diseñadas para simular, analizar y optimizar Autómatas Finitos Deterministas (AFD). Las herramientas permiten verificar si una cadena de texto es aceptada por el AFD, manejar transiciones que no consumen entrada (transiciones epsilon) y reducir el número de estados del autómata para hacerlo más eficiente sin cambiar el lenguaje que acepta.

## Estructura del Proyecto

El proyecto consta de varios scripts organizados de la siguiente manera:

- **main.py**: Este es el punto de entrada del proyecto, donde las funciones de los otros módulos son utilizadas para ejecutar pruebas sobre los AFDs definidos.
- **defs.py**: Define una serie de funciones y constantes utilizadas a lo largo del proyecto. Esto incluye definiciones de estados, transiciones y funciones de ayuda para manejar las operaciones del autómata.
- **classes.py**: Contiene las definiciones de clases necesarias para construir y operar los AFDs. Esto incluye la clase Autómata, Estado, y cualquier otra estructura de datos necesaria.

## Características Principales

### Ejecución de AFD
Permite cargar o definir un autómata finito determinista y evaluar cadenas para determinar si son aceptadas por el autómata según las reglas de transición definidas.

### Reducción de AFD
Implementa algoritmos de minimización de estados para optimizar el AFD, lo cual es útil para reducir la complejidad del autómata sin alterar el lenguaje que es capaz de reconocer.

### Transiciones Epsilon
Maneja eficazmente las transiciones epsilon, permitiendo que el autómata cambie de estado sin necesidad de consumir símbolos de la cadena de entrada, facilitando así la simulación de autómatas más complejos.

## Operadores y Caracteres Especiales

- **Parentesis** `(`, `)`: Utilizados para agrupar expresiones y controlar el orden de operación.
- **Operador OR** `|`: Se emplea para indicar alternancia, permitiendo que la expresión coincida con cualquiera de los patrones separados por este operador.
- **Concatenación** `.`: Implica una concatenación explícita entre expresiones.
- **Cerradura de Kleene** `*`: El carácter o grupo precedente puede aparecer cero o más veces.

## Instalación

Para poner en marcha el proyecto, siga los siguientes pasos:

1. Clone el repositorio en su máquina local usando Git: https://github.com/mar22266/RegexToAFDConverter.git

2. Navegue hasta el directorio del proyecto:
   cd RegexToAFDConveter

3. Instale las dependencias necesarias utilizando pip:
   pip install colorama graphviz

4. Ejecute el script principal para comenzar las pruebas o simulaciones:
   python main.py

## Uso

Para utilizar las herramientas del proyecto, simplemente ejecute el script `main.py` desde su terminal. Este script está configurado para demostrar las capacidades del proyecto y proporcionar una salida visual de los resultados mediante la consola.

## Dependencias

Este proyecto depende de las siguientes bibliotecas Python:
- `colorama`: Esta biblioteca es utilizada para añadir color y estilo a la salida de texto en la consola, lo cual mejora significativamente la legibilidad de los resultados.
- `graphviz`: Utilizada para generar visualizaciones gráficas de los autómatas, facilitando la comprensión de su estructura y comportamiento.
