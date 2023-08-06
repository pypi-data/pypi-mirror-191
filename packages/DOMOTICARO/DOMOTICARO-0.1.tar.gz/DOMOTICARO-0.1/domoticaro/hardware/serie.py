#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# wrapper para integrar el puerto serie (/dev/ttyACM) mediante usb CDC
# Copyright © 2019 Valentín Basel <valentinbasel@gmail.com>
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

import serial
import serial.tools.list_ports


class CDC(object):

    """ docstring clase CDC

    interface de conexión serial USB_CDC para el proyecto de domotica
    DOMOTICARO.
    Implementa una capa de abstracción que permite conectar puerto CDC al
    hardware ICARO o ARDUINO,
    es una API para poder interactuar con el firmware DOMOTICARO_V1.
    su funcion es la de preparar el puerto /devttyUSB o ttyACM para enviar
    y recibir datos.
    una ves inicializada la clase, hay que tener en cuenta lo siguiente:
    el metodo self.puerto es donde se carga el valor del dispositivo serie.
    por defecto es /dev/ttyACM0. cambiarla antes de usar la funcion iniciar()
    """
    _PUERTO = '/dev/ttyACM0'  # valor inicial por defecto
    _BAUDIOS = 9600
    _BYTESIZE = 8
    _PARITY = 'N'
    _STOPBIT = 1
    _TIMEOUT = None
    _XONXOFF = True
    _RTSCTS = True
    _DSRDTR = True
    _RS232 = serial.Serial()

    def __init__(self):
        """TODO: to be defined1. """
        pass

    def puerto(self, arg1):
        """TODO: Docstring for puerto.

        :arg1: String con la dirección del puerto /dev/ttyACM para CDC
        :returns: True / False

        """
        self._PUERTO = arg1

    def iniciar(self):
        """TODO: Docstring for iniciar.

        :arg1: TODO
        :returns: TODO

        """
        self._RS232.port = self._PUERTO
        self._RS232.baudrate = self._BAUDIOS
        self._RS232.bytesize = self._BYTESIZE
        self._RS232.parity = self._PARITY
        self._RS232.stopbit = self._STOPBIT
        self._RS232.timeout = self._TIMEOUT
        self._RS232.xonxoff = self._XONXOFF
        self._RS232.rtscts = self._RTSCTS
        self._RS232.dsrdtr = self._DSRDTR
        self._RS232.exclusive = True
        try:
            self._RS232.open()
            print("iniciar la placa en el puerto :", self._PUERTO)
            return True
        except Exception as e:
            raise e
            return False

    def cerrar(self):
        """TODO: Docstring for cerrar.

        :arg1: TODO
        :returns: TODO

        """
        try:
            self._RS232.close()
            return True
        except:
            return False


    def enviar(self, cadena_caracter):
        """TODO: Docstring for enviar.

        :arg1: TODO
        :returns: TODO

        """
        buff=''
        buff2=""
        if self._RS232.isOpen():
            try:
                for caracter in cadena_caracter:
                    self._RS232.write(caracter.encode("ascii"))
                    #time.sleep(0.01)

                
                while buff != b'\n':
                    buff = self._RS232.read()#self._RS232.inWaiting())
                    buff2 = buff2 + buff.decode("ascii") 
                    #print (buff2)
                #self._RS232.flush()
                return buff2
            except Exception as e:
                print(e)
                print("no se pudo completar el envio de datos")
                return False 
        else:
            print("el puerto: ",self._PUERTO, " esta cerrado")
            return False

