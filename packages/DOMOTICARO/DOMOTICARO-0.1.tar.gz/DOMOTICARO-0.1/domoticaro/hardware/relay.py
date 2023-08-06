#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# objeto Rele
# Copyright © 2019 Valentín Basel <valentinbasel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


class RELE(object):

    """Docstring for RELE.
        La clase RELE implementa los metodos y parametros necesarios para poder
        controlar un relay mecanico.

        A causa de las limitaciones mecanicas de un relay, no es posible usar
        PWM con la señal.

    """

    def __init__(self, puerto, base):
        """
        puerto = el valor del relay (0,1,2,3) que leera la placa.
        base = clase BASE para poder implementar el envio de datos a la placa.
        """
        self._puerto = puerto
        self.__enviar = base

    def on(self):
        """TODO: Docstring for on.
        Prende el Relay
        :returns: 1

        """
        cadena = "r"+str(self._puerto)+"1"
        self.__enviar(cadena)
        return 1

    def off(self):
        """TODO: Docstring for off.
        apaga el Relay
        :returns: 0

        """
        cadena = "r"+str(self._puerto)+"0"
        self.__enviar(cadena)
        return 0

    def estado(self):
        """TODO: Docstring for estado.
        0 = apagado
        1 = encendido
        :returns: 0 - 1 en función del estado descripto por el rele en la placa

        """
        cadena = "r"+str(self._puerto)+"e"
        r = self.__enviar(cadena)
        if r[0] == '0' or r[0] == '1':
            return int(r)
        else:
            return False

    def conmutar(self):
        """TODO: Docstring for conmutar.
        conmuta el estado del rele. Si el estado es 1, se conmutara a 0 y
        viceversa.
        0 = apagado
        1 = encendido
        :returns: 0 - 1 en función del estado descripto por el rele en la placa
        """
        estado = self.estado()
        if estado == 0:
            return self.on()
        if estado == 1:
            return self.off()
        return False
