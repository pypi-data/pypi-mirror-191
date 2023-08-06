#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
# capa de abstracción para parsear HTML
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
import requests
from lxml import etree


class HTML(object):

    """Docstring for HTML. """

    def __init__(self):
        """TODO: to be defined. """
        self._url = ""
        self._dicc_html = {'REL': '', 'R': '', 'G': '', 'B': ''}

    def puerto(self, arg):
        """
        """
        self._url = arg
        print("este es el puerto seleccionado: ", arg)

    def iniciar(self):
        """TODO: Docstring for iniciar.

        :arg1: TODO
        :returns: TODO

        """
        pass

    def cerrar(self):
        """TODO: Docstring for cerrar.

        :arg1: TODO
        :returns: TODO

        """
        pass

    def enviar(self, arg1):
        """TODO: Docstring for enviar.

        :arg1: TODO
        :returns: TODO

        """
        if arg1 == "t":
            r = requests.get(self._url, params=self._dicc_html)
            dicc = self.parseador_tabla(r.text)
            return dicc["temperatura"]
        if arg1 == "h":
            r = requests.get(self._url, params=self._dicc_html)
            dicc = self.parseador_tabla(r.text)
            return dicc["humedad"]
        if arg1 == "a0":
            r = requests.get(self._url, params=self._dicc_html)
            dicc = self.parseador_tabla(r.text)
            return dicc["Analogico"]
        if arg1[0] == "r":
            if arg1[2] == "1":
                self._dicc_html["REL"] = "ON"+arg1[1]
                r = requests.get(self._url, params=self._dicc_html)
                dicc = self.parseador_tabla(r.text)
                val = "RELE_"+arg1[1]
                return dicc[val]
            if arg1[2] == "0":
                self._dicc_html["REL"] = "OFF"+arg1[1]
                r = requests.get(self._url, params=self._dicc_html)
                dicc = self.parseador_tabla(r.text)
                val = "RELE_"+arg1[1]
                return dicc[val]
            if arg1[2] == "e":
                self._dicc_html["REL"] = ""
                r = requests.get(self._url, params=self._dicc_html)
                dicc = self.parseador_tabla(r.text)
                val = "RELE_" + arg1[1]
                return dicc[val]
        self._dicc_html["REL"] = ""

    def parseador_tabla(self, arg):
        """TODO: Docstring for parseador_tabla.

        :arg: TODO
        :returns: TODO

        """
        table = etree.HTML(arg).find("body/table")
        rows = iter(table)
        valores = []
        dicc_estado = {}
        for row in rows:
            values = [col.text for col in row]
            valores.append(values)
        for dicc in range(1, len(valores)):
            key, valor = valores[dicc]
            if valor == "ON":
                valor = "1"
            if valor == "OFF":
                valor = "0"
            dicc_estado[key] = valor
        return dicc_estado
