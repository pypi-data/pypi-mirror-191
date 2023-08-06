#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# Clase TELEGRAMBOT como capa de abstracción para domoticaro
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
from .telegram_api import TELEGRAM
from .emulador import EMULADOR


class BOT(object):

    """La clase BOT proporciona una capa de abstracción que permite tener
        varios formatos de comunicación (telegram, irc, off-line)"""

    def __init__(self, tipo, arg=None):
        if tipo == "telegram":
            self.__chatbot = TELEGRAM(arg)
        elif tipo == "emulador":
            self.__chatbot = EMULADOR(arg)
        else:
            print(f'error, el valor {tipo} no es un tipo reconocido')
            exit(1)

    def actualizar(self):
        flag = self.__chatbot.actualizar()
        return flag

    def enviar_texto(self,  chat_id, texto):
        flag = self.__chatbot.enviar_mensaje(chat_id, texto)
        return flag

    def enviar_imagen(self, chat_id, arch):
        """TODO: Docstring for enviar_imagen.
        :returns: TODO

        """
        flag = self.__chatbot.enviar_imagen(chat_id, arch)
        return flag

    def hay_mensaje(self):
        flag = self.__chatbot.hay_mensajes()
        return flag

    def recibir_ultimo_mensaje(self):
        chat_id, texto = self.__chatbot.obtener_ultimo_mensaje()
        return (chat_id, texto)
