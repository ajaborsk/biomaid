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
import logging
import re
from abc import ABCMeta, ABC
from copy import deepcopy

from django.urls import reverse
import tomlkit

import altair
from altair import Chart, Data, Color, Scale
from django.forms.widgets import MediaDefiningClass, Media
from django.http import HttpResponse, JsonResponse
from django.template import Context, Engine
from django.utils.translation import gettext as _
from analytics.data import get_data

from common.base_views import BiomAidViewMixinMetaclass
from common.models import Alert, Discipline


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

    def __init__(self, html_id=None, params=None, parent=None, mode='render'):
        self._mode = mode
        self._parent = parent
        self.params = params or {}
        self.html_id = html_id or re.sub(r'(?<!^)(?=[A-Z])', '_', self.__class__.__name__).lower()
        self.template = None

        # Used only for direct instanciate-then-setup instanciation.
        if self.params:
            self._setup(**self.params)

    def _get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Widget _get method not overloaded'})

    def _post(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Widget _post method not overloaded'})

    # def params_process(self):
    #     pass
    #
    def _setup(self, **params):
        self.params.update(params or {})
        # self.params_process()

    def _get_context_data(self, **kwargs):
        context = Context()
        for k, v in self._template_mapping.items():
            if callable(v):
                context[k] = v(self, kwargs)
            elif isinstance(v, str):
                context[k] = self.params.get(v)
            else:
                context[k] = v
        return context

    def _prepare(self):
        """prepare the widget for rendering, based on parameters"""
        pass

    def _as_html(self, html_only=False):
        """Render the widget as HTML. The media (JS, CSS) of the widget must have been loaded in the HTML page header"""
        self._prepare()

        context = self._get_context_data()
        context['html_only'] = html_only

        engine = Engine.get_default()
        if self.template_string:
            self.template = engine.from_string(self.template_string)
            # Small hack to give a name to the template (helps debug)
            self.template.name = self.__class__.__name__
        elif self.template_name:
            self.template = engine.get_template(self.template_name)
        else:
            self.template = engine.from_string(_("-- Undefined Template --"))

        return self.template.render(context)

    def __str__(self):
        return self._as_html()


class ContainerWidget(HtmlWidget):
    PARAMS_ADD = ('base_children',)
    base_children = tuple()

    @property
    def children(self):
        return self._children

    def __init__(self, html_id=None, params=None, parent=None):
        self._children = []
        super().__init__(html_id, params, parent)
        self._children = [base_child(html_id=self.html_id + '-' + str(c)) for c, base_child in enumerate(self.base_children)]
        if params and not parent:
            self._setup(**params)

    def _add_child(self, child_class, html_id_suffix, params=None):
        if isinstance(child_class, type):
            widget = child_class(self.html_id + '-' + html_id_suffix, params=params or {}, parent=self)
            self._children.append(widget)
        else:
            raise RuntimeError
            # self._children.append(child)
        return widget

    def _setup(self, **params):
        super()._setup(**params)
        if 'children' in params:
            self._children = params['children']
        for child in self.children:
            child._setup(**self.params)

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

    def _setup(self, **params):
        if 'columns' in params:
            self.base_columns = params['columns']
        super()._setup(**params)

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


class SimpleTextWidget(HtmlWidget):
    template_string = (
        '<div id="{{ html_id }}" style="'
        'text-align:{{ text_align }};background-color:{{ background_color }};font-size:{{ font_size }}px;display:flex;'
        'flex-direction:column;width:100%;height:100%;justify-content:space-evenly;'
        '"><div style="color:{{ text_color }}">{{ text | safe}}</div></div>'
    )
    PARAMS_ADD = ('text_align', 'font_size', 'text_color')
    _template_mapping_add = {
        'text': 'text',
        'text_align': 'text_align',
        'background_color': 'background_color',
        'text_color': 'text_color',
        'font_size': 'font_size',
    }

    label = _("Texte libre")
    help_text = _("Simple texte statique")
    manual_params = {
        'text': {'label': 'Texte', 'default': ''},
        'font_size': {'label': 'Taille du texte', 'type': 'int', 'default': 16},
        'text_align': {
            'label': 'Alignement horizontal',
            'type': 'choice',
            'choices': [('left', 'Gauche'), ('center', 'Centre'), ('right', 'Droite')],
            'default': 'center',
        },
        'flag': {'label': "Drapeau", 'type': 'boolean', 'default': False},
        'background_color': {'label': "Couleur du fond", 'type': 'color', 'default': '#fff'},
        'text_color': {'label': "Couleur du texte", 'type': 'color', 'default': '#000'},
    }

    default_text = ''
    default_size = 16
    default_align = 'center'
    default_color = '#000'

    def _setup(self, **params):
        super()._setup(**params)
        self.params['text'] = self.params.get('text', self.default_text)
        self.params['text_align'] = str(self.params.get('text_align', self.default_align))
        self.params['font_size'] = str(self.params.get('font_size', self.default_size))
        self.params['background_color'] = str(
            self.params.get('background_color', self.manual_params.get('background_color', {}).get('default'))
        )
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
        css = {
            'all': [
                'smart_view/css/vega-widget.css',
            ],
        }

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

    def _setup(self, **params):
        super()._setup(**params)

    def _prepare(self):
        self.chart = self.params.get('chart')
        super()._prepare()

    def _get_context_data(self, **kwargs):
        context = super()._get_context_data(**kwargs)
        context['options'] = json.dumps(self.altair_options)
        if self.chart:
            context['spec'] = self.chart.to_json()
        else:
            raise RuntimeError(_("A Altair SmartWidget must have a 'chart' parameter"))
        return context


class BasicChartWidget(AltairWidget):
    def _prepare(self):
        qs = self.params.get('qs')
        category = self.params.get('category')
        amount = self.params.get('amount')

        self.params['chart'] = (
            Chart(Data(values=list(qs)))
            .encode(
                color=Color(category + ':O', scale=Scale(scheme='Category20')),
                theta=amount + ':Q',
            )
            .mark_arc(innerRadius=100)
            .properties(width='container', height='container')
        )
        super()._prepare()


class BarChartWidget(AltairWidget):
    def _prepare(self):

        qs = self.params.get('qs')
        category = self.params.get('category')
        x = self.params.get('x')
        y = self.params.get('y')

        self.params['chart'] = (
            Chart(Data(values=list(qs)))
            .encode(
                color=Color(category + ':N', scale=Scale(scheme='Category20')),
                x=x,
                y=y,
            )
            .mark_bar(tooltip=True)
            .properties(width='container', height='container')
        )
        super()._prepare()


class DemoPieChartWidget(AltairWidget):
    label = _("Démo Camenbert")

    def _prepare(self):

        qs = [{'category': k, 'value': v} for k, v in {'a': 4, 'b': 6, 'c': 10, 'd': 3, 'e': 7, 'f': 8}.items()]
        category = 'category:N'
        value = 'value:Q'
        self.params['chart'] = (
            Chart(Data(values=qs))
            .encode(
                theta=value,
                color=altair.Color(category, legend=None),
            )
            .mark_arc(tooltip=True)
            .properties(width='container', height='container')
            .configure_view(strokeWidth=0)
        )
        super()._prepare()


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
            self._setup(**params)

    def _prepare(self):
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
        self.suffix = id(self)
        self.light_color = '#{:02x}{:02x}{:02x}'.format(*(int(v * 255.0) for v in colorsys.hls_to_rgb(hue, 0.9, saturation)))
        self.dark_color = '#{:02x}{:02x}{:02x}'.format(*(int(v * 255.0) for v in colorsys.hls_to_rgb(hue, 0.4, saturation)))
        super()._prepare()

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


class MyAlertsWidget(LightAndTextWidget):
    label = _("Mes alertes")

    def params_process(self):
        qs = Alert.objects.filter(destinataire=self.params['user'], cloture__isnull=True)
        self.params['color'] = 'red'
        self.params['text'] = 'Yop ' + str(qs.count())


class SimpleScalarWidget(HtmlWidget):
    template_string = (
        '<div id="{{ html_id }}" style="'
        'text-align:center;font-size:{{ font_size }}px;display:flex;'
        'flex-direction:column;width:100%;height:100%;justify-content:space-evenly;'
        '"><div style="color:{{ text_color }}">{{ prefix }}&nbsp;{{ scalar }}&nbsp;{{ suffix }}</div></div>'
    )
    PARAMS_ADD = ('font_size', 'text_color', 'scalar', 'prefix', 'suffix')
    _template_mapping_add = {
        'text_color': 'text_color',
        'font_size': 'font_size',
        'prefix': 'prefix',
        'suffix': 'suffix',
        'scalar': 'scalar',
    }

    label = _("Donnée simple")
    help_text = _("Donnée unique (nombre)")
    manual_params = {
        'font_size': {'label': 'Taille du texte', 'type': 'int'},
        'text_color': {'label': "Couleur du texte", 'type': 'color'},
        'prefix': {'label': "Préfixe", 'type': 'string'},
        'suffix': {'label': "Suffixe", 'type': 'string'},
    }

    def _setup(self, **params):
        super()._setup(**params)
        self.params['prefix'] = self.params.get('prefix', '')
        self.params['suffix'] = self.params.get('suffix', '')
        self.params['scalar'] = get_data('common.user-active-alerts', all_params=self.params)


class PrevisionnelParExpertWidget(AltairWidget):
    label = _("Nb prévisionnels par expert")

    @staticmethod
    def manual_params(params):
        return {
            'discipline': {
                'label': "Discipline",
                'type': 'choice',
                'choices': list(Discipline.objects.filter(cloture__isnull=True).values_list('code', 'nom')),
            },
        }

    def _setup(self, **params):
        super()._setup(**params)

        qs = get_data('drachar.previsionnel-par-expert', all_params=self.params)
        category = altair.Color('nom_expert', type='nominal', title="Chargé d'opération")
        value = 'nombre:Q'
        self.params['chart'] = (
            Chart(Data(values=list(qs)))
            .transform_calculate(
                url=reverse('drachar:previsionnel', kwargs={'url_prefix': params['url_prefix']})
                + '?filters=['
                + '{"name":+"expert",+"value":+{"expert":+'
                + altair.datum.expert
                + '}},+{"name":+"solder_ligne",+"value":+{"solder_ligne":+false}}]'
            )
            .encode(theta=value, color=category, href='url:N', tooltip=[category, 'nombre:Q'])
            .mark_arc(tooltip=True)
            .properties(width='container', height='container')
            .configure_view(strokeWidth=0)
        )


class MontantPrevisionnelParExpertWidget(AltairWidget):
    label = _("Montant prévisionnel par expert")

    @staticmethod
    def manual_params(params):
        return {
            'discipline': {
                'label': "Discipline",
                'type': 'choice',
                'choices': list(Discipline.objects.filter(cloture__isnull=True).values_list('code', 'nom')),
            },
        }

    def _setup(self, **params):
        super()._setup(**params)

        qs = get_data('drachar.montant-previsionnel-par-expert', all_params=self.params)
        category = 'nom_expert:N'
        value = 'montant_total:Q'
        self.params['chart'] = (
            Chart(Data(values=list(qs)))
            .encode(
                theta=value,
                color=altair.Color(category),
            )
            .mark_arc(tooltip=True)
            .properties(width='container', height='container')
            .configure_view(strokeWidth=0)
        )


class Vue2Widget(HtmlWidget):
    class Media:
        js = [
            'smart_view/js/vue-2.7.8.min.js',
            'smart_view/js/axios-0.27.2.min.js',
            'smart_view/js/get-coockie.js',
        ]


class VueWidget(HtmlWidget):
    @property
    def media(self):
        return Media(
            js=[
                'https://unpkg.com/vue@3/dist/vue.global.js',
                'https://unpkg.com/vue-router@4/dist/vue-router.global.js',
                'https://unpkg.com/primevue@^3/core/core.min.js',
                'smart_view/js/axios-0.27.2.min.js',
                'common/vue/{}.js'.format(self._vue_widget_name),
            ],
            css={
                'all': [
                    "https://unpkg.com/primevue@^3/resources/themes/saga-blue/theme.css",
                    "https://unpkg.com/primevue@^3/resources/primevue.min.css",
                    "https://unpkg.com/primeflex@^3/primeflex.min.css",
                    "https://unpkg.com/primeicons/primeicons.css",
                ]
            },
        )

    _template_mapping_add = {
        'vue_widget_name': 'vue_widget_name',
        'vue_props': 'vue_props',
        'vue_opts': 'vue_opts',
    }

    template_string = (
        '''{% load json_tags %}<div id="{{ html_id }}"></div>'''
        '''<script>const routes = [{ path: "/", component: {{ vue_widget_name }} }];'''
        '''const router = VueRouter.createRouter({ history: VueRouter.createWebHashHistory(), routes });'''
        '''const {{ html_id }}_app = Vue.createApp({{ vue_widget_name }}, {{ vue_props|to_json }})'''
        '''.use(primevue.config.default, {{ vue_opts|to_json }}).use(router).mount('#{{ html_id }}');'''
        '''</script>'''
    )

    def _setup(self, **params):
        super()._setup(**params)
        self.params['vue_widget_name'] = self._vue_widget_name
        self.params['vue_opts'] = {'ripple': True}
        # self.params['vue_props'] = {'msg': "I did it !", 'html_id': self.params['html_id']}


class DemoWidget(VueWidget):
    _vue_widget_name = 'demo_widget'


class VueCockpit(VueWidget):
    class Media:
        js = [
            'smart_view/js/vega@5.min.js',
            'smart_view/js/vega-lite@4.min.js',
            'smart_view/js/vega-embed@6.min.js',
        ]

    _vue_widget_name = 'cockpit'

    default_grid_layout: list[dict] = []

    categories = {
        'generic': {'label': _("Génériques"), 'help_text': _("Tuiles sans source de données (toujours identiques)")},
        'demo': {'label': _("Démo"), 'help_text': _("Tuiles de démontration")},
        'common': {'label': _("Globaux"), 'help_text': _("Tuiles globales pour toute l'application")},
        'dem': {'label': _("Demandes"), 'help_text': _("Tuiles du module de gestion des demandes")},
        'drachar': {'label': _("DraCHAr"), 'help_text': _("Tuiles du module de suivi plan d'équipement")},
    }

    # Later, these templates could be defined in each module (ie Django application) as alarms, views, models, etc.
    available_tile_templates: dict = {
        'simple_text': {
            'category': 'generic',
            'label': _("Texte"),
            'help_text': _("Widget qui affiche un texte fixe"),
            'w': 3,
            'h': 1,
            'class': SimpleTextWidget,
        },
        'my_alerts': {
            'category': 'common',
            'label': _("Mes alertes"),
            'class': MyAlertsWidget,
        },
        'demo_pie_chart': {
            'category': 'demo',
            'label': _("Camenbert"),
            'class': DemoPieChartWidget,
        },
        'simple_light': {
            'category': 'demo',
            'label': _("Voyant coloré"),
            'class': SimpleLightWidget,
        },
        'light_and_text': {
            'category': 'demo',
            'label': _("Texte et voyant"),
            'class': LightAndTextWidget,
        },
        'a_repartir': {
            'category': 'dem',
            'label': _("Demandes à répartir"),
            'class': RepartirWidget,
        },
        'simple_scalar': {
            'category': 'demo',
            'label': _("Valeur numérique"),
            'class': SimpleScalarWidget,
        },
        'nb_previsionnel_par_expert': {
            'category': 'drachar',
            'label': _("Prévisionnel par expert (qté)"),
            'class': PrevisionnelParExpertWidget,
        },
        'montant_previsionnel_par_expert': {
            'category': 'drachar',
            'label': _("Prévisionnel par expert (€)"),
            'class': MontantPrevisionnelParExpertWidget,
        },
    }

    def __init__(self, *args, **kwargs):
        self.contents = kwargs.pop('contents', None)
        self.config_name = kwargs.pop('config_name', 'cockpit')
        self.user_settings_path = kwargs.pop('user_settings_path', None)

        if not isinstance(self.contents, dict) or 'layout' not in self.contents:
            logging.warning("Using fallback layout for portal home content (not using {}).".format(repr(self.contents)))
            self.contents = {'layout': self.default_grid_layout}

        try:
            for widget in self.contents['layout']:
                if 'w_params' in widget and not isinstance(widget['w_params'], str):
                    # convert w_params to a JSON string (if needed)
                    widget['w_params'] = json.dumps(widget['w_params'])
        except TypeError:
            logging.warning(
                "Using fallback layout for portal home content (layout is not iterable: {}).".format(repr(self.contents['layout']))
            )
            self.contents = {'layout': self.default_grid_layout}

        self.editable = self.contents.get('editable', True)
        self.columns = self.contents.get('columns', 16)
        self.rows = self.contents.get('rows', 32)
        self.v_spacing = self.contents.get('v_spacing', 12)
        self.h_spacing = self.contents.get('h_spacing', 12)
        self.initial_layout = []

        super().__init__(*args, **kwargs)

    def _setup(self, **params):
        super()._setup(**params)
        try:
            self.initial_layout = self.params['user_preferences'][self.user_settings_path]
        except KeyError:
            pass

    def _get_as_toml(self, request, cockpit_name, *args, **kwargs):
        toml_doc = tomlkit.TOMLDocument()
        grid_layout = self.contents['layout']
        if self.editable:
            if not request.GET.get('reset'):
                try:
                    grid_layout = self.params['user_preferences'][self.config_name + '.grid-layout']
                except KeyError:
                    pass
        base_cfg = {}
        cfg = base_cfg
        if not cockpit_name:
            cockpit_name = self.config_name
        while '.' in cockpit_name:
            root, cockpit_name = cockpit_name.split('.', 1)
            cfg[root] = {}
            cfg = cfg[root]
        cfg[cockpit_name] = {
            'layout': deepcopy(grid_layout),
            'rows': self.rows,
            'columns': self.columns,
            'h_spacing': self.h_spacing,
            'v_spacing': self.v_spacing,
        }
        if self.editable:
            cfg[cockpit_name]['editable'] = True
            cfg[cockpit_name]['available_widgets'] = list(self.available_widgets.keys())
        else:
            cfg[cockpit_name]['editable'] = False
        for widget in cfg[cockpit_name]['layout']:
            widget['w_params'] = json.loads(widget['w_params'])
        toml_doc.update(base_cfg)
        return HttpResponse(toml_doc.as_string(), content_type='text/plain; charset=utf-8')

    def _get(self, request, *args, **kwargs):
        """Get the tiles contents"""
        try:
            tiles = json.loads(request.GET['layout'])
        except json.JSONDecodeError as exc:
            return JsonResponse({'error': 'JSON decode error', 'exception': str(exc)})
        print('get:', repr(tiles))
        tiles_contents = {tile['i']: {'html': '<b>Computed text</b>'} for tile in tiles}
        return JsonResponse({'tiles': tiles_contents})

    def _post(self, request, *args, **kwargs):
        print('cockpit post...', repr(request.POST['layout']))
        try:
            layout = json.loads(request.POST['layout'])
        except json.JSONDecodeError as exc:
            return JsonResponse({'error': 'JSONDecodeError', 'exception': str(exc)})

        self.params['user_preferences'][self.user_settings_path] = layout
        # self.params['user_preferences'][self.user_settings_path]
        return JsonResponse({'recorded_layout': 'not implemented yet'})

    def _get_context_data(self, **kwargs):
        # This part is comuted BEFORE applying the parameters->context mapping

        # Since this is a property only used to generate the html/js, no need to compute it in setup()
        #  (which is called at every instanciation)
        palette = {}
        for tile_template_name, tile_template in self.available_tile_templates.items():
            if tile_template['category'] not in palette:
                palette[tile_template['category']] = self.categories[tile_template['category']]
                palette[tile_template['category']]['items'] = {}
            palette[tile_template['category']]['items'][tile_template_name] = {
                'label': tile_template['label'],
                'help_text': tile_template.get('help_text', ''),
                'w': tile_template.get('w', 1),
                'h': tile_template.get('h', 1),
            }
        self.params['vue_props'] = {
            'html_id': self.html_id,
            # 'tile_templates': {k: {} for k, v in self.available_tile_templates.items()},
            'grid_params': {
                'row': self.rows,
                'columns': self.columns,
                'h_spacing': self.h_spacing,
                'v_spacing': self.v_spacing,
                'editable': self.editable,
                'init_layout': self.initial_layout,
            },
            'palette': palette,
        }

        # Apply parameters->context mapping then return
        return super()._get_context_data(**kwargs)
