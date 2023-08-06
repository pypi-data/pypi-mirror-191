#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# base para el sensor analogico
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


class ANALOGICO(object):

    """Docstring for ANALOGICO. """
    def __init__(self, puerto, base):
        """TODO: to be defined1. """
        self._puerto = puerto
        self.__enviar = base

    def leer(self):
        """TODO: Docstring for leer.
        :returns: TODO

        """
        valor = self.__enviar("a"+str(self._puerto))
        try:
            valor = float(valor)
        except Exception as e:
            print(e)
            valor = "None"
        return valor
