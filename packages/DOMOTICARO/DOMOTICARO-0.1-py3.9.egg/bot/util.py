#!/usr/bin/env python3
# -*- coding: utf-8 -*-


###############################################################################
# utilerias para chatbot
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

import re
import random


class PARES(object):
    def __init__(self, pairs):
        """
        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second expressions
        :rtype: None
        """

        reflexiones = {
                     "yo soy": " tu eres",
                     "Yo era": " tú eras",
                     "Yo": "tú",
                     "soy": "eres",
                     "mio": "tuyo",
                     "eras": "yo era",
                     "tu": "lo haré",
                     "tuyo": "mío",
                     "usted": "yo",
                     "yo": "tú",
                     "quiero": "queres",
                     "estoy": "estas",
                     "me": "te"
                        }
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflexiones
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))),
            re.IGNORECASE
        )

    def _Comodin(self, response, match):
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1: pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2:]
            )
            pos = response.find("%")
        return response

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start(): mo.end()]],
            str.lower()
        )

    def Respuesta(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._Comodin(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp
