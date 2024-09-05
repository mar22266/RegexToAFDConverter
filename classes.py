""" File donde estan las clases necesarias para el proyecto """

# Importar la clase Digraph de la librería graphviz
from graphviz import Digraph

# Clase para representar un nodo de un árbol. Se utiliza en la construcción de árboles para representar expresiones regulares.
class Nodo:
    def __init__(self, valor, identificador):
        # Inicializa el nodo con un valor y un identificador.
        # valor: Contenido del nodo, que puede ser un operador o un carácter.
        # identificador: Identificador único para cada nodo, útil para visualizaciones gráficas.
        self.valor = valor
        self.identificador = identificador
        self.izquierda = None
        self.derecha = None
    
    def graficar_nodo(self, grafo):
        # Agrega el nodo actual al objeto grafo (de tipo graphviz.Digraph u otro compatible).
        grafo.node(self.identificador, label=str(self.valor))
        # Si el nodo tiene un hijo izquierdo, crea una arista hacia él y llama recursivamente a graficar.
        if self.izquierda is not None:
            grafo.edge(self.identificador, self.izquierda.identificador)
            self.izquierda.graficar_nodo(grafo)
        # Si el nodo tiene un hijo derecho, crea una arista hacia él y llama recursivamente a graficar.
        if self.derecha is not None:
            grafo.edge(self.identificador, self.derecha.identificador)
            self.derecha.graficar_nodo(grafo)
            
# Clase para representar un árbol. Usada para construir y visualizar estructuras de árboles derivados de expresiones regulares.
class Arbol:
    def __init__(self, raiz, nombre):
        # Inicializa el árbol con una raíz y un nombre.
        # raiz: El nodo raíz del árbol.
        # nombre: Nombre del árbol, usado para crear archivos de salida gráficos.
        self.raiz = raiz
        self.nombre = nombre
    
    def graficar(self):
        # Crea y visualiza un gráfico del árbol usando graphviz.
        grafo = Digraph('G', filename=f'AST-{self.nombre}.gv', format='png')
        # Inicia el proceso de graficación desde la raíz.
        self.raiz.graficar_nodo(grafo)
        # Muestra el gráfico.
        grafo.view()

# Clase para representar una pila.
class Pila:
    def __init__(self):
        # Inicializa la pila con una lista vacía para almacenar los elementos.
        self.elementos = []

    def apilar(self, elemento):
        # Agrega un elemento al final de la lista (top de la pila).
        self.elementos.append(elemento)
    
    def desapilar(self):
        # Elimina el último elemento agregado a la pila y lo devuelve.
        return self.elementos.pop()
    
    def esta_vacia(self):
        # Devuelve True si la pila está vacía, False de lo contrario.
        return len(self.elementos) == 0

    def ver_tope(self):
        # Devuelve el último elemento agregado a la pila sin eliminarlo.
        # Retorna None si la pila está vacía.
        if self.esta_vacia():
            return None
        else:
            return self.elementos[-1]
    
    def tamano(self):
        # Devuelve el número de elementos en la pila.
        return len(self.elementos)

# Clase para representar un Autómata Finito No Determinista (AFN).
class AFNoDeterminista:
    def __init__(self, inicio, aceptacion, transiciones):
        # Inicializa el AFN con estados de inicio, aceptación y transiciones.
        # inicio: Estado inicial del AFN.
        # aceptacion: Conjunto de estados de aceptación.
        # transiciones: Diccionario que mapea pares a un conjunto de estados destino.
        self.inicio = inicio
        self.aceptacion = aceptacion
        self.transiciones = transiciones

    def obtener_transiciones(self):
        # Devuelve el diccionario de transiciones del autómata.
        return self.transiciones
    
    def obtener_inicio(self):
        # Devuelve el estado inicial del autómata.
        return self.inicio
    
    def obtener_aceptacion(self):
        # Devuelve el conjunto de estados de aceptación del autómata.
        return self.aceptacion

# Clase para representar un Autómata Finito Determinista (AFD).
class AFDeter:
    def __init__(self, nodo_inicio, nodos_aceptacion, transiciones):
        # Inicializa el AFD con un nodo de inicio, nodos de aceptación y transiciones.
        # nodo_inicio: Estado inicial del AFD.
        # nodos_aceptacion: Conjunto de estados de aceptación.
        # transiciones: Diccionario que mapea pares a estados destino.
        self.nodo_inicio = nodo_inicio
        self.nodos_aceptacion = nodos_aceptacion
        self.transiciones = transiciones

    def obtener_transiciones(self):
        # Devuelve el diccionario de transiciones del autómata.
        return self.transiciones
    
    def obtener_inicio(self):
        # Devuelve el estado inicial del autómata.
        return self.nodo_inicio
    
    def obtener_aceptacion(self):
        # Devuelve el conjunto de estados de aceptación del autómata.
        return self.nodos_aceptacion

    def visualizar(self):
        # Crea una visualización del AFD utilizando graphviz.
        dot = Digraph('AFD')
        
        todos_nodos = set()
        # Recopila todos los nodos del autómata para su visualización.
        for (origen, _), destino in self.transiciones.items():
            todos_nodos.add(origen)
            todos_nodos.add(destino)
        
        # Crea nodos en graphviz. Estados de aceptación se muestran con un doble círculo.
        for nodo in todos_nodos:
            if nodo in self.nodos_aceptacion:
                dot.node(nodo, shape='doublecircle')
            else:
                dot.node(nodo)
        
        # Crea las aristas con etiquetas para cada transición.
        for (origen, etiqueta), destino in self.transiciones.items():
            dot.edge(origen, destino, label=etiqueta)
        
        # Devuelve el objeto graphviz para su visualización.
        return dot
