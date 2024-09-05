"""File donde estan las funciones necesarias para el proyecto"""

# Importar librerías necesarias
from classes import *
import copy
import string
import copy
from colorama import Fore, Style

# Función para leer las expresiones regulares desde un archivo
def leer_regex():
    with open("./regex.txt", "r", encoding='utf-8') as archivo:
        return archivo.read().split("\n")

# Función para obtener la precedencia de un operador
def obtener_precedencia(caracter):
    precedencias = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5}
    return precedencias.get(caracter, 6)

# Función para transformar el operador opcional '?' en una expresión regular
def transformar_opcional(cadena):
    pila = []  # Utiliza una pila para construir la nueva expresión regular.
    i = 0
    while i < len(cadena):  # Itera sobre cada caracter de la cadena.
        caracter = cadena[i]
        if caracter == '?':  # Encuentra el operador opcional '?'.
            temp = ''
            if pila[-1] == ')':  # Maneja agrupaciones con paréntesis.
                temp = ')'
                pila.pop()
                contador = 1
                # Bucle para manejar paréntesis anidados correctamente.
                while contador > 0:
                    temp = pila.pop() + temp
                    if temp[0] == '(':
                        contador -= 1
                    if temp[0] == ')':
                        contador += 1
                temp = temp[1:]
            # Maneja caracteres simples fuera de cualquier paréntesis.
            elif pila[-1] not in '()*|':
                temp = pila.pop()
                while pila and pila[-1] not in '()*|':
                    temp = pila.pop() + temp
            temp = r'(ε|' + temp + ')'  # Crea la nueva representación con ε.
            pila.append(temp)
        else:
            pila.append(caracter)
        i += 1
    return ''.join(pila)

# Función para transformar una clase de caracteres en una expresión regular
def transformar_clase(regex):
    resultado = ''
    bandera = False  # Controla si estamos dentro de un set de caracteres.
    for i in range(len(regex)):
        char1 = regex[i]
        if i + 1 < len(regex):
            char2 = regex[i + 1]
            # Maneja la creación de alternancias dentro de los sets de caracteres.
            if bandera:
                if char2 == ']':  # Cierra la alternancia al encontrar ']'.
                    resultado += char1 + ')'
                    bandera = False
                else:  # Continúa la alternancia dentro del set.
                    resultado += char1 + '|'
            # Controla la apertura de un nuevo set de caracteres.
            if not bandera:
                if char1 == '[':
                    resultado += '('
                    bandera = True
                elif char1 != ']' and char2 != ']':
                    resultado += char1
    resultado += regex[-1]
    return resultado

# Transforma el operador '+' en una expresión regular a la equivalente cerradura de Kleene '*'.
def transformar_positiva_kleene(expresion):
    salida = ''
    pila_balance = []  # Maneja el balanceo de paréntesis.
    pila = []  # Almacena temporalmente caracteres para formar subexpresiones.
    kleene_positivo = False  # Indica si se está procesando un operador '+'.
    
    # Itera sobre la expresión en reversa para manejar operadores '+'.
    for i in reversed(range(len(expresion))):
        caracter = expresion[i]
        if caracter == '+':
            kleene_positivo = True  # Activa el modo de transformación para el operador '+'.
        elif kleene_positivo:
            # Agrega paréntesis a la pila para balancear y formar la subexpresión correcta.
            if caracter == ')':
                pila_balance.append(caracter)
            elif caracter == '(':
                if pila_balance:
                    pila_balance.pop()
            pila.append(caracter)
            # Finaliza la transformación cuando los paréntesis están balanceados.
            if not pila_balance:
                subcadena = '(' + ''.join(reversed(pila)) + ')*'
                salida = subcadena + salida
                pila = []
                kleene_positivo = False
        else:
            salida = caracter + salida  # Continúa agregando caracteres a la salida si no está en modo '+'.

    return salida


# Escapa backslashes antes de caracteres que no son metacaracteres para tratarlos como literales.
def escapar_caracteres(expresion):
    resultado = ''  # Inicializa la cadena de salida.
    # Itera sobre cada caracter, duplicando backslashes donde sea necesario.
    for i in range(len(expresion) - 1):
        char1 = expresion[i]
        if char1 == '\\' and expresion[i + 1] not in ['(', ')', '{', '}']:
            resultado += '\\' + char1  # Duplica el backslash.
        else:
            resultado += char1  # Agrega el caracter a la salida.
    resultado += expresion[-1]  # Añade el último caracter.
    return resultado


def considerar_punto(expresion):
    salida = ''  # Inicializa la cadena de salida que acumulará el resultado final.

    # Itera sobre la expresión regular hasta el penúltimo carácter para procesar cada caracter.
    for i in range(len(expresion) - 1):
        caracter = expresion[i]
        # Comprueba si el carácter actual es un punto.
        if caracter == '.':
            salida += '\\' + caracter  # Añade un backslash antes del punto para escaparlo.
        else:
            salida += caracter  # Añade el carácter directamente a la salida si no es un punto.
    salida += expresion[-1]  # Añade el último carácter de la expresión a la salida.

    return salida  # Devuelve la expresión regular con los puntos correctamente escapados.


# Esta función prepara una expresión regular añadiendo puntos de concatenación y realizando transformaciones necesarias.
def formatear_regex(expresion: str) -> str:
    todos_operadores = ['|', '?', '+', '*', '^']
    operadores_binarios = ['|', '^']
    resultado = ''
    
    # Aplica transformaciones secuenciales para manejar diferentes aspectos de la expresión regular.
    expresionX = transformar_clase(expresion)
    expresionX = transformar_opcional(expresionX)
    expresionX = transformar_positiva_kleene(expresionX)
    expresionX = escapar_caracteres(expresionX)
    expresionX = considerar_punto(expresionX)

    escapado = False
    # Añade puntos de concatenación explícitos para asegurar la correcta interpretación de la expresión.
    for i in range(len(expresionX) - 1):
        c1 = expresionX[i]
        c2 = expresionX[i + 1]
        resultado += c1
        if c1 == '\\':
            escapado = not escapado
        elif not escapado and c1 not in operadores_binarios and c2 not in todos_operadores and c2 != '(':
            resultado += '.'
    resultado += expresionX[-1]
    return resultado

# Convierte una expresión regular de notación infija a postfija usando el algoritmo de Shunting Yard.
def infijo_a_postfijo(expresion: str):
    regex_formateada = formatear_regex(expresion)  # Prepara la expresión para conversión.
    postfija = ''
    pila = Pila()  # Utiliza una pila para manejar los operadores y paréntesis.
    escapar_siguiente = False  # Indicador para manejar caracteres escapados.

    # Itera a través de la expresión formateada, procesando cada caracter.
    for caracter in regex_formateada:
        if escapar_siguiente:
            postfija += caracter
            escapar_siguiente = False
            continue

        if caracter == '\\':
            escapar_siguiente = True
        elif caracter == '(':
            pila.apilar(caracter)
        elif caracter == ')':
            while pila.ver_tope() != '(':
                postfija += pila.desapilar()
            pila.desapilar()
        else:
            # Mientras que la pila no esté vacía y la precedencia del operador en la pila sea mayor o igual al actual.
            while not pila.esta_vacia() and obtener_precedencia(pila.ver_tope()) >= obtener_precedencia(caracter):
                postfija += pila.desapilar()
            pila.apilar(caracter)

    # Vacía cualquier operador restante en la pila.
    while not pila.esta_vacia():
        postfija += pila.desapilar()

    return postfija


# Construye un árbol de análisis para una expresión regular dada en notación postfija.
def crear_arbol(expresion):
    pila = Pila()
    operadores = {'*': 1, '|': 2, '.': 2}  # Diccionario para identificar y manejar la aridad de los operadores.

    for i, char in enumerate(expresion):
        if char in operadores:
            nodo = Nodo(char, f'{i}')
            # Crear nodos en el árbol según el operador sea binario o unario.
            if operadores[char] == 2:  # Operadores binarios toman dos operandos.
                derecha = pila.desapilar()
                izquierda = pila.desapilar()
                nodo.derecha = derecha
                nodo.izquierda = izquierda
            elif operadores[char] == 1:  # Operador unario toma un operando.
                izquierda = pila.desapilar()
                nodo.izquierda = izquierda
            pila.apilar(nodo)
        else:
            pila.apilar(Nodo(char, f'{i}'))  # Crea un nodo para un carácter y lo pone en la pila.

    return pila.desapilar()  # Retorna el nodo raíz del árbol construido.


# Visualiza y muestra los árboles de las expresiones regulares proporcionadas.
def dibujar_arbol(expresiones):
    for expresion in expresiones:
        print(f"Árbol de la expresión regular: {expresion}")
        postfija = infijo_a_postfijo(expresion)  # Convierte la expresión a su forma postfija.
        print(f"Postfija: {postfija}")
        arbol = Arbol(crear_arbol(postfija), expresiones.index(expresion))
        arbol.graficar()  # Método para visualizar el árbol.


# Crea un autómata finito no determinista (AFND) para un único carácter.
def crear_caracter(c):
    inicio, aceptacion = 0, 1
    transiciones = {(inicio, c): [aceptacion]}  # Define transiciones para el carácter dado.
    return AFNoDeterminista(inicio, aceptacion, transiciones)  # Retorna un nuevo AFND.


# Realiza la operación de concatenación entre dos autómatas finitos no deterministas.
def operador_concatenacion(afn1, afn2):
    transiciones = afn1.transiciones.copy()  # Copia las transiciones del primer AFN.
    ajuste = afn1.aceptacion  # Utiliza el estado de aceptación del primer AFN como ajuste.

    # Ajusta y combina las transiciones del segundo AFN.
    for (estado, simbolo), siguientes_estados in afn2.transiciones.items():
        nuevo_estado = estado + ajuste if estado != afn2.inicio else ajuste
        nuevos_siguientes_estados = [s + ajuste for s in siguientes_estados]

        transiciones[(nuevo_estado, simbolo)] = nuevos_siguientes_estados

    return AFNoDeterminista(afn1.inicio, afn2.aceptacion + ajuste, transiciones)  # Retorna un nuevo AFND combinado.


# Aplica el operador Kleene '*' a un autómata, creando un nuevo autómata que acepta cualquier número de repeticiones del patrón original.
def operador_kleene(afnd):
    inicio, ajuste = 0, 1
    aceptacion = afnd.aceptacion + 2
    # Configura las transiciones para el nuevo autómata con el operador Kleene.
    transiciones = {(inicio, ''): [afnd.inicio + ajuste, aceptacion], (afnd.aceptacion + ajuste, ''): [afnd.inicio + ajuste, aceptacion]}
    
    # Ajusta las transiciones existentes del autómata original para incluir las nuevas en el autómata resultante.
    for (estado, simbolo), siguientes_estados in afnd.transiciones.items():
        nuevo_estado = estado + ajuste
        nuevos_siguientes_estados = [s + ajuste for s in siguientes_estados]
        transiciones[(nuevo_estado, simbolo)] = nuevos_siguientes_estados

    return AFNoDeterminista(inicio, aceptacion, transiciones)


# Construye un autómata que acepta lenguajes representados por dos autómatas usando el operador lógico OR ('|').
def operador_or(afn1, afn2):
    inicio = 0
    aceptacion = afn1.aceptacion + afn2.aceptacion + 3
    ajuste1 = 1
    ajuste2 = afn1.aceptacion + 2
    # Configura las transiciones iniciales y finales para el nuevo autómata.
    transiciones = {
        (inicio, ''): [afn1.inicio + ajuste1, afn2.inicio + ajuste2],
        (afn1.aceptacion + ajuste1, ''): [aceptacion],
        (afn2.aceptacion + ajuste2, ''): [aceptacion]
    }
    # Ajusta y combina transiciones de ambos autómatas en el autómata resultante.
    for (estado, simbolo), siguientes_estados in afn1.transiciones.items():
        transiciones[(estado + ajuste1, simbolo)] = [s + ajuste1 for s in siguientes_estados]
    for (estado, simbolo), siguientes_estados in afn2.transiciones.items():
        transiciones[(estado + ajuste2, simbolo)] = [s + ajuste2 for s in siguientes_estados]
    return AFNoDeterminista(inicio, aceptacion, transiciones)


# Construye un autómata finito no determinista (AFN) a partir de una expresión regular en notación postfija.
def construir_afn(postfija):
    pila = Pila()
    # Diccionario que asocia operadores de expresión regular con sus funciones correspondientes.
    operadores = {'.': operador_concatenacion, '|': operador_or, '*': operador_kleene}

    # Procesa cada carácter de la expresión postfija, aplicando operadores o creando caracteres.
    for char in postfija:
        if char in operadores:
            if char == '*':  # Aplica operador unario Kleene.
                afnd = pila.desapilar()
                pila.apilar(operadores[char](afnd))
            else:  # Aplica operadores binarios.
                afn2 = pila.desapilar()
                afn1 = pila.desapilar()
                pila.apilar(operadores[char](afn1, afn2))
        else:
            pila.apilar(crear_caracter(char))  # Crea un nodo de carácter y lo añade a la pila.
    return pila.desapilar()  # Devuelve el AFN construido.



# Genera una representación gráfica de un autómata finito no determinista (AFN) y la guarda como un archivo PNG.
def dibujar_afn(afn, indice):
    grafo = Digraph()  # Crea un objeto grafo para visualización.
    grafo.attr(rankdir='LR')  # Ajusta la dirección del grafo de izquierda a derecha.
    # Añade nodos al grafo, marcando el estado de aceptación con un doble círculo.
    for estado in range(afn.aceptacion + 1):
        grafo.node(str(estado), shape='doublecircle' if estado == afn.aceptacion else 'circle')
    # Añade aristas entre los estados basados en las transiciones del AFN.
    for (estado, simbolo), siguientes_estados in afn.transiciones.items():
        for siguiente_estado in siguientes_estados:
            grafo.edge(str(estado), str(siguiente_estado), label=simbolo or 'ε')
    # Guarda el grafo en un archivo PNG.
    grafo.render(f'AFN{indice + 1}', view=False, format='png')


# Expande un conjunto de estados utilizando transiciones epsilon para formar el cierre epsilon.
def formar_nuevo_conjunto(actual, transiciones):
    nuevo_conjunto = set()  # Inicializa un nuevo conjunto para el cierre.
    cola = list(actual)  # Usa una cola para manejar los estados pendientes de procesar.

    # Procesa cada estado en la cola, agregando nuevos estados alcanzables vía transiciones epsilon.
    while cola:
        estado = cola.pop(0)
        nuevo_conjunto.add(estado)
        if (estado, '') in transiciones:
            for destino in transiciones[(estado, '')]:
                if destino not in nuevo_conjunto:
                    cola.append(destino)

    return nuevo_conjunto  # Devuelve el conjunto expandido.


# Convierte un conjunto de estados en una cadena de texto, separada por comas.
def conjunto_a_cadena(conjunto):
    return ','.join(str(elemento) for elemento in conjunto)  # Utiliza una comprensión de lista para formatear el conjunto como una cadena.


# Convierte un autómata finito no determinista (AFN) en un autómata finito determinista (AFD) utilizando el método de subconjuntos.
def calcular_subconjuntos(afn):
    # Obtener todas las transiciones del autómata finito no determinista (AFN) proporcionado.
    transiciones_afn = afn.obtener_transiciones()

    caracteres = []  # Lista para almacenar los caracteres únicos usados en las transiciones.
    transiciones_procesadas = {}  # Diccionario para mantener transiciones procesadas, reemplazando 'ε' por ''.

    # Procesar cada transición para ajustar las transiciones epsilon:
    for key in transiciones_afn:
        # Reemplaza transiciones epsilon ('ε') por transiciones vacías ('') para estandarizar el manejo.
        if key[1] == 'ε':
            transiciones_procesadas[(key[0], '')] = transiciones_afn[key]
        else:
            # Mantener las transiciones no epsilon tal como están.
            transiciones_procesadas[key] = transiciones_afn[key]

    # Actualizar el diccionario de transiciones con las transiciones procesadas.
    transiciones_afn = transiciones_procesadas

    # Extraer y almacenar todos los caracteres utilizados en las transiciones que no son epsilon.
    for key in transiciones_afn.keys():
        if key[1] != '':
            caracteres.append(key[1])
    # Ordenar alfabéticamente los caracteres para asegurar consistencia en el procesamiento.
    caracteres = sorted(caracteres)
    # Establecer una transición de auto-bucle para el estado de aceptación en transiciones vacías para manejar el cierre.
    transiciones_afn[(afn.obtener_aceptacion(), '')] = [afn.obtener_aceptacion()]

    estados = []  # Lista para almacenar todos los estados únicos del AFN.
    # Recopilar todos los estados involucrados en las transiciones.
    for key in transiciones_afn.keys():
        estados.append(key[0])

    # Agregar una cadena vacía a la lista de caracteres para manejar transiciones epsilon en el algoritmo de subconjuntos.
    caracteres.append('')
    # Ordenar los estados para asegurar un procesamiento consistente.
    estados.sort()

    conjuntos = {}  # Diccionario para almacenar el cierre epsilon de cada estado.
    # Generar el cierre epsilon para cada estado y caracter.
    for estado in estados:
        for caracter in caracteres:
            if caracter == '':
                # Si el estado tiene transiciones epsilon, procesarlas para formar el cierre epsilon.
                if ((estado, caracter) in transiciones_afn.keys()):
                    conjunto_temp = copy.deepcopy(transiciones_afn[(estado, caracter)])
                    conjunto_temp.append(estado)
                    # Utiliza la función formar_nuevo_conjunto para calcular el cierre epsilon.
                    conjuntos[estado] = {'ε': formar_nuevo_conjunto(conjunto_temp, transiciones_afn)}
            else:
                # Almacenar transiciones normales y cierres epsilon en el diccionario.
                if ((estado, caracter) in transiciones_afn.keys()):
                    conjuntos[estado] = {caracter: set(transiciones_afn[(estado, caracter)]), 'ε': set([estado])}

    # Identificar el conjunto inicial para el estado de inicio del AFN.
    for conj in conjuntos.values():
        if afn.obtener_inicio() in conj['ε']:
            nodo_inicio = conj['ε']

    # Convertir el conjunto inicial del estado de inicio a una cadena para usar en la construcción del AFD.
    cadena_inicio = conjunto_a_cadena(nodo_inicio)
    # Inicializar la lista de conjuntos del AFD con el conjunto inicial.
    conjuntos_afd = [cadena_inicio]
    # Diccionario para almacenar las transiciones del AFD.
    transiciones_afd = {}

    # Bucle para iterar hasta que no haya más cambios en los conjuntos de estados del AFD, asegurando que todos los estados posibles sean explorados.
    hay_cambio = True
    while hay_cambio:
        hay_cambio = False
        for conjunto in conjuntos_afd:
            for caracter in caracteres:
                nuevo_conjunto = set()
                # Divide el conjunto actual en estados individuales y explora transiciones para cada caracter.
                for elemento in conjunto.split(','):
                    estado = int(elemento)
                    # Si existe una transición para ese caracter desde el estado actual, expande el nuevo conjunto con el cierre epsilon del destino.
                    if caracter != '':
                        if (estado, caracter) in transiciones_afn:
                            for destino in transiciones_afn[(estado, caracter)]:
                                for cierre in conjuntos[destino]['ε']:
                                    nuevo_conjunto.add(cierre)
                # Si se forma un nuevo conjunto, se agrega a los conjuntos del AFD y se marca que hubo un cambio.
                if len(nuevo_conjunto) > 0:
                    cadena_conjunto = conjunto_a_cadena(nuevo_conjunto)
                    transiciones_afd[(conjunto, caracter)] = cadena_conjunto
                    if cadena_conjunto not in conjuntos_afd:
                        conjuntos_afd.append(cadena_conjunto)
                        hay_cambio = True

    # Asigna letras del alfabeto a cada conjunto único para simplificar las transiciones del AFD.
    alfabeto_mayusculas = list(string.ascii_uppercase)
    mapeo = list(zip(list(conjuntos_afd), alfabeto_mayusculas))

    # Crea transiciones nuevas basadas en el mapeo de conjuntos a sus respectivas letras.
    transiciones_nuevas = {}
    for trans in transiciones_afd:
        for mapeo_conjunto in mapeo:
            if trans[0] == mapeo_conjunto[0]:
                transiciones_nuevas[(mapeo_conjunto[1], trans[1])] = transiciones_afd[trans]

    # Establece las transiciones finales del AFD a partir de las nuevas transiciones mapeadas.
    transiciones_finales = {}
    for trans in transiciones_nuevas:
        for mapeo_conjunto in mapeo:
            if transiciones_nuevas[trans] == mapeo_conjunto[0]:
                transiciones_finales[trans] = mapeo_conjunto[1]

    # Determina los nodos de aceptación en el AFD basado en la presencia del estado de aceptación del AFN en los conjuntos.
    nodos_aceptacion = []
    for conjunto in conjuntos_afd:
        if str(afn.obtener_aceptacion()) in conjunto:
            nodos_aceptacion.append(conjunto)

    # Actualizar la cadena de inicio con el identificador asignado en el mapeo.
    for mapeo_conjunto in mapeo:
        if mapeo_conjunto[0] == cadena_inicio:
            cadena_inicio = mapeo_conjunto[1]

    # Mapear los nodos de aceptación a sus identificadores correspondientes para uso en el AFD.
    nodos_aceptacion_mapeados = []
    for nodo in nodos_aceptacion:
        for mapeo_conjunto in mapeo:
            if nodo == mapeo_conjunto[0]:
                nodos_aceptacion_mapeados.append(mapeo_conjunto[1])

    # Filtrar y recopilar los caracteres que son válidos para transiciones, excluyendo los especiales y vacíos.
    caracteres_validos = []
    for caracter in caracteres:
        if caracter not in caracteres_validos and caracter != '' and caracter != 'ε':
            caracteres_validos.append(caracter)

    # Mapear y finalizar la configuración de transiciones para el AFD, asegurando que todas las transiciones sean válidas.
    transiciones_finales_mapeadas = {}
    for trans in transiciones_finales:
        for caracter in caracteres_validos:
            if (trans[0], caracter) not in transiciones_finales:
                # Crear un estado de "vaciado" para manejar transiciones no definidas.
                transiciones_finales_mapeadas[(trans[0], caracter)] = 'V'
                # Asegurar que el estado de "vaciado" tenga transiciones a sí mismo para todos los caracteres válidos.
                for c in caracteres_validos:
                    transiciones_finales_mapeadas[('V', c)] = 'V'
            else:
                # Asignar las transiciones finales mapeadas desde el conjunto original de transiciones.
                transiciones_finales_mapeadas[(trans[0], caracter)] = transiciones_finales[(trans[0], caracter)]

    # Devolver el AFD determinista con el conjunto inicial, los nodos de aceptación mapeados y las transiciones finales.
    return AFDeter(cadena_inicio, nodos_aceptacion_mapeados, transiciones_finales_mapeadas)


# Esta función genera y guarda una representación gráfica del AFD, en su forma simplificada.
def dibujar_afd(afd, indice, simplificado=False):
    # Selecciona el modo de visualización basado en el parámetro 'simplificado'.
    if simplificado:
        # Obtiene la representación gráfica del AFD simplificado.
        grafo = afd.visualizar()
        # Guarda el gráfico como un archivo PNG para el AFD simplificado.
        grafo.render(f'AFDSimplificado{indice+1}', view=False, format='png')
    else:
        # Obtiene la representación gráfica del AFD estándar.
        grafo = afd.visualizar()
        # Guarda el gráfico como un archivo PNG para el AFD estándar.
        grafo.render(f'AFD{indice+1}', view=False, format='png')


# Minimiza un AFD utilizando el algoritmo de minimización de estados, agrupando estados equivalentes.
def reducir_afd(afd):
    # Obtener las transiciones, estado inicial y estados de aceptación del AFD.
    transiciones_afd = afd.obtener_transiciones()
    estado_inicial_afd = afd.obtener_inicio()
    estados_aceptacion_afd = afd.obtener_aceptacion()

    # Inicializar las particiones con estados de aceptación y no aceptación.
    particiones = []
    estados_no_aceptacion = [estado for estado, _ in transiciones_afd.keys() if estado not in estados_aceptacion_afd]
    particiones.append(estados_no_aceptacion)   
    particiones.append(estados_aceptacion_afd)

    # Recopilar y ordenar todos los símbolos usados en las transiciones para procesar uniformemente.
    caracteres_unicos = sorted(list(set([simbolo for _, simbolo in transiciones_afd.keys()])))

    # Ejecutar el bucle de refinamiento de particiones hasta que no haya cambios.
    while True:
        nuevas_particiones = []  # Lista para mantener nuevas particiones basadas en la revisión actual.
        
        # Evaluar cada subconjunto de la partición actual para determinar si se puede dividir más.
        for subconjunto in particiones:
            subdivisiones = {}  # Diccionario para nuevas subdivisiones basadas en comportamiento de transiciones.

            # Analizar cada estado en el subconjunto para determinar su grupo basado en transiciones.
            for estado in subconjunto:
                clave = tuple()  # Clave para agrupar estados con comportamientos similares.
                for simbolo in caracteres_unicos:
                    # Revisar cada símbolo y determinar a qué partición conduce la transición.
                    if (estado, simbolo) in transiciones_afd:
                        destino = transiciones_afd[(estado, simbolo)]
                        for indice, categoria in enumerate(particiones):
                            if destino in categoria:
                                clave += (indice,)
                                break
                    else:
                        clave += (-1,)  # Indicar que no hay transición para ese símbolo.

                # Agrupar estados en el subconjunto actual según sus claves.
                if clave not in subdivisiones:
                    subdivisiones[clave] = []
                subdivisiones[clave].append(estado)

            # Agregar los grupos formados a las nuevas particiones.
            nuevas_particiones.extend(subdivisiones.values())

        # Verificar si las nuevas particiones son iguales a las anteriores; si lo son, terminar el bucle.
        if len(nuevas_particiones) == len(particiones):
            break
        particiones = nuevas_particiones  # Actualizar las particiones para la siguiente iteración.


    # Consolidar las particiones eliminando duplicados dentro de cada subconjunto y confirmando la partición final.
    particiones_finales = []
    for subconjunto in particiones:
        temporal = []
        for estado in subconjunto:
            if estado not in temporal:
                temporal.append(estado)

        if len(temporal) > 0:
            particiones_finales.append(temporal)

    particiones = particiones_finales  # Actualizar las particiones a las versiones finales.

    # Crear transiciones simplificadas que reflejen las nuevas particiones.
    transiciones_simplificadas = {}
    for simbolo in caracteres_unicos:
        for subconjunto in particiones:
            estado_fuente = ','.join(map(str, subconjunto))
            if (subconjunto[0], simbolo) in transiciones_afd:
                destino = transiciones_afd[(subconjunto[0], simbolo)]
                for categoria in particiones:
                    if destino in categoria:
                        transiciones_simplificadas[(estado_fuente, simbolo)] = ','.join(map(str, categoria))
                        break

    # Mapear las transiciones simplificadas a una forma final que será utilizada por el AFD determinista.
    transiciones_finales = {}
    for clave in transiciones_simplificadas:
        transiciones_finales[(clave[0][0], clave[1])] = transiciones_simplificadas[clave][0]

    # Actualizar el estado inicial basado en las transiciones finales.
    for clave in transiciones_finales:
        if clave[0] == estado_inicial_afd:
            estado_inicial_afd = clave[0]

    # Identificar los estados de aceptación finales basados en las transiciones finales.
    estados_aceptacion_finales = []
    for clave in transiciones_finales:
        if clave[0] in estados_aceptacion_afd and clave[0] not in estados_aceptacion_finales:
            estados_aceptacion_finales.append(clave[0])

    # Devolver el AFD determinista con los estados iniciales y de aceptación actualizados.
    return AFDeter(estado_inicial_afd, estados_aceptacion_finales, transiciones_finales)


def buscar_camino(ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice):
    if indice >= len(cadena):  # Verificar si alcanzamos el final de la cadena
        if ruta[-1] == estado_aceptacion_afn:
            return ruta
        else:
            # Probar transiciones epsilon desde el estado actual si no estamos en aceptación
            return explorar_epsilon(ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice)

    # Continuar con la cadena si no hemos terminado
    return procesar_simbolos(ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice)


# Explora las transiciones epsilon para encontrar un camino que acepte la cadena.
def explorar_epsilon(ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice):
    # Verifica si existen transiciones epsilon desde el último estado de la ruta.
    if (ruta[-1], 'ε') in transiciones_afn:
        for destino in transiciones_afn[(ruta[-1], 'ε')]:
            nueva_ruta = copy.deepcopy(ruta)  # Crea una nueva ruta con el destino añadido.
            nueva_ruta.append(destino)
            # Recursivamente busca un camino válido desde el nuevo estado.
            resultado = buscar_camino(nueva_ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice)
            if resultado is not None:
                return resultado  # Retorna el camino encontrado si es válido.


# Procesa el carácter actual de la cadena para avanzar en el autómata o explorar transiciones epsilon.
def procesar_simbolos(ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice):
    caracter_actual = cadena[indice]  # Carácter actual a procesar.
    # Verifica si existe una transición directa para el carácter actual.
    if (ruta[-1], caracter_actual) in transiciones_afn:
        for destino in transiciones_afn[(ruta[-1], caracter_actual)]:
            nueva_ruta = copy.deepcopy(ruta)  # Crea una nueva ruta con el destino añadido.
            nueva_ruta.append(destino)
            # Recursivamente busca un camino aceptado desde el nuevo estado.
            resultado = buscar_camino(nueva_ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice + 1)
            if resultado is not None:
                return resultado  # Retorna el resultado si encuentra un camino aceptado.

    # Si no hay transiciones directas disponibles, explora las transiciones epsilon.
    return explorar_epsilon(ruta, transiciones_afn, estado_aceptacion_afn, cadena, indice)


# Simula un autómata finito no determinista (AFN) sobre una cadena de entrada y devuelve si la cadena es aceptada o no.
def simular_afn(afn, cadena):
    cadena = cadena or 'ε'  # Simplifica la asignación para manejar cadenas vacías

    transiciones = afn.obtener_transiciones()
    inicio = afn.obtener_inicio()
    aceptacion = afn.obtener_aceptacion()

    # Procesar transiciones considerando transiciones epsilon
    transiciones_procesadas = {(origen, simbolo if simbolo else 'ε'): destinos 
                            for (origen, simbolo), destinos in transiciones.items()}

    # Extraer caracteres únicos y estados desde las transiciones
    caracteres = {simbolo for _, simbolo in transiciones_procesadas if simbolo}
    estados = {estado for estado in transiciones_procesadas}

    # Crear cierre epsilon para cada estado
    cierre_epsilon = {}
    for estado in estados:
        epsilon_closure = set([estado])
        cambios = True
        while cambios:
            cambios = False
            nuevos_estados = set()
            for e in epsilon_closure:
                if (e, 'ε') in transiciones_procesadas:
                    nuevos = set(transiciones_procesadas[(e, 'ε')]) - epsilon_closure
                    if nuevos:
                        nuevos_estados.update(nuevos)
                        cambios = True
            epsilon_closure.update(nuevos_estados)
        cierre_epsilon[estado] = sorted(epsilon_closure)

    # Verificar si la cadena tiene caracteres no permitidos
    if any(c not in caracteres for c in cadena):
        return f"{Fore.RED}LA CADENA NO ES ACEPTADA (NO CUMPLE CON LOS CARACTERES){Style.RESET_ALL}"

    # Intentar encontrar un camino que acepte la cadena
    intentos = 0
    while intentos < 2000:
        ruta = buscar_camino([inicio], transiciones_procesadas, aceptacion, cadena, 0)
        if ruta:
            break
        intentos += 1

    if not ruta:
        return f"{Fore.RED}LA CADENA NO ES ACEPTADA{Style.RESET_ALL}"

    print("Ruta encontrada:", ruta)
    if ruta[-1] == aceptacion:
        return f"{Fore.GREEN}LA CADENA ES ACEPTADA{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}LA CADENA NO ES ACEPTADA{Style.RESET_ALL}"


# Ejecuta un AFD sobre una cadena de entrada y devuelve si la cadena es aceptada o no
def ejecutar_afd(afd, cadena):
    # Reemplaza ε por una cadena vacía
    cadena = cadena.replace('ε', '')

    # Obtiene las transiciones, el estado inicial y los estados de aceptación del AFD
    transiciones_afd = afd.obtener_transiciones()
    estado_inicial_afd = afd.obtener_inicio()
    estados_aceptacion_afd = afd.obtener_aceptacion()

    # Inicializa el recorrido con el estado inicial
    recorrido = f'{estado_inicial_afd}'
    estado_actual = estado_inicial_afd

    # Itera sobre cada carácter de la cadena de entrada
    for simbolo in cadena:
        # Verifica si hay una transición desde el estado actual con el símbolo actual
        if (estado_actual, simbolo) in transiciones_afd:
            # Actualiza el estado actual a donde lleva la transición
            estado_actual = transiciones_afd[(estado_actual, simbolo)]
            # Actualiza el recorrido con la transición realizada
            recorrido += f' =>({simbolo}) {estado_actual}'
        else:
            # Si no hay transición, la cadena no es aceptada
            return Fore.RED + "LA CADENA NO ES ACEPTADA" + Style.RESET_ALL

    # Verifica si el estado actual es un estado de aceptación
    if estado_actual in estados_aceptacion_afd:
        # Imprime el recorrido completo de la cadena por el AFD
        print('Recorrido:\n', recorrido)
        return Fore.GREEN + "LA CADENA ES ACEPTADA" + Style.RESET_ALL
    else:
        # Si no está en un estado de aceptación, la cadena no es aceptada
        return Fore.RED + "LA CADENA NO ES ACEPTADA" + Style.RESET_ALL
