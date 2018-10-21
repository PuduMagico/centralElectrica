import csv
#mm2*omega/km
from _csv import reader

rho = 0.0172


class ListaDistancias:
    def __init__(self, id, val):
        self.id = id
        self.val = val
        self.siguiente = None

    def añadir(self, id, val):
        actual = self
        while actual.siguiente != None:
            actual = self.siguiente
        actual.siguiente = ListaDistancias(id, val)

    def encontrarDistancia(self, id):
        actual = self
        while actual.id != id:
            actual = actual.siguiente
        return actual.val


class ListaNodos:
    def __init__(self, nodo):
        self.nodo = nodo
        self.siguiente = None

    def añadir(self, nodo):
        actual = self
        while actual.siguiente != None:
            actual = self.siguiente
        actual.siguiente = ListaNodos(nodo)

    def largoLista(self):
        l = 0
        nodoActual = self
        if nodoActual.nodo == None:
            return 0
        while nodoActual != None:
            l += 1
            nodoActual = nodoActual.siguiente
        return l


class Red:
    def __init__(self):
        self.generadoras = None
        self.potenciaTotal = 0

    def agregar(self, nodo):
        if nodo.clase == "Generadora":
            if self.generadoras == None:
                self.generadoras = ListaNodos(nodo)
            else:
                self.generadoras.añadir(nodo)
            self.potenciaTotal += nodo.potencia
        else:
            print("error")

    def demandaTotal(self):
        demandaTotal = 0
        nodoActual = self.generadoras
        while nodoActual != None:
            demandaTotal += nodoActual.nodo.demanda()
            nodoActual = nodoActual.siguiente
        return demandaTotal

    def distribuir(self):
        nodoActual = self.generadoras
        demandaTotal = self.demandaTotal()
        while nodoActual != None:
            demandaTotal += nodoActual.nodo.demanda()
            nodoActual = nodoActual.siguiente
            print(demandaTotal)
        print("Potencia Total:", self.potenciaTotal)
        print("Demanda Total:", demandaTotal)
        if self.potenciaTotal >= demandaTotal:
            print("todo ok")
        else:
            print("falta energia, comenzar simulacion")
            self.simulacion()

    def simulacion(self):
        nodoActual = self.generadoras
        while nodoActual != None:
            numeroHijos = nodoActual.nodo.hijos.largoLista()
            print(numeroHijos)
            hijoActual = nodoActual.nodo.hijos
            while hijoActual != None:
                distancia = nodoActual.nodo.distancias.encontrarDistancia(hijoActual.nodo.id)
                print(distancia, hijoActual.nodo.id)
                print("potencia q le estoy dando", nodoActual.nodo.potencia / numeroHijos)
                print("su consumo", hijoActual.nodo.consumo)
                print("gasto por distancia", nodoActual.nodo.potencia * rho * distancia / (253 * numeroHijos))

                if nodoActual.nodo.potencia / numeroHijos > hijoActual.nodo.consumo + nodoActual.nodo.potencia * rho * distancia / (
                        253 * numeroHijos):
                    hijoActual.nodo.potenciaDisponible += nodoActual.nodo.potencia / numeroHijos - (
                                hijoActual.nodo.consumo + nodoActual.nodo.potencia * rho * distancia / (
                                    253 * numeroHijos))
                    hijoActual.nodo.consumo = 0
                elif nodoActual.nodo.potencia / numeroHijos < hijoActual.nodo.consumo + nodoActual.nodo.potencia * rho * distancia / (
                        253 * numeroHijos) and nodoActual.nodo.potencia / numeroHijos > nodoActual.nodo.potencia * rho * distancia / (
                        253 * numeroHijos):
                    hijoActual.nodo.consumo -= nodoActual.nodo.potencia / numeroHijos - nodoActual.nodo.potencia * rho * distancia / (
                                253 * numeroHijos)
                else:
                    pass

                print(hijoActual.nodo.consumo)
                print(hijoActual.nodo.potenciaDisponible)
                hijoActual = hijoActual.siguiente

            nodoActual = nodoActual.siguiente
        print("???")
        nodoActual = self.generadoras
        print("oka")
        while nodoActual != None:
            print("hola")
            hijoActual = nodoActual.nodo.hijos
            while hijoActual != None:
                if hijoActual.nodo.simulado == 0:
                    hijoActual.nodo.simulacion()
                    hijoActual.nodo.simulado = 1
                hijoActual = hijoActual.siguiente
            nodoActual = nodoActual.siguiente


class Nodo:
    def __init__(self, id, sistema, provincia, comuna):
        self.id = id
        self.sistema = sistema
        self.provincia = provincia
        self.comuna = comuna
        self.hijos = None
        self.distancias = None
        self.potenciaDisponible = 0
        self.clase = ""
        self.simulado = 0

    def __str__(self):
        format_string = "id={} sistema={} provincia={} comuna={} clase={}"
        retval = format_string.format(self.id, self.sistema, self.provincia, self.comuna, self.clase)
        return retval


class Generadora(Nodo):
    def __init__(self, id, nombre, sistema, provincia, comuna, tipo, potencia):
        Nodo.__init__(self, id, sistema, provincia, comuna)
        self.nombre = nombre
        self.tipo = tipo
        self.potencia = potencia
        self.clase = "Generadora"

    def agregar(self, nodo, dist):
        # and noLoop(nodo,Self):
        if nodo.clase == "Elevadora":
            nodo.proveedores += 1
            # nodo.potenciaDisponible = nodo.potenciaDisponible + self.potencia - self.potencia*dist*rho/253
            if self.hijos == None:
                self.hijos = ListaNodos(nodo)
            else:
                self.hijos.añadir(nodo)
            if self.distancias == None:
                self.distancias = ListaDistancias(nodo.id, dist)
            else:
                self.distancias.añadir(nodo.id, dist)

        elif not noLoop(nodo, Self):
            print("loop")
        else:
            print("movimiento malo")

    def demanda(self):
        potenciaHijos = 0
        hijoActual = self.hijos
        while hijoActual != None:
            distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
            potenciaHijos += (hijoActual.nodo.demanda() / hijoActual.nodo.proveedores) / (1 - rho * distancia / 253)

            hijoActual = hijoActual.siguiente

        return potenciaHijos


def load_generadora(filename, container):
    with open('data/' + filename, 'r') as csvfile:
        file = csv.reader(csvfile)
        next(file, None)  # skip the first line as it contains headers
        for row in file:
            [id, nombre, sistema, provincia, comuna, tipo, potencia] = row
            newItem = Generadora(id, nombre, sistema, provincia, comuna, tipo, potencia)
            container.append(newItem)


class Elevadora(Nodo):
    def __init__(self, id, nombre, sistema, provincia, comuna, consumo):
        Nodo.__init__(self, id, sistema, provincia, comuna)
        self.nombre = nombre
        self.consumo = consumo
        self.proveedores = 0
        self.clase = "Elevadora"

    def agregar(self, nodo, dist):
        # and noLoop(nodo,Self):
        if nodo.clase == "Transmision" and nodo.proveedores == 0:
            nodo.proveedores += 1
            if self.hijos == None:
                self.hijos = ListaNodos(nodo)
            else:
                self.hijos.añadir(nodo)
            if self.distancias == None:
                self.distancias = ListaDistancias(nodo.id, dist)
            else:
                self.distancias.añadir(nodo.id, dist)
        elif nodo.proveedores != 0:
            print("este nodo ya tiene un proveedor")

        elif not noLoop(nodo, Self):
            print("loop")
        else:
            print("movimiento malo")

    def demanda(self):
        if self.hijos.nodo == None:
            return self.consumo
        else:
            potenciaHijos = 0
            hijoActual = self.hijos
            while hijoActual != None:
                # el 85 corresponde a la seccion transversal
                distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
                potenciaHijos += (hijoActual.nodo.demanda() / hijoActual.nodo.proveedores) / (
                            1 - rho * distancia / 202.7)

                hijoActual = hijoActual.siguiente

            return self.consumo + potenciaHijos

    def simulacion(self):
        hijoActual = self.hijos
        demandaHijosTotal = 0

        while hijoActual != None:
            distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
            demandaHijosTotal += hijoActual.nodo.demanda() / (1 - rho * distancia / 202.7)
            hijoActual = hijoActual.siguiente

        hijoActual = self.hijos
        while hijoActual != None:

            distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
            print(distancia, hijoActual.nodo.id)

            print("potencia q le estoy dando",
                  self.potenciaDisponible * (hijoActual.nodo.demanda() / (1 - rho * distancia / demandaHijosTotal)))
            print("su consumo", hijoActual.nodo.consumo)
            print("gasto por distancia", self.potenciaDisponible * rho * distancia / 202.7)

            potenciaDada = self.potenciaDisponible * (
                        hijoActual.nodo.demanda() / (1 - rho * distancia / demandaHijosTotal))
            if potenciaDada > hijoActual.nodo.consumo + self.potenciaDisponible * rho * distancia / 202.7:
                hijoActual.nodo.potenciaDisponible += self.potenciaDisponible - (
                            hijoActual.nodo.consumo + self.potenciaDisponible * rho * distancia / 202.7)
                hijoActual.nodo.consumo = 0
            elif potenciaDada < hijoActual.nodo.consumo + self.potenciaDisponible * rho * distancia / 202.7 and self.potenciaDisponible > self.potenciaDisponible * rho * distancia / 202.7:
                hijoActual.nodo.consumo -= self.potenciaDisponible - self.potenciaDisponible * rho * distancia / 202.7
            else:
                pass
            self.potenciaDisponible -= potenciaDada
            print(hijoActual.nodo.consumo)
            print(hijoActual.nodo.potenciaDisponible)
            self.hijos.nodo.simular()
            hijoActual = hijoActual.siguiente


def load_elevadora(filename, container):
    with open('data/' + filename, 'r') as csvfile:
        file = csv.reader(csvfile)
        next(file, None)  # skip the first line as it contains headers
        for row in file:
            [id, nombre, sistema, provincia, comuna, consumo] = row
            newItem = Elevadora(id, nombre, sistema, provincia, comuna, consumo)
            container.append(newItem)

class Transmision(Nodo):
    def __init__(self, id, nombre, sistema, provincia, comuna, consumo):
        Nodo.__init__(self, id, sistema, provincia, comuna)
        self.nombre = nombre
        self.consumo = consumo
        self.proveedores = 0
        self.clase = "Transmision"

    def agregar(self, nodo, dist):
        # and noLoop(nodo,Self):
        if nodo.clase == "Distribucion" and nodo.proveedores == 0:
            nodo.proveedores += 1
            if self.hijos == None:
                self.hijos = ListaNodos(nodo)
            else:
                self.hijos.añadir(nodo)
            if self.distancias == None:
                self.distancias = ListaDistancias(nodo.id, dist)
            else:
                self.distancias.añadir(nodo.id, dist)
        elif nodo.proveedores != 0:
            print("este nodo ya tiene un proveedor")

        elif not noLoop(nodo, Self):
            print("loop")
        else:
            print("movimiento malo")

    def demanda(self):
        if self.hijos.nodo == None:
            return self.consumo
        else:
            potenciaHijos = 0
            hijoActual = self.hijos
            while hijoActual != None:
                # el 85 corresponde a la seccion transversal
                distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
                potenciaHijos += (hijoActual.nodo.demanda() / hijoActual.nodo.proveedores) / (1 - rho * distancia / 152)

                hijoActual = hijoActual.siguiente

            return self.consumo + potenciaHijos

    def simular(self):
        hijoActual = self.hijos
        while hijoActual != None:
            distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
            print(distancia, hijoActual.nodo.id)

            print("potencia q le estoy dando", self.potenciaDisponible)
            print("su consumo", hijoActual.nodo.consumo)
            print("gasto por distancia", self.potenciaDisponible * rho * distancia / 202.7)

            if self.potenciaDisponible > hijoActual.nodo.consumo + self.potenciaDisponible * rho * distancia / 202.7:
                hijoActual.nodo.potenciaDisponible += self.potenciaDisponible - (
                            hijoActual.nodo.consumo + self.potenciaDisponible * rho * distancia / 202.7)
                hijoActual.nodo.consumo = 0
            elif self.potenciaDisponible < hijoActual.nodo.consumo + self.potenciaDisponible * rho * distancia / 202.7 and self.potenciaDisponible > self.potenciaDisponible * rho * distancia / 202.7:
                hijoActual.nodo.consumo -= self.potenciaDisponible - self.potenciaDisponible * rho * distancia / 202.7
            else:
                pass

            print(hijoActual.nodo.consumo)
            print(hijoActual.nodo.potenciaDisponible)
            hijoActual = hijoActual.siguiente

        self.hijos.nodo.simular()



def load_transmision(filename, container):
    with open('data/' + filename, 'r') as csvfile:
        file = csv.reader(csvfile)
        next(file, None)  # skip the first line as it contains headers
        for row in file:
            [id, nombre, sistema, provincia, comuna, consumo] = row
            newItem = Transmision(id, nombre, sistema, provincia, comuna, consumo)
            container.append(newItem)


class Distribucion(Nodo):
    def __init__(self, id, nombre, sistema, provincia, comuna, consumo):
        Nodo.__init__(self, id, sistema, provincia, comuna)
        self.nombre = nombre
        self.consumo = consumo
        self.proveedores = 0
        self.clase = "Distribucion"

    def agregar(self, nodo, dist):
        # and noLoop(nodo,Self):
        if nodo.clase == "Casa":
            nodo.proveedores += 1
            if self.hijos == None:
                self.hijos = ListaNodos(nodo)
            else:
                self.hijos.añadir(nodo)
            if self.distancias == None:
                self.distancias = ListaDistancias(nodo.id, dist)
            else:
                self.distancias.añadir(nodo.id, dist)

        elif not noLoop(nodo, Self):
            print("loop")
        else:
            print("movimiento malo")

    def demanda(self):
        if self.hijos.nodo == None:
            return self.consumo
        else:
            potenciaHijos = 0
            hijoActual = self.hijos
            while hijoActual != None:
                # el 85 corresponde a la seccion transversal
                distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
                potenciaHijos += (hijoActual.nodo.demanda() / hijoActual.nodo.proveedores) / (1 - rho * distancia / 85)

                hijoActual = hijoActual.siguiente

            return self.consumo + potenciaHijos

def load_distribucion(filename, container):
    with open('data/' + filename, 'r') as csvfile:
        file = csv.reader(csvfile)
        next(file, None)  # skip the first line as it contains headers
        for row in file:
            [id, nombre, sistema, provincia, comuna, consumo] = row
            newItem = Distribucion(id, nombre, sistema, provincia, comuna, consumo)
            container.append(newItem)



class Casa(Nodo):
    def __init__(self, id, sistema, provincia, comuna, consumo):
        Nodo.__init__(self, id, sistema, provincia, comuna)
        self.consumo = consumo
        self.proveedores = 0
        self.clase = "Casa"

    def __str__(self):
        retval = '{} id={} sistema={} provincia={} comuna={} consumo={} proveedores={}'
        retval = retval.format(self.clase, self.id, self.sistema, self.provincia,
                               self.comuna, self.consumo, self.proveedores)
        return retval

    def agregar(self, nodo, dist):
        # and noLoop(nodo,Self):
        if nodo.clase == "Casa":
            nodo.proveedores += 1
            if self.hijos == None:
                self.hijos = ListaNodos(nodo)
            else:
                self.hijos.añadir(nodo)
            if self.distancias == None:
                self.distancias = ListaDistancias(nodo.id, dist)
            else:
                self.distancias.añadir(nodo.id, dist)

        elif not noLoop(nodo, Self):
            print("loop")
        else:
            print("movimiento malo")

    def remover(self, nodo):
        pass

    def demanda(self):
        if self.hijos == None:
            return self.consumo
        else:
            potenciaHijos = 0
            hijoActual = self.hijos
            while hijoActual != None:
                # el 85 corresponde a la seccion transversal
                distancia = self.distancias.encontrarDistancia(hijoActual.nodo.id)
                potenciaHijos += (hijoActual.nodo.demanda() / hijoActual.nodo.proveedores) / (1 - rho * distancia / 85)

                hijoActual = hijoActual.siguiente

            return self.consumo + potenciaHijos



def load_casas(filename, container):
    with open('data/' + filename, 'r') as csvfile:
        file = csv.reader(csvfile)
        next(file, None)  # skip the first line as it contains headers
        for row in file:
            [id, sistema, provincia, comuna, consumo] = row
            newItem = Casa(id, sistema, provincia, comuna, consumo)
            container.append(newItem)


casas = []
load_casas("casas.csv", casas)
#for casa in casas:
#    print(casa)
#
# # Esta es una red como aparece en el enunciado.
# red = Red()
#
# gen1 = Generadora(1, "nombre", "sistema", "provincia", "comuna", "hidro", 75)
# gen2 = Generadora(2, "nombre", "sistema", "provincia", "comuna", "hidro", 75)
#
# ele1 = Elevadora(3, "nombre", "sistema", "provincia", "comuna", 80)
#
# trans1 = Transmision(4, "nombre", "sistema", "provincia", "comuna", 20)
# trans2 = Transmision(5, "nombre", "sistema", "provincia", "comuna", 20)
#
# distr1 = Distribucion(6, "nombre", "sistema", "provincia", "comuna", 20)
# distr2 = Distribucion(7, "nombre", "sistema", "provincia", "comuna", 20)
#
# casa1 = Casa(8, "sistema", "provincia", "comuna", 10)
# casa2 = Casa(9, "sistema", "provincia", "comuna", 10)
# casa3 = Casa(10, "sistema", "provincia", "comuna", 10)
#
# casa4 = Casa(11, "sistema", "provincia", "comuna", 20)
# casa5 = Casa(12, "sistema", "provincia", "comuna", 15)
# casa6 = Casa(13, "sistema", "provincia", "comuna", 15)
#
# ####
#
# red.agregar(gen1)
# red.agregar(gen2)
#
# gen1.agregar(ele1, 10)
# gen2.agregar(ele1, 25)
#
# ele1.agregar(trans1, 10)
# ele1.agregar(trans2, 5)
#
# trans1.agregar(distr1, 23)
# trans2.agregar(distr2, 10)
#
# distr1.agregar(casa1, 10)
# distr1.agregar(casa2, 10)
#
# distr2.agregar(casa4, 15)
# distr2.agregar(casa5, 50)
#
# casa1.agregar(casa3, 10)
# casa2.agregar(casa3, 15)
#
# casa4.agregar(casa6, 10)
# casa5.agregar(casa6, 5)
#
# print(red.demandaTotal())
# print(ele1.demanda())
#
# print(casa6.demanda())
#
# print(red.distribuir())
