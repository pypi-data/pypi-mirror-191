#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# wraper de sintesis de voz espeak
# Copyright © 2019 Valentin Basel <valenitnbasel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
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

import subprocess
import re

class VOZ(object):

    """Espeak es una clase para poder implementar un wrapper sencillo que
       permita controlar el programa espeak de los sistemas GNU/linux para
       sintesis de voz por computadora (texto a voz).
       tranforma cualquier cadena de texto en audio.
    """

    def __init__(self,_voz="es",_pitch=100,_velocidad=200):

        """TODO: to be defined1.

        :voz: TODO
        :pitch: TODO
        :velocidad: TODO

        """
        self.args=[
                  ["-v",_voz,str],
                  ["-p",_pitch,int],
                  ["-s",_velocidad,int],
                  ]

    def __ejecutar(self, text):
        """
        metodo privado de la clase para ejecutar mediante subprocess
        el comando espeak con los parametros que se envien.

        :text: cadena de caracteres (string) con el comando espeak a ejecutar
        :returns: True si fue correcto, False si hubo algun error

        """
        cmd = self.__contruir_cmd(text)
        return subprocess.check_output(cmd,
                                       stderr=subprocess.PIPE).decode('UTF8')

    def __contruir_cmd(self, texto):
        """Crea la cadena de caracteres que leera subprocess.

        :texto: texto a insertar en el comando
        :returns: lista con los valores  para ejecutar


        """
        comando_final = ["espeak-ng"]
        for dat in self.args:
            if type(dat[1])==dat[2]:
                comando_final.append(dat[0]+str(dat[1]))
            else:
                print("error")
                return 1
        comando_final.append(texto)
        return comando_final

    def decir(self, texto):
        """TODO: Docstring for decir.

        :texto: cadena de caracteres para traducir a audio
        :returns: True/False

        """
        return self.__ejecutar(str(texto))

    def velocidad(self,v):
        """
        Modifica la velocidad de dicción de Espeak.
        Acepta valores enteros de 10 a 300.
        :v: integer con la velocidad de pronunciacion del texto (10 - 300)
        :returns: True - False

        """
        if type(v)==int:
            if v>=10 and v<=300:
                self.args[2][1]=v
                return True
            else:
                print ("error de valores de velocidad")
                return False
        else:
            print("error, tipo no reconocido. tiene que ser un integer")
            return False

    def pitch(self,v):
        """
        Modifica el tono de dicción de espeak.
        Acepta valores enteros de 0 a 99.
        :v: integer con el timbre de proncunciancion  del texto (0 - 99)
        :returns: True - False

        """
        if type(v)==int:
            if v>0 and v<100:
                self.args[1][1]=v
                return True
            else:
                print ("error de valores del pitch")
                return False
        else:
            print("error, tipo no reconocido. tiene que ser un integer")
            return False
