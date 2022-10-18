#  Copyright (c)

#
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
import colorsys
import json
import re
from abc import ABCMeta, ABC
from copy import deepcopy

import altair
from altair import Chart, Data, Color, Scale
from django.forms.widgets import MediaDefiningClass, Media
from django.http import JsonResponse
from django.template import Context, Engine
from django.utils.translation import gettext as _

from common.base_views import BiomAidViewMixinMetaclass


def media_property(cls):
    def _media(self):

        # print("Container Media...", cls)
        # print(f"  self.Media: {self.Media} {dir(self.Media)}")

        # Get the media property of the superclass, if it exists
        sup_cls = super(cls, self)
        try:
            base = sup_cls.media
        except AttributeError:
            base = Media()

        # Get the media definition for this class
        definition = getattr(cls, "Media", None)
        if definition:
            extend = getattr(definition, "extend", True)
            if extend:
                if extend is True:
                    m = base
                else:
                    m = Media()
                    for medium in extend:
                        m = m + base[medium]
                base = m + Media(definition)
            else:
                base = Media(definition)

        try:
            for child in self.children:
                base = base + child.media
        except AttributeError:
            pass

        # print(f"base: {repr(base)}")
        return base

    return property(_media)


# Useless metaclass (for now), just for tests
class WidgetPageMetaClass(BiomAidViewMixinMetaclass):
    def __new__(mcs: type, name: str, bases: tuple, attrs: dict):

        inherited_attrs = {
            'main_widget': None,
        }

        if len(bases) == 1:
            for base in reversed(bases[0].__mro__):
                for attrname in inherited_attrs.keys():
                    if attrname in base.__dict__:
                        inherited_attrs[attrname] = base.__dict__[attrname]
        else:
            NotImplementedError("Multiple heritance non implemented yet for WidgetPage")

        attrs.update(inherited_attrs)

        new_class = super().__new__(mcs, name, bases, attrs)
        # print(">"*10, f"Creating WidgetPage class {name}")
        # print(">"*10, f"Creating WidgetPage class   {bases}, {bases}")
        # print(">"*10, f"Creating WidgetPage class   {attrs}")
        # print(">"*10, f"Creating WidgetPage class   {inherited_attrs}")
        return new_class


class HtmlMediaDefiningClass(MediaDefiningClass, ABCMeta):
    """
    Metaclass for HtmlWidget.
    """

    def __new__(mcs, name, bases, attrs):
        params_set = set()
        _template_mapping = dict()
        if len(bases) == 1:
            for base_dict in list(b.__dict__ for b in reversed(bases[0].__mro__)) + [attrs]:
                # print(f"base: {base}")
                if 'PARAMS_ADD' in base_dict:
                    # print(f"  params: {base.__dict__['PARAMS']}")
                    params_set.update(set(base_dict['PARAMS_ADD']))
                if '_template_mapping' in base_dict:
                    _template_mapping = base_dict['_template_mapping'].copy()
                if '_template_mapping_add' in base_dict:
                    _template_mapping.update(base_dict['_template_mapping_add'])
                if '_template_mapping_del' in base_dict:
                    for k in base_dict['_template_mapping_del']:
                        del _template_mapping[k]

            # print(f"params_set: {params_set}")
            attrs['PARAMS'] = deepcopy(params_set)
            # print(f"{name}._template_mapping: {_template_mapping}")
            attrs['_template_mapping'] = deepcopy(_template_mapping)

            new_class = super().__new__(mcs, name, bases, attrs)

            if "media" not in attrs:
                new_class.media = media_property(new_class)

            # Do not check this (but this should be done for some HtmlWidgets... :-( )
            # if name != 'HtmlWidget' and new_class.template_string is None and new_class.template_name is None:
            #     raise RuntimeError(
            #         _("Widget Class {} must have either a template_string or a template_name attribute").format(name)
            #     )

            return new_class
        else:
            NotImplementedError("Multiple heritance non implemented yet for WidgetPage")


class HtmlWidget(ABC, metaclass=HtmlMediaDefiningClass):
    """
    Main (abstract) parent class for HtmlWidgets classes
    """

    @classmethod
    def _factory(cls, **attrs):
        # print(f"factory {cls}")
        # print(f"  factory {cls.__dict__}")
        # Small hacking name
        if '_HtmlWidget__factorized_count' in cls.__dict__:
            # print(f"  before/__factorized_count {cls.__factorized_count}")
            cls.__factorized_count += 1
        else:
            cls.__factorized_count = 1
        # print(f"   after/__factorized_count {cls.__factorized_count}")
        return type(cls.__name__ + str(cls.__factorized_count), (cls,), attrs)

    PARAMS_ADD = ('template_string', 'template_name')

    template_string = ""
    template_name = None
    _template_mapping = {
        'html_id': lambda self, kwargs: self.html_id,
    }

    def __init__(self, html_id=None, params=None):
        self.params = params or {}
        self.html_id = html_id or re.sub(r'(?<!^)(?=[A-Z])', '_', self.__class__.__name__).lower()
        self.template = None

        # print('Widget __init__...')

        # Used only for direct instanciate-then-setup instanciation
        if self.params:
            self.setup(**self.params)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Widget get method not overloaded'})

    def params_process(self):
        pass

    def setup(self, **params):
        self.params.update(params or {})

        self.params_process()

        # print('Widget setup...')

        engine = Engine.get_default()
        if self.template_string:
            self.template = engine.from_string(self.template_string)
            # Small hack to give a name to the template (helps debug)
            self.template.name = self.__class__.__name__
        elif self.template_name:
            self.template = engine.get_template(self.template_name)
        else:
            self.template = engine.from_string(_("-- Undefined Template --"))

    def _get_context_data(self, **kwargs):
        context = Context()
        for k, v in self._template_mapping.items():
            if callable(v):
                context[k] = v(self, kwargs)
            elif isinstance(v, str):
                context[k] = self.params[v]
            else:
                context[k] = v
        return context

    def _as_html(self, html_only=False):
        context = self._get_context_data()
        context['html_only'] = html_only
        return self.template.render(context)

    def __str__(self):
        return self._as_html()


class ContainerWidget(HtmlWidget):
    class Media:
        js = ['container_w.js']

    PARAMS_ADD = ('base_children',)

    base_children = tuple()

    @property
    def children(self):
        return self._children

    def __init__(self, html_id=None, params=None):
        super().__init__(html_id=html_id, params=None)
        self._children = [base_child(html_id=self.html_id + '-' + str(c)) for c, base_child in enumerate(self.base_children)]
        if params:
            self.setup(**params)

    def _add_child(self, child):
        self._children.append(child)
        return child

    def setup(self, **params):
        super().setup(**params)
        if 'children' in params:
            self._children = params['children']
        for child in self.children:
            child.setup(**self.params)

    def _get_context_data(self, **kwargs):
        context = super()._get_context_data(**kwargs)
        context['children'] = self._children
        return context


class GridWidget(ContainerWidget):
    class Media:
        css = {'all': ['grid-widget.css']}

    template_string = (
        '<div id="{{ html_id }}" class="grid-widget" '
        'style="display:grid;width:80%;margin:20px 10%;grid-gap:10px;'
        'align-items:center;justify-items:center;grid-template-columns:repeat(5, 1fr);">'
        '{% for child in children %}{{ child }}{% endfor %}</div>'
    )
    base_columns = 1

    def setup(self, **params):
        if 'columns' in params:
            self.base_columns = params['columns']
        super().setup(**params)

    def _get_context_data(self, **kwargs):
        context = super()._get_context_data(**kwargs)
        context['columns_style'] = ' '.join(self.base_columns * [str(100 / self.base_columns) + '%'])
        return context


class SimpleValueWidget(GridWidget):
    pass


class TableWidget(GridWidget):
    column_titles = []
    row_titles = []
    cells = [[]]

    def setup(self, **params):
        super().setup(**params)


class SimpleTextWidget(HtmlWidget):
    template_string = (
        '<div id="{{ html_id }}" style="'
        'text-align:{{ text_align }};font-size:{{ font_size }}px;display:flex;'
        'flex-direction:column;width:100%;height:100%;justify-content:space-evenly;'
        '"><div style="color:{{ text_color }}">{{ text | safe}}</div></div>'
    )
    PARAMS_ADD = ('text_align', 'font_size', 'text_color')
    _template_mapping_add = {
        'text': 'text',
        'text_align': 'text_align',
        'text_color': 'text_color',
        'font_size': 'font_size',
    }

    label = _("Texte libre")
    help_text = _("Simple texte statique")
    manual_params = {
        'text': {'label': 'Texte'},
        'font_size': {'label': 'Taille du texte', 'type': 'int'},
        'flag': {'label': "Drapeau", 'type': 'boolean'},
        'text_color': {'label': "Couleur du texte", 'type': 'color'},
    }

    default_text = ''
    default_size = 16
    default_align = 'center'
    default_color = '#000'

    def params_process(self):
        super().params_process()
        self.params['text'] = self.params.get('text', self.default_text)
        self.params['text_align'] = str(self.params.get('text_align', self.default_align))
        self.params['font_size'] = str(self.params.get('font_size', self.default_size))
        self.params['text_color'] = str(self.params.get('text_color', self.default_color))

    # def _get_context_data(self, **kwargs):
    # context = super()._get_context_data(**kwargs)
    # context['text'] = self.params['text']
    # context['text_align'] = self.params['text_align']
    # context['font_size'] = self.params['font_size']
    # return context


class AltairWidget(HtmlWidget):
    class Media:
        js = [
            'smart_view/js/vega@5.min.js',
            'smart_view/js/vega-lite@4.min.js',
            'smart_view/js/vega-embed@6.min.js',
        ]
        css = {'all': 'smart_view/css/vega-widget.css'}

    # height = 500
    template_name = 'smart_view/smart_widget_altair.html'

    @property
    def altair_options(self):
        return {'renderer': 'svg', 'mode': 'vega-lite', 'actions': False, 'tooltip': {'theme': 'dark'}}

    @property
    def altair_data(self):
        return {
            'spec': self.chart.to_dict(),
            'options': self.altair_options,
        }

    def __init__(self, html_id=None, params=None):
        self.chart = None
        super().__init__(html_id=html_id, params=params)

    def setup(self, **params):
        self.chart = self.params.get('chart')
        super().setup(**params)

    def _get_context_data(self, **kwargs):
        context = super()._get_context_data(**kwargs)
        context['options'] = json.dumps(self.altair_options)
        if self.chart:
            context['spec'] = self.chart.to_json()
        else:
            raise RuntimeError(_("A Altair SmartWidget must have a 'chart' parameter"))
        return context


class BasicChartWidget(AltairWidget):
    def setup(self, **params):  # *args, qs=None, category=None, amount=None, **kwargs):
        super().setup(**params)

        qs = self.params.get('qs')
        category = self.params.get('category')
        amount = self.params.get('amount')

        self.chart = (
            Chart(Data(values=list(qs)))
            .encode(
                color=Color(category + ':O', scale=Scale(scheme='Category20')),
                theta=amount + ':Q',
            )
            .mark_arc(innerRadius=100)
            .properties(width='container', height='container')
        )


class BarChartWidget(AltairWidget):
    def setup(self, **params):
        super().setup(**params)

        qs = self.params.get('qs')
        category = self.params.get('category')
        x = self.params.get('x')
        y = self.params.get('y')

        self.chart = (
            Chart(Data(values=list(qs)))
            .encode(
                color=Color(category + ':N', scale=Scale(scheme='Category20')),
                x=x,
                y=y,
            )
            .mark_bar(tooltip=True)
            .properties(width='container', height='container')
        )


class TestBarChartWidget(BarChartWidget):
    def setup(self, **params):
        self.params['x'] = 'xx:N'
        self.params['y'] = 'yy:N'
        self.params['category'] = 'yy:O'
        self.params['qs'] = [{'xx': 1, 'yy': 2}]
        super().setup(**params)


class DemoPieChartWidget(AltairWidget):
    label = _("Démo Camenbert")

    def setup(self, **params):
        super().setup(**params)

        qs = [{'category': k, 'value': v} for k, v in {'a': 4, 'b': 6, 'c': 10, 'd': 3, 'e': 7, 'f': 8}.items()]
        category = 'category:N'
        value = 'value:Q'
        self.chart = (
            Chart(Data(values=qs))
            .encode(
                theta=value,
                color=altair.Color(category, legend=None),
            )
            .mark_arc(tooltip=True)
            .properties(width='container', height='container')
            .configure_view(strokeWidth=0)
        )


class SvgWidget(HtmlWidget):
    pass


class SimpleLightWidget(SvgWidget):
    template_name = 'analytics/led_circle_clip_art.svg'

    COLORS_HS = {
        'red': (0.0, 1.0),
        'green': (0.33, 1.0),
        'yellow': (0.1666, 1.0),
        'orange': (0.09, 1.0),
        'gray': (0.0, 0.0),
    }

    def __init__(self, html_id=None, params=None):
        super().__init__(html_id=html_id, params=params)
        self.suffix = id(self)  # to avoid svg/html id collisions
        self.light_color = '#dfdfdf'
        self.dark_color = '#050505'
        if params:
            self.setup(**params)

    def setup(self, **params):
        super().setup(**params)

        hue = None
        saturation = 1.0
        color = self.params.get('color', 128)

        if isinstance(color, int):
            hue = color / 255.0
        elif isinstance(color, str):
            hue, saturation = self.COLORS_HS.get(color, (None, None))

        if hue is None:
            raise ValueError(
                _("SimpleLightWidget argument must be a integer " "(hue from 0 to 255) or a color name in {}, not {}").format(
                    ', '.join(list(self.COLORS_HS.keys())), color
                )
            )

        self.suffix = id(self)  # to avoid svg/html id collisions
        self.light_color = '#{:02x}{:02x}{:02x}'.format(*(int(v * 255.0) for v in colorsys.hls_to_rgb(hue, 0.9, saturation)))
        self.dark_color = '#{:02x}{:02x}{:02x}'.format(*(int(v * 255.0) for v in colorsys.hls_to_rgb(hue, 0.4, saturation)))

    def _get_context_data(self, **kwargs):
        context = super()._get_context_data(**kwargs)
        context['suffix'] = self.suffix
        context['light_color'] = self.light_color
        context['dark_color'] = self.dark_color
        return context


class LightAndTextWidget(GridWidget):
    base_children = (
        SimpleLightWidget,
        SimpleTextWidget,
    )


class RepartirWidget(LightAndTextWidget):
    def params_process(self):
        self.params['text'] = "A répartir"
        self.params['color'] = 'orange'


class VueWidget(HtmlWidget):
    class Media:
        js = [
            'smart_view/js/vue-2.7.8.min.js',
            'smart_view/js/axios-0.27.2.min.js',
            'smart_view/js/get-coockie.js',
        ]
