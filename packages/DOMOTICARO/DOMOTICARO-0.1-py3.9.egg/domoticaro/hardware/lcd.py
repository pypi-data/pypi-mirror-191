#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# clase para controlar la pantalla LCD
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

class LCD(object):

    """Docstring for LCD. 
        LCD permite comunicar al hardware, a traves del protocolo I2C del 
        hardware, datos de python en la pantallita LCD del hardware.

    """
    def __init__(self,base):
        """
        base = clase BASE para poder implementar el envio de datos a la placa. 
        """
        self.__enviar = base

    def escribir(self, arg1):
        """TODO: Docstring for escribir.

        :arg1: Cadena de texto (string) con la información para enviar al lcd 
        :returns: None

        """
        cadena = "l"+str(arg1)+"\n"
        self.__enviar(cadena)

    def borrar(self):
        """TODO: Docstring for borrar.
        Envia el caracter 'L' para borrar la pantalla del lcd  
        :returns: None

        """
        self.__enviar("L")

