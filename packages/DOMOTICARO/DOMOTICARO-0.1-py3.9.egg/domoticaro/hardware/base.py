#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# clase base para implementar una capa de abstracción sobre el hardware posible
# para DOMOTICARO
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


class BASE_HARDWARE(object):
    """Docstring for BASE_HARDWARE. """

    def __init__(self, puerto="cdc"):
        """ Docstring para __init__
        inicia el puerto de comunicación serial e implementa una capa de
        abstracción para seleccionar el tipo de comunicación entre el hardware
        y PYTHON.
        por defecto inicia con el puerto CDC.

        """
        # print ("inicio la placa 18f4550")
        # esto es medio raro, habria que ver como mejorar, sobre todo si
        # queremos habilitar la placa con otro puerto
        if puerto == "apicaro":
            from .serie import CDC
            print("inicio el hardware con puerto CDC")
            self.__comunicacion = CDC()
        elif puerto == "arduino":
            from .serie_arduino import CDC
            self.__comunicacion = CDC()
        elif puerto == "weemos":
            from .html_weemos import HTML
            self.__comunicacion = HTML()
        else:
            print("error de puerto seleccionado")
            print("se usara el emulador")

    def iniciar(self, puerto="/dev/ttyACM0"):
        """TODO: Docstring for iniciar.
        :returns: TODO

        """
        self.__comunicacion.puerto(puerto)
        return self.__comunicacion.iniciar()

    def puerto(self, arg1):
        """TODO: Docstring for puerto.

        :arg1: TODO
        :returns: TODO

        """
        return self.__comunicacion.puerto(arg1)

    def cerrar(self):
        """TODO: Docstring for cerrar.
        :returns: TODO

        """
        return self.__comunicacion.cerrar()

    def _enviar(self, arg1):
        """TODO: Docstring for _enviar.

        :arg1: TODO
        :returns: TODO

        """
        return self.__comunicacion.enviar(arg1)
