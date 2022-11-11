from copy import deepcopy
import json
from pprint import pprint

from django.db.models import Value

"""
# TODO

- [ ] Sorties d'actions (liste des états possibles)
- [ ] Noms des états en utilisant les noms des conditions 'manuelles'
- [ ] Arbre syntaxique pour les conditions + moteur simplification (assez gros travail)...
  - [ ] Meilleurs gestion des conflits entre conditions
- [ ] Expression ORM Django pour les états
- [ ] dict python pour les permissions
- [ ] Récupération des données (fields, default, etc.) depuis SmartView/Django
- [ ] Export Graphviz (.gv)
"""


class Workflow:
    def __init__(self, name: str, cfg: dict, fields: dict = None):
        self.name = str(name)
        self.fields = fields
        self.cfg = deepcopy(cfg)
        self.states: dict = dict()
        self.permissions: dict = dict()

        # Check that workflow name, all condition names and action names are identifiers
        if not self.name.isidentifier():
            raise RuntimeError(f"Workflow name '{self.name}' is not a valid identifier")
        for condition_name in self.cfg['conditions']:
            if not condition_name.isidentifier():
                raise RuntimeError(f"Workflow '{self.name}' condition name '{condition_name}' is not a identifier.")
        for action_name in self.cfg['actions']:
            if not action_name.isidentifier():
                raise RuntimeError(f"Workflow '{self.name}' action name '{action_name}' is not a identifier.")

        def condition_unpack(conditions_cfg: dict, condition: str | tuple | list | dict | None) -> list | None:
            if condition is None:
                return condition
            elif isinstance(condition, dict):
                return [condition]
            elif isinstance(condition, str):
                if condition in conditions_cfg:
                    unpacked_condition = conditions_cfg.get(condition)
                    if isinstance(unpacked_condition, dict):
                        return [unpacked_condition]
                    else:
                        return condition_unpack(conditions_cfg, unpacked_condition)
                else:
                    raise RuntimeError("Condition '{}' not found in workflow '{}'".format(condition, self.name))
            elif isinstance(condition, list) or isinstance(condition, tuple):
                return sum([condition_unpack(conditions_cfg, c) for c in condition], [])
            else:
                raise RuntimeError("Type of condition must be str or tuple or list, not {}".format(type(condition)))

        def conflict_detect(lu1, v1, lu2, v2):
            # field__isnull=True is in conflict with almost everything (except itself)
            if lu1 == 'isnull' and v1 is True and (lu2 != 'isnull' or not (v2 is True)):
                return True
            # field__isnull=True is in conflict with almost everything (except itself) ; mirror
            if lu2 == 'isnull' and v2 is True and (lu1 != 'isnull' or not (v1 is True)):
                return True
            # different values with same lookup -> conflict
            if lu1 == lu2 and v1 != v2:
                return True

            # For now, everything else seems not lead to a conflict
            return False

        def are_sconditions_conflicting(c1: dict, c2: dict) -> bool:
            # If conditions not on same fields => not problem
            if c1['fields'].isdisjoint(c2['fields']):
                return False
            # just a simple for a start :
            if len(c1['def']) == 1 and len(c2['def']) == 1:
                k1 = list(c1['def'].keys())[0]
                k2 = list(c2['def'].keys())[0]
                if not k1.startswith(':') and not k2.startswith(':'):
                    lu1, v1 = k1.partition('__')[2], c1['def'][k1]
                    lu2, v2 = k2.partition('__')[2], c2['def'][k2]
                    conflict = conflict_detect(lu1, v1, lu2, v2)
                    return conflict
            return False

        def scondition_fields(scondition: dict) -> set:
            deps = set()
            for name, data in scondition.items():
                if name[0] != ':':
                    deps.add(name.split('__')[0])
            return deps

        def build_states(sconditions: dict, indexes: list | None = None, conflicts_sconditions: dict or None = None) -> list:
            """Build a list of states (as list of sconditions indexes) while preventing conflics (ie does not
                include in a same state conficting conditions)

            :param sconditions: all workflow sconditions definitions
            :type sconditions: dict
            :param conflicts_sconditions: dict of sconditions used to check for conflicts (indexes sconditions is used if None)
            :type conflicts_sconditions: dictorNone
            :param indexes: List of indexes used to generate states combinations (sconditions keys are used if None),
                defaults to None
            :type indexes: list | None, optional
            :return: list of states as lists of sconditions indexes
            :rtype: list
            """
            if indexes is None:
                indexes = list(sconditions.keys())
            else:
                indexes = list(indexes)

            conflicts_sconditions = conflicts_sconditions or {i: sconditions[i] for i in indexes}

            states: list[list] = [[]]
            while indexes:
                index = indexes[0]
                indexes = indexes[1:]
                states += [
                    state + [index] for state in states if set(conflicts_sconditions[index]['conflicts']).isdisjoint(set(state))
                ]
            return states

        # print(build_states(list(range(10))), len(build_states(list(range(10)))))
        # Process all conditions lists to get states

        # For each action, resolve conditions names (= build a list of 'single' conditions)
        # And build the workflow wide 'single' conditions list.
        all_sconditions_set: set = set()
        for action_name, action_def in self.cfg['actions'].items():
            sconditions_list: list | None = condition_unpack(self.cfg.get('conditions', {}), action_def.get('condition', tuple()))
            # print(action_name, sconditions_list)

            # keep this list for later use
            if sconditions_list is not None:
                action_def['sconditions_json_set'] = {
                    json.dumps(c, sort_keys=True, separators=(',', ':')) for c in sconditions_list
                }
            else:
                action_def['sconditions_json_set'] = set()

            # Add conditions to the global set
            # Use a JSON compact canonic encoding to prevent (almost ?) multiple registrations for a same condition
            all_sconditions_set |= action_def['sconditions_json_set']

        # print(f"all_conditions_set: {all_conditions_set}")

        # Build a list of all 'single' conditions in the workflow
        all_sconditions: dict = {
            idx: {'json_def': json_definition, 'def': json.loads(json_definition)}
            for idx, json_definition in enumerate(sorted(list(all_sconditions_set)))
        }

        reversed_sconditions = {v['json_def']: k for k, v in all_sconditions.items()}

        # For each action, set unique conditions indexes set
        for action_name, action_def in self.cfg['actions'].items():
            if action_def['condition'] is None:
                action_def['sconditions_idx_set'] = None
            else:
                action_def['sconditions_idx_set'] = {reversed_sconditions[j] for j in action_def['sconditions_json_set']}

        # Extract field names in every 'single' condition
        for idx, scondition_data in all_sconditions.items():
            scondition_data['fields'] = scondition_fields(scondition_data['def'])

        # Detect 'single' conditions conflicts
        for idx, scondition_data in all_sconditions.items():
            scondition_data['conflicts'] = []
            for idx2, scondition_data2 in all_sconditions.items():
                if idx2 != idx and are_sconditions_conflicting(scondition_data, scondition_data2):
                    scondition_data['conflicts'].append(idx2)
                    # print("Conflict !", idx, idx2, scondition_data['def'], scondition_data2['def'])

        # preliminary states dict
        self.states = {'-'.join(['c' + str(s) for s in p]): {'sconditions_set': set(p)} for p in build_states(all_sconditions)}

        for state_def in self.states.values():
            # links actions sources to states
            state_def['actions'] = {
                k: {}
                for k, v in self.cfg['actions'].items()
                if v['sconditions_idx_set'] is not None and v['sconditions_idx_set'].issubset(state_def['sconditions_set'])
            }
            # build fields dependencies (useful ??)
            state_def['fields'] = set()  # field dependencies
            for sc in state_def['sconditions_set']:
                state_def['fields'] |= all_sconditions[sc]['fields']

        # For every action, compute which condition can be affected
        for k, v in self.cfg['actions'].items():
            # potentialy modified conditions
            pmc = set()
            for sc in all_sconditions.keys():
                if not all_sconditions[sc]['fields'].isdisjoint(v['permissions'].keys()):
                    # at least a fields
                    pmc.add(sc)
            # set(v['permissions'].keys()).intersection(all_sconditions[] state_def['sconditions_set'])  # list of fields
            v['can_alter_sconditions_set'] = pmc

        # print("List of all states :")
        # pprint(self.states)

        # links actions ends to states
        for state_def in self.states.values():
            print("state:", state_def['sconditions_set'])
            for k in state_def['actions'].keys():
                v = self.cfg['actions'][k]
                unmodified_sconditions = state_def['sconditions_set'] - v['can_alter_sconditions_set']
                # print("  action:", k)
                # print("    unmodified:", unmodified_sconditions)
                # print("    indexes:", list(v['can_alter_sconditions_set']))
                # print(
                #     "    conflicts:", {i: all_sconditions[i] for i in list(unmodified_sconditions | v['can_alter_sconditions_set'])}
                # )
                modified_conditions = build_states(
                    all_sconditions,
                    indexes=list(v['can_alter_sconditions_set']),
                    conflicts_sconditions={
                        i: all_sconditions[i] for i in list(unmodified_sconditions | v['can_alter_sconditions_set'])
                    },
                )
                final_conditions = [set(msc) | unmodified_sconditions for msc in modified_conditions]
                state_def['actions'][k]['ends'] = final_conditions
                print(f'    {k}: pmc {final_conditions}')

        print("List of all single conditions :")
        pprint(all_sconditions)
        print()
        print("List of all single actions :")
        pprint(self.cfg['actions'])
        print()
        print("List of all states :")
        pprint(self.states)

        # Build a preliminary workflow tree
        ...

        # Remove every unreachable state
        ...

    @property
    def states_expr(self):
        return Value('')

    # @property
    # def permissions(self):
    #     return dict()

    def dot(self):
        output = "digraph {\n"
        for k, v in self.states.items():
            if k:
                output += f'  "{k}" [shape=rect];\n'
                for ak, av in v['actions'].items():
                    for lnk in av['ends']:
                        lnk_name = '-'.join(['c' + str(s) for s in lnk])
                        output += f'    "{k}" -> "{lnk_name}" [label="{ak}"];\n'
        output += "}\n"
        return output

    def __str__(self):
        return self.dot()


simple_fields_cfg = {
    'cloture': {'default': None},
    'p1': {'default': None},
    'p2': {'default': None},
    'nom': {'default': None},
}

simple_workflow_cfg = {
    'conditions': {
        'active': {'cloture__isnull': True},
        'closed': (
            {'cloture__isnull': False},
            # {'cloture__lt': 'NOW'},
        ),
        'c1': {'p1': True},
        'c2': {'p2': True},
    },
    'actions': {
        'create': {
            'roles': (
                'DIR',
                'EXP',
            ),
            'condition': None,
            'permissions': {
                'nom': True,
            },
        },
        'modify': {
            'roles': (
                'OWN',
                'ADM',
            ),
            'condition': 'active',
            'permissions': {
                'nom': True,
            },
        },
        'update1': {'roles': ('P1',), 'condition': 'active', 'permissions': {'p2': True}},
        'update2': {'roles': ('P2'), 'condition': 'active', 'permissions': {'p1': True}},
        'close': {
            'roles': ('ADM',),
            'condition': ('c1', 'c2', 'active'),
            'permissions': {
                'cloture': True,
            },
        },
        'reopen': {
            'roles': ('ADM',),
            'condition': 'closed',
            'permissions': {
                'cloture': True,
            },
        },
    },
}

double_workflow_cfg = {
    'conditions': {
        'c1': {'f1': True},
        'c2': {'f2': True},
    },
    'actions': {
        'update1': {'roles': ('P1', 'P2'), 'condition': 'c1', 'permissions': {'p2': True}},
        'update2': {'roles': ('P1', 'P2'), 'condition': 'c2', 'permissions': {'p1': True}},
    },
}

if __name__ == '__main__':
    # Experimental code (to work on class creation)
    wf = Workflow('demo', simple_workflow_cfg, simple_fields_cfg)
    with open('test.gv', 'w+') as f:
        f.write(wf.dot())
