from copy import copy, deepcopy
from collections.abc import Mapping
from pprint import pprint

import tomli

from django.db.models import Expression, Value, Case, When

"""
# TODO

- [X] Sorties d'actions (liste des états possibles)
- [-] Noms des états en utilisant les noms des conditions 'manuelles'
- [ ] Arbre syntaxique pour les conditions + moteur simplification (assez gros travail)...
  - [-] Meilleurs gestion des conflits entre conditions
- [ ] Expression ORM Django pour les états
- [ ] dict python pour les permissions
- [ ] Récupération des données (fields, default, etc.) depuis SmartView/Django
- [X] Export Graphviz (.gv)
"""


def _(m):
    return m


def get_deps(expr):
    if isinstance(expr, dict):
        r = set()
        for k, v in expr.items():
            if k.startswith(':'):  # Special case ':or' ':and' ':not'
                if isinstance(v, list):
                    for vv in v:
                        r |= get_deps(vv)
                else:
                    r |= get_deps(v)
            else:
                r.add(k.partition('__')[0])
        return r
    else:
        raise RuntimeError(_("Expression {} is not valid (not a dict) !").format(repr(expr)))


def make_states(cond_list):
    if len(cond_list) > 0:
        cond = cond_list[0]
        rem = make_states(cond_list[1:])
        return [[(cond[0], k, v)] + r for k, v in cond[1]['values'].items() for r in rem]
    else:
        return [[]]


def parse_condition_expression(expression):
    # STUB !
    return expression


def evaluate_condition_expression(expression, values):
    # print('  ', expression, values)
    if isinstance(expression, dict):
        for value in values:
            if value[0] in expression and expression[value[0]] != value[1]:
                return False
        return True
    else:
        raise RuntimeError(_("Only simple dict expressions are supported, not : '{}'").repr(expression))


def filter_match(filter_def, values):
    print("       filter_match", filter_def, values)
    for c, v in filter_def.items():
        fieldname, sep, lookup = c.partition('__')
        field_value = values.get(fieldname)
        if sep == '' and v != field_value:
            return False
        if lookup == 'isnull' and v is False and field_value is None:
            return False
        if lookup == 'isnull' and v is True and field_value is not None:
            return False
        # There is others lookups to handle...
        ...
    return True


def propagate_reachable(states, state):
    if state['reachable'] is False:
        state['reachable'] = True
        for action in state['actions'].values():
            for end in action['ends']:
                propagate_reachable(states, states[end])


class Workflow:
    def __init__(self, name: str, cfg: dict, fields: dict = None):
        self.name = str(name)
        self.fields = fields
        self.cfg = deepcopy(cfg)
        self.states: dict = dict()
        # self.permissions: dict = dict()
        self.next_state_index = 0
        self.conditions = {}

        all_deps = set()
        fieldnames_set = set(fields.keys())
        # For each condition
        for cname, condition in self.cfg['conditions'].items():
            self.conditions[cname] = {'values': {}, 'dependencies': set()}
            # Build dependencies list
            deps = set()
            for key, value in condition.items():
                self.conditions[cname]['values'][key] = copy(value)
                vdeps = get_deps(value)

                if not vdeps.issubset(fieldnames_set):
                    raise RuntimeError(
                        _("Workflow '{}': In condition '{}', for value '{}', dependencies {} are not all in fields ({})").format(
                            self.name, cname, key, vdeps, fieldnames_set
                        )
                    )

                if not all_deps.isdisjoint(vdeps):
                    raise RuntimeError(
                        _(
                            "Workflow '{}', Condition '{}' : value '{}' use "
                            "field(s) '{}' that are already used by previous conditions !"
                        ).format(self.name, cname, key, ', '.join(list(vdeps)))
                    )
                deps |= vdeps
            self.conditions[cname]['dependencies'] = deps
            all_deps |= deps
        pprint(self.conditions)

        # Build states (basic, no link, just conditions & names)
        self.states = {
            self.make_state_id(state_l): {
                'def': state_l,
                'actions': {},
                'dict': dict((s[0], s[1]) for s in state_l),
                'can_be_initial': None,
                'reachable': False,
            }
            for state_l in make_states(list(self.conditions.items()))
        }
        print(f"all states: {self.states}")

        # Parse actions conditions expressions
        for action_name, action_cfg in self.cfg['actions'].items():
            action_cfg['condition_expr'] = parse_condition_expression(action_cfg['condition'])

        # Fields that can be set at creation
        creation_fields = set(self.cfg['create']['permissions'].keys())

        # Defaults
        defaults_values = {k: v['default'] for k, v in fields.items()}

        # For each state
        for state_name, state_def in self.states.items():
            print(state_name)
            # Build state --> action --> state links
            for action_name, action_cfg in self.cfg['actions'].items():
                if evaluate_condition_expression(action_cfg['condition_expr'], state_def['def']):
                    state_def['actions'][action_name] = {'ends': set()}
                    print(' ', action_name)
                    for dest_state_name, dest_state_def in self.states.items():
                        dest_ok = True
                        for dest_cond_name, dest_cond_value in dest_state_def['dict'].items():
                            if (
                                set(action_cfg['permissions'].keys()).isdisjoint(self.conditions[dest_cond_name]['dependencies'])
                                and state_def['dict'][dest_cond_name] != dest_cond_value
                            ):
                                dest_ok = False
                                break
                        if dest_ok:
                            state_def['actions'][action_name]['ends'].add(dest_state_name)

            # Determine if this state can be a initial state
            can_be_initial = True
            for cond in state_def['def']:
                cond_fields = self.conditions[cond[0]]['dependencies']
                print('   ', cond[0], cond_fields)
                print(f"     {cond[2]}/{defaults_values}")
                if cond_fields.isdisjoint(creation_fields) and not filter_match(cond[2], defaults_values):
                    can_be_initial = False
                    break
            state_def['can_be_initial'] = can_be_initial
            print('    ', can_be_initial)

        # Propagate 'reachable' attribute
        for state_name, state_def in self.states.items():
            if state_def['can_be_initial']:
                propagate_reachable(self.states, state_def)

        self.states = {k: v for k, v in self.states.items() if v['reachable'] is True}

    def make_state_id(self, state_l: list[tuple]) -> str:
        # return '__'.join(s[0] + ':' + s[1] for s in state_l)
        state_id = 'S' + str(self.next_state_index)
        self.next_state_index += 1
        return state_id

    def dot(self):
        bn = '\n'
        output = "digraph {\n"
        for k, v in self.states.items():
            if k:
                attrs = 'style="filled", fillcolor="#ffff88", ' if v['can_be_initial'] else ''
                output += f'''  "{k}" [{attrs}shape=box, label="{k}\n{bn.join([c[0]+'='+c[1] for c in v['def']])}"];\n'''
                for ak, av in v['actions'].items():
                    for lnk in av['ends']:
                        # lnk_name = self.mk_state_id(lnk)
                        output += f'''    "{k}" -> "{lnk}" [label="{ak}\n({', '.join(self.cfg['actions'][ak]['roles'])})"];\n'''
        output += "}\n"
        return output

    @property
    def permissions(self) -> dict:
        perms = {'create': tuple(role for role in self.cfg['create']['permissions']), 'write': {}}
        # 'Creation' permissions (quite simple, can be written with comprehensions)
        perms['write'][None] = {
            role: {fieldname: permission for fieldname, permission in self.cfg['create']['permissions'].items()}
            for role in self.cfg['create']['roles']
        }
        # 'states' permissions ; a little more complicated since a role can be granted for multiple actions
        for state_n, state_d in self.states.items():
            state_roles_perms = {}
            for action_n in state_d['actions'].keys():
                action_d = self.cfg['actions'][action_n]
                for role in action_d['roles']:
                    state_roles_perms[role] = dict(state_roles_perms.get(role, {}), **action_d['permissions'])
            perms['write'].update({state_n: state_roles_perms})
        return perms

    @property
    def django_orm_state_expr(self) -> Expression:
        # First, lazy, implementation. Rely on database engine optimizer
        cases = []
        for state_name, state_def in self.states.items():
            conds = {}
            for name, value, condition_expr in state_def['def']:
                conds.update(condition_expr)
            cases.append(When(**conds, then=Value(state_name)))
        return Case(*cases, default=Value('Undefined'))

    def __str__(self):
        return self.dot()


def toml_to_dict(cfg, dict_id: str | None = None):
    """Get a object and transform any included list of dictionnaries in a single dictionnary
    with its keys as `dict_id` parameter entry (only if every dict in the list has this key).
    Designed to be used with [[something]] TOML syntax with every section with a 'name' or
    'id' or any other identifier/key.

    Use a recursive algorithm.

    :param cfg: The
    :type cfg: Any litteral type
    :param dict_id: name of the id field, defaults to None (=> does nothing)
    :type dict_id: str or None, optional
    :return: The treated cfg object
    :rtype: Same as one provided in input (cfg)
    """
    if isinstance(cfg, list):
        if all([isinstance(v, dict) and dict_id in v for v in cfg]):
            return {v[dict_id]: toml_to_dict({kk: vv for kk, vv in v.items() if kk != dict_id}, dict_id) for v in cfg}
        else:
            return [toml_to_dict(v, dict_id) for v in cfg]
    elif isinstance(cfg, Mapping):
        return {k: toml_to_dict(v, dict_id) for k, v in cfg.items()}
    else:
        return cfg


if __name__ == '__main__':
    # Experimental code (to work on class creation)

    # This should come from SmartView (don't forget to add dependencies !!)
    simple_fields_cfg = {
        'cloture': {'default': None},
        'd1': {'default': None},
        'd2': {'default': None},
        'nom': {'default': None},
    }

    with open('local/config.d/workflows.toml', 'rb') as f:
        cfg = toml_to_dict(tomli.load(f), dict_id='name')['workflows']

    wf = Workflow('demo', cfg['demo'], simple_fields_cfg)
    with open('test.gv', 'w+') as f:
        f.write(wf.dot())

    pprint(cfg['demo'])
    pprint(wf.permissions)
    print(wf.django_orm_state_expr)
