# Módulos
import sys, pygame, os
from pygame.locals import *

# Constantes
WIDTH = 600
HEIGHT = 600

class nodo:
    def __init__(self, valor="Manzana"):
        self.padre = None
        self.hijos = []
        self.valor = valor

    def esHoja(self):
        return not self.hijos

class arbol:
    def __init__(self):
        self.raiz = None

    def add_raiz(self, valor):
        nodo_temp = nodo(valor)
        self.raiz = nodo_temp
        return nodo_temp

    def add_nodo(self, padre, valor):
        nodo_temp = nodo(valor)
        padre.hijos.append(nodo_temp)
        nodo_temp.padre = padre
        return nodo_temp

    def ancestros(self, nodo):
        if not nodo:
            return []
        else:
            return self.ancestros(nodo.padre) + [nodo.valor]

def generar_vecinos(parameters, size, vecinosVisitados, arbolito, nodoActual, coordsB, cola):
    x = int(nodoActual.valor[0])
    y = int(nodoActual.valor[1])
    coordConj = str(x) + str(y)
    vecinosVisitados.add(coordConj)

    if not y == 0:
        if parameters[x][y - 1] == "1" or parameters[x][y - 1] == "B":
            vecinoIzq = nodo([x, y - 1])
            coordConj = str(x) + str(y - 1)

            if not coordConj in vecinosVisitados:
                nodito = arbolito.add_nodo(nodoActual, vecinoIzq.valor)
                if vecinoIzq.valor == coordsB:
                    print(arbolito.ancestros(nodito))
                    return arbolito.ancestros(nodito)
                #cola.append(nodito)
                cola.insert(0, nodito)

    if not x == 0:
        if parameters[x - 1][y] == "1" or parameters[x - 1][y] == "B":
            vecinoArriba = nodo([x - 1, y])
            coordConj = str(x - 1) + str(y)
            if not coordConj in vecinosVisitados:
                nodito = arbolito.add_nodo(nodoActual, vecinoArriba.valor)
                if vecinoArriba.valor == coordsB:
                    return arbolito.ancestros(nodito)
                # cola.append(nodito)
                cola.insert(0, nodito)

    if not x == int(size) - 1:
        if parameters[x + 1][y] == "1" or parameters[x + 1][y] == "B":
            vecinoAbajo = nodo([x + 1, y])
            coordConj = str(x + 1) + str(y)
            if not coordConj in vecinosVisitados:
                nodito = arbolito.add_nodo(nodoActual, vecinoAbajo.valor)
                # vecinosVisitados.add(coordConj)
                if vecinoAbajo.valor == coordsB:
                    return arbolito.ancestros(nodito)
                # cola.append(nodito)
                cola.insert(0, nodito)

    if not y == int(size) - 1:
        if parameters[x][y + 1] == "1" or parameters[x][y + 1] == "B":
            vecinoDer = nodo([x, y + 1])
            coordConj = str(x) + str(y + 1)
            if not coordConj in vecinosVisitados:
                nodito = arbolito.add_nodo(nodoActual, vecinoDer.valor)
                # vecinosVisitados.add(coordConj)
                if vecinoDer.valor == coordsB:
                    return arbolito.ancestros(nodito)
                # cola.append(nodito)
                cola.insert(0, nodito)


    # return parameters[x-1][y]

def main():
    pygame.init()
    # reloj = pygame.time.Clock()
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    vecinosVisitados = set()

    filename = sys.argv[1]
    file = open(filename)
    lista = file.read().splitlines()
    coordsLab = lista[0].split(" ")
    rows = coordsLab[0]
    cols = coordsLab[1]
    size = WIDTH / int(rows)
    # sizeY = WIDTH / int(cols)

    parameters = lista[1:]

    color = dict()
    color["blanco"] = (255, 255, 255)
    color["azul"] = (0, 0, 255)
    color["rojo"] = (0, 255, 0)
    color["verde"] = (0, 255, 0)
    color["negro"] = (0, 0, 0)
    color["inicio"] = (255, 255, 255)
    color["fin"] = (0, 0, 0)
    color["camino"] = (176, 252, 255)
    color["pared"] = (7, 114, 117)

    pantalla.fill(color["blanco"])

    left = 0
    top = 0
    coords = (left, top, size, size)   # (left, top, width, height)
    laberinto = []
    counterx = 0
    countery = 0

    ## Gráfico
    for fila in parameters:
        coords = (left, top, size, size)
        for dig in fila:
            coords = (left, top, size, size)
            if dig == "A":
                colorActual = color["inicio"]
                coordsInicio = [countery, counterx]

            elif dig == "B":
                colorActual = color["fin"]
                coordsB = [countery, counterx]

            elif dig == "0":
                colorActual = color["pared"]

            elif dig == "1":
                colorActual = color["camino"]

            laberinto.append(pygame.draw.rect(pantalla, colorActual, coords))
            left += size
            counterx += 1

        left = 0
        counterx = 0
        top += size
        countery += 1

    # Creamos el ÁRBOL
    arbolito = arbol()
    raiz = arbolito.add_raiz(coordsInicio)
    cola = []
    cola.append(raiz)

    i = 0
    while cola:
        nodoActual = cola.pop()

        camino = generar_vecinos(parameters, rows, vecinosVisitados, arbolito, nodoActual, coordsB, cola)
        if not camino == None:
            break

        '''print(nodoActual.valor)
        print(cola[0].valor)
        print(cola)
        print(vecinosVisitados)'''
    camino.pop(0)
    camino.pop(len(camino)-1)

    conjuntoInicio = set()
    x = coordsInicio[0]
    y = coordsInicio[1]
    inicio = str(x) + str(y)
    conjuntoInicio.add(inicio)
    vecinosVisitados = vecinosVisitados - conjuntoInicio

    for element in vecinosVisitados:
        x = int(element[0])
        y = int(element[1])

        coords = (y * size, x * size, size, size)
        laberinto.append(pygame.draw.rect(pantalla, color["verde"], coords))


    for element in camino:
        x = element[0]
        y = element[1]

        coords = (y * size, x * size, size, size)
        laberinto.append(pygame.draw.rect(pantalla, color["azul"], coords))



    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

        laberinto
        pygame.display.update()
        # reloj.tick(1)


if __name__ == '__main__':
    main()