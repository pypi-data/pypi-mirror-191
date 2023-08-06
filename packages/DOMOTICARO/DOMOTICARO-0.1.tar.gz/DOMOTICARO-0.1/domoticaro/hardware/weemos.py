#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# interface de abstracción para el hardware basado en micro controladores 
# 18F4550 con bootloader pinguino V4.0
#
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
from .base import BASE_HARDWARE
from .relay import RELE
from .analogico import ANALOGICO
from .temperatura import TEMPERATURA
from .humedad import HUMEDAD


class ESP12F(BASE_HARDWARE):

    """Docstring for ESP12F.
    La clase ESP12F es una capa de abstracción diseñada para poder usar
    de forma transparente la comunicación entre python y la placa WEEMOS
    basada en el micro controlador ESP12F.
    hereda de la clase BASE_HARDWARE los metodos para la comunicación GET 

    los metodos heredados de BASE_HARDWARE:

    self.iniciar()
    self.cerrar()
    """
    def __init__(self, puerto):
        print("inicio 18f4550")
        BASE_HARDWARE.__init__(self, puerto)
        self.rele1 = RELE(1, self._enviar)
        self.rele2 = RELE(2, self._enviar)
        self.analogico = ANALOGICO(0, self._enviar)
        self.humedad = HUMEDAD(self._enviar)
        self.temperatura = TEMPERATURA(self._enviar)
