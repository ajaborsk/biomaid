#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import json

# import time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.apps import apps


def recursive_dict_set(key_path, value):
    if len(key_path) == 1:
        return {key_path[0]: value}
    else:
        return {key_path[0]: recursive_dict_set(key_path[1:], value)}


class UserSettings:
    def __init__(self, user):
        self.__user = user
        self.__settings = None
        self.__touched = False
        self.__settings_defs = apps.get_app_config('common').user_settings

    def __load_settings(self):
        self.__settings = json.loads(self.__user.preferences)

    def _save_settings(self):
        if self.__touched:
            self.__user.preferences = json.dumps(self.__settings)
            self.__user.save(update_fields=['preferences', 'date_modification'])
        else:
            # Ignore silently or raise a warning ?
            pass

    def __getitem__(self, key):
        if self.__settings is None:
            self.__load_settings()

        key_path = key.split('.')
        s = self.__settings
        while key_path[0] in s:
            if len(key_path) == 1:
                # print(f"Settings: {key_path[0]} {repr(s[key_path[0]])}")
                return s[key_path[0]]
            else:
                s = s[key_path[0]]
                key_path = key_path[1:]
        return self.__settings_defs[key].get('default')

    def __setitem__(self, key, value):
        if self.__settings is None:
            self.__load_settings()

        key_path = key.split('.')
        s = self.__settings
        found = False
        while key_path[0] in s:
            if len(key_path) == 1:
                s[key_path[0]] = value
                found = True
                break
            else:
                s = s[key_path[0]]
                key_path = key_path[1:]
        if not found:
            if len(key_path) == 1:
                s[key_path[0]] = value
            else:
                s[key_path[0]] = recursive_dict_set(key_path[1:], value)
        self.__touched = True

    def __delitem__(self, key):
        if self.__settings is None:
            self.__load_settings()

        key_path = key.split('.')
        s = self.__settings
        while key_path[0] in s:
            if len(key_path) == 1:
                del s[key_path[0]]
                self.__touched = True
                break
            else:
                s = s[key_path[0]]
                key_path = key_path[1:]

    # def __getattr__(self, key):
    #     if self._settings is None:
    #         self.load_settings()
    #     return self._settings.__getattr__(key)
    #
    # def __setattr__(self, key, value):
    #     if self._settings is None:
    #         self.load_settings()
    #     self._settings.__setattr__(key, value)
    #     self.save_settings()
    #
    # def __delattr__(self, key):
    #     if self._settings is None:
    #         self.load_settings()
    #     self._settings.__delattr__(key)
    #     self.save_settings()

    def __len__(self):
        if self.__settings is None:
            self.__load_settings()
        return len(self.__settings)

    def __repr__(self):
        if self.__settings is None:
            self.__load_settings()
        return repr(self.__settings)

    def __iter__(self):
        if self.__settings is None:
            self.__load_settings()
        return iter(self.__settings)


def get_user_settings(user, keys):
    response = {}
    # timer = time.time()

    if user.is_anonymous:
        settings = dict()
    else:
        settings = json.loads(user.preferences)

    if isinstance(keys, str):
        keys = [keys]

    for key in keys:
        response[key] = apps.get_app_config('common').user_settings.get(key, {}).get('default')
        key_path = key.split('.')
        s = settings
        while key_path[0] in s:
            if len(key_path) == 1:
                response[key] = s[key_path[0]]
                break
            else:
                s = s[key_path[0]]
                key_path = key_path[1:]

    # timer = time.time() - timer
    # print("Get user settings took:", timer*1000, "ms")
    # print("get settings", key, response)
    return response


def set_user_settings(user, settings):

    user_settings = json.loads(user.preferences)

    for sname, setting in settings.items():
        key_path = sname.split('.')
        s = user_settings
        found = False
        while key_path[0] in s:
            if len(key_path) == 1:
                s[key_path[0]] = setting
                found = True
                break
            else:
                s = s[key_path[0]]
                key_path = key_path[1:]
        if not found:
            if len(key_path) == 1:
                s[key_path[0]] = setting
            else:
                s[key_path[0]] = recursive_dict_set(key_path[1:], setting)

        # print("Set", s)
    # print("Tout", user_settings)
    user.preferences = json.dumps(user_settings)
    user.save(update_fields=['preferences', 'date_modification'])


class ApiUserSettingsView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        # print("Getting settings for:", request.user, request.GET['keys'])
        if 'keys' in request.GET:
            return JsonResponse(get_user_settings(request.user, json.loads(request.GET['keys'])))
        else:
            return JsonResponse({'error': 'no keys provided'})

    def post(self, request, **kwargs):
        settings = json.loads(request.POST['settings'])
        # print("Setting user settings:", request.user, settings)
        set_user_settings(request.user, settings)
        return JsonResponse({'done': True})
