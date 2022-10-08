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
from django import template
from django.template import TemplateSyntaxError
from django.template import Variable

from django.template.base import VariableDoesNotExist
from django.template.defaulttags import Node
from django.utils.html import conditional_escape

register = template.Library()


class URLKwargsNode(Node):
    def __init__(self, view_name, kwargs_name=None, asvar=None):
        self.view_name = view_name
        self.kwargs_name = kwargs_name
        self.asvar = asvar

    def render(self, context):
        from django.urls import NoReverseMatch, reverse

        kwargs = {}

        if 'url_prefix' in context and context['url_prefix']:
            kwargs.update({'url_prefix': context['url_prefix']})

        try:
            if self.kwargs_name is not None:
                kwargs.update(self.kwargs_name.resolve(context))
        except VariableDoesNotExist:
            pass

        view_name = self.view_name.resolve(context)
        try:
            current_app = context.request.current_app
        except AttributeError:
            try:
                current_app = context.request.resolver_match.namespace
            except AttributeError:
                current_app = None
        # Try to look up the URL. If it fails, raise NoReverseMatch unless the
        # {% url ... as var %} construct is used, in which case return nothing.
        url = ''
        try:
            url = reverse(view_name, kwargs=kwargs, current_app=current_app)
        except NoReverseMatch:
            # print('reverse kwargs', view_name, kwargs)
            if self.asvar is None:
                raise

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            if context.autoescape:
                url = conditional_escape(url)
            return url


@register.tag
def url_kwargs(parser, token):
    r"""
    Return an absolute URL matching the given view with its parameters.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% url_kwargs "url_name" kwargs %}

    The first argument is a URL pattern name.

    The second argument is a dictionary-like keyword arguments

    For example, if you have a view ``app_name.views.client_details`` taking
    the client's id and the corresponding line in a URLconf looks like this::

        path('client/<int:id>/', views.client_details, name='client-detail-view')

    and this app's URLconf is included into the project's URLconf under some
    path::

        path('clients/', include('app_name.urls'))

    then in a template you can create a link for a certain client like this::

        {% url "client-detail-view" client.id %}

    The URL will look like ``/clients/client/123/``.

    The first argument may also be the name of a template variable that will be
    evaluated to obtain the view name or the URL name, e.g.::

        {% with url_name="client-detail-view" %}
        {% url url_name client.id %}
        {% endwith %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument, a URL pattern name." % bits[0])
    viewname = parser.compile_filter(bits[1])
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits) == 0:
        kwargs_name = None
    elif len(bits) == 1:
        kwargs_name = Variable(bits[0])
    else:
        raise TemplateSyntaxError("Malformed arguments to url_kwargs tag (more than one argument)")

    return URLKwargsNode(viewname, kwargs_name, asvar)
