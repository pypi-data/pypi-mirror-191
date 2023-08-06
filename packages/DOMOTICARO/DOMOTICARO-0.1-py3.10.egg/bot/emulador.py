#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
# emulador de chatbot para domoticaro
# Copyright © 2020 Valentin Basel <valentinbasel@gmail.com>
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
###############################################################################

import os


class EMULADOR(object):

    def __init__(self, arg=None):
        self.mensajes = []
        self._num_act = 0
        self.chat_id = 1
        self.ruta = os.getenv("HOME") + "/espacio_de_trabajo/emulador/"

    def enviar_imagen(self, chat_id, mens):
        """TODO: Docstring for enviar_imagen.
        :returns: TODO

        """
        mens = "img>> " + mens
        self.enviar_mensaje(chat_id, mens)

    def actualizar(self):
        """TODO: Docstring for actualizar.

        :arg1: TODO
        :returns: TODO

        """
        arch = open(self.ruta + "log1.txt", "r")
        lista_temporal = []
        for dato in arch.readlines():
            lista_temporal.append(dato)
        arch.close()
        self.mensajes = lista_temporal

    def hay_mensajes(self):
        self.actualizar()
        num = len(self.mensajes)
        if num > self._num_act:
            self._num_act = num
            return True
        else:
            return False

    def obtener_ultimo_mensaje(self):
        ultima_act = self._num_act - 1
        mens = self.mensajes[ultima_act]
        chat_id = self.chat_id
        return chat_id, mens

    def enviar_mensaje(self, chat_id, mens):
        # cadena = str(chat_id) + ": " + mens + "\n"
        cadena = "\n" + mens
        arch = open(self.ruta + "log2.txt", "a")
        arch.write(cadena)
        arch.close()
