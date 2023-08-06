#!/usr/bin/env python3

###############################################################################
# telegram_api
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

import json 
import requests


class TELEGRAM(object):

    """Docstring for TELEGRAM. """

    def __init__(self, token):
        """TODO: to be defined. """ 
        self._TOKEN = token
        self._URL = "https://api.telegram.org/bot{}/".format(self._TOKEN)
        self.__tipos_msg = ["forward_from",
                            "forward_from_chat",
                            "forward_from_message_id",
                            "forward_signature",
                            "forward_sender_name",
                            "reply_to_message",
                            "edit_date",
                            "media_group_id",
                            "author_signature", 
                            "text", 	
                            "entities",
                            "caption_entities",
                            "audio",
                            "document",
                            "animation",
                            "game",
                            "photo",
                            "sticker",
                            "video",
                            "voice",
                            "video_note",
                            "caption",
                            "contact",
                            "location",
                            "venue",
                            "poll",
                            "new_chat_members",
                            "left_chat_member",
                            "new_chat_title",
                            "new_chat_photo",
                            "delete_chat_photo",
                            "group_chat_created",
                            "supergroup_chat_created",
                            "channel_chat_created",
                            "migrate_to_chat_id",
                            "migrate_from_chat_id",
                            "pinned_message",
                            "invoice",
                            "successful_payment",
                            "connected_website",
                            "passport_data",
                            "reply_markup"]
        # el numero total de mensajes
        self._num_act = self.__ultimo_msg()

    def hay_mensajes(self):
        """TODO: Docstring for hay_mensajes.
        :returns: TODO

        """
        num = self.__ultimo_msg()
        if num > self._num_act:
            self._num_act = num
            return True
        else:
            return False

    def __ultimo_msg(self):
        """TODO: Docstring for ultimo_msg.
        :returns: TODO

        """
        act = self.actualizar()
        num_act = len(act["result"])
        return num_act

    def __obtener_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def __obtener_json_desde_url(self, url):
        content = self.__obtener_url(url)
        js = json.loads(content)
        return js

    def actualizar(self):
        url = self._URL + "getUpdates"
        js = self.__obtener_json_desde_url(url)
        return js

    def tipo_msg(self):
        act = self.actualizar()
        ultima_act = self._num_act - 1
        text = act["result"][ultima_act]["message"]
        tipo_msg = list(text.keys())
        return tipo_msg[4]

    def obtener_ultimo_mensaje(self):
        act = self.actualizar()
        ultima_act = self._num_act - 1
        text = act["result"][ultima_act]["message"]
        tipo_msg = list(text.keys())
        text = act["result"][ultima_act]["message"][tipo_msg[4]]

        chat_id = act["result"][ultima_act]["message"]["chat"]["id"]
        return (chat_id, text)

    def enviar_mensaje(self, chat_id, texto):
        url = self._URL + \
              "sendMessage?text={}&chat_id={}".format(texto, chat_id)
        self.__obtener_url(url)
        return True

    def enviar_imagen(self, chat_id, arch):
        """TODO: Docstring for enviar_imagen.
        :returns: TODO

        """
        url = self._URL + "sendPhoto"
        try:
            requests.post(url,
                          data={"chat_id": chat_id},
                          files={'photo': open(arch, 'rb')}
                          ) 
        except Exception as e:
            # raise e
            print(e)
            return False
        return True

