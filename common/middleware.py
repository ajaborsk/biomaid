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
import time
import logging
from collections import Counter

import django
from django.db import connection
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.utils.timezone import now

from common.db_utils import server_ready

logger = logging.getLogger(__name__)


class SetLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            request.user.last_seen = now()
            request.user.save(update_fields=('last_seen', 'date_modification'))

        return response


class QueryLogger:
    def __init__(self):
        self.queries = []

    def __call__(self, execute, sql, params, many, context):
        current_query = {
            'sql': sql,
            'params': params,
            'many': many,
            'type': sql.split(maxsplit=1)[0].lower(),
        }
        start = time.monotonic()
        try:
            result = execute(sql, params, many, context)
        except Exception as e:
            current_query['status'] = 'error'
            current_query['exception'] = e
            raise
        else:
            current_query['status'] = 'ok'
            return result
        finally:
            duration = time.monotonic() - start
            current_query['duration'] = duration
            self.queries.append(current_query)


class LoggingMiddleware:
    def __init__(self, get_response, redirect_url='/geqip-chuap/common/no_ie/'):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.redirect_url = redirect_url

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # debug("log for", request.user)

        if "Trident" in request.META["HTTP_USER_AGENT"] and request.path_info != self.redirect_url:
            return redirect(self.redirect_url)

        timer = time.monotonic()
        self.ql = QueryLogger()

        with connection.execute_wrapper(self.ql):
            response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if len(self.ql.queries):
            logger.info(
                _("{} a fait {} requêtes SQL ; répartition : {} ; temps total pour le calcul de la vue: {:.1f}ms").format(
                    request.user,
                    len(self.ql.queries),
                    dict(Counter([query['type'] for query in self.ql.queries])),
                    (time.monotonic() - timer) * 1000,
                )
            )

        for query in self.ql.queries:
            if query['type'] != 'select':
                logger.info(str(query['sql']) + repr(query['params']))

        return response


class StartupMiddleware:
    """
    This middleware is a trick to trigger app hooks exactly once at django launch when the application is FULLY initialized
    These hooks are NOT triggered on every manage.py command but ONLY at server startup
    """

    def __init__(self, get_response):
        self.get_response = get_response
        server_ready()
        raise django.core.exceptions.MiddlewareNotUsed

    def __call__(self, request):
        response = self.get_response(request)
        return response
