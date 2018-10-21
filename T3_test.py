# coding=utf-8

"""Tests for the T3 script."""

import unittest

from T3 import Red, Generadora, Elevadora, Transmision, Distribucion, Casa


class ConsultaTest(unittest.TestCase):

    def setUp(self):
        self.red = Red()

        # Comuna = 'comuna'
        gen1 = Generadora(1, "nombre", "sistema", "provincia", "comuna", "hidro", 75)
        gen2 = Generadora(2, "nombre", "sistema", "provincia", "comuna1", "hidro", 75)

        ele1 = Elevadora(3, "nombre", "sistema", "provincia", "comuna", 80)
        ele2 = Elevadora(3, "nombre", "sistema", "provincia", "comuna1", 80)

        trans1 = Transmision(4, "nombre", "sistema", "provincia", "comuna", 20)
        trans2 = Transmision(5, "nombre", "sistema", "provincia", "comuna1", 20)

        distr1 = Distribucion(6, "nombre", "sistema", "provincia", "comuna", 20)
        distr2 = Distribucion(7, "nombre", "sistema", "provincia", "comuna1", 20)

        casa1 = Casa(8, "sistema", "provincia", "comuna", 10)
        casa2 = Casa(9, "sistema", "provincia", "comuna", 10)
        casa3 = Casa(10, "sistema", "provincia", "comuna1", 10)
        casa4 = Casa(11, "sistema", "provincia", "comuna1", 10)

        self.red.agregar(gen1)
        self.red.agregar(gen2)

        gen1.agregar(ele1, 10)
        gen2.agregar(ele1, 25)

        ele1.agregar(trans1, 10)
        ele2.agregar(trans2, 5)

        trans1.agregar(distr1, 23)
        trans2.agregar(distr2, 10)

        distr1.agregar(casa1, 10)
        distr1.agregar(casa2, 10)

        distr2.agregar(casa3, 15)
        distr2.agregar(casa4, 50)

    def testConsumoTotalPorComuna(self):
        self.assertEqual(140, self.red.getConsumoPorComuna('comuna'))
