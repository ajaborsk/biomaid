#!/usr/bin/python3
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
"""

   Fonctionnalités à implémenter :
   ===============================

   Tests et contrôles :
   --------------------

   * Tests de régression avec différentes config (navigateur, moteur bdd)
   * Analyse + tests individuels (pour débuggage)
   * Contrôle de la configuration python: packages (venv)
   * Contrôle du settings ???
   * Détection accès serveur exploit (+ ssh auto)
   * Détection état git (branche, répertoire de travail, commit/tag)
   * Détection BDD (moteur, pgsql présent, base de test O/N...)
   * Tests coverage
   * Analyse flake8
   * Détection print() ou log() de debug dans le source

   Actions :
   ---------

   * Créer une nouvelle version (tout compris)
   * contrôle passage exploit -> nouvelle version (migration, etc.)
   * Passage complet vers la nouvelle version (tout compris) sur la base de production ???

   Gestion de la base :
   --------------------

   * Repository de bases (pour développement)
   * To/From base de test (avec contrôle)
   * Récupération copie base exploitation
   * Récupération/check sauvegarde ?

   Runtime :
   ---------

   * Fonctionnement runserver de dev en tâche de fond
   * Aides navigation dans les logs (debug, QuiFaitQuoi...)
   * Shell django ?

   Divers :
   --------

   * Gestion de la configuration (semi-arborescente, à la .INI) de l'outil lui-même, avec sauvegarde auto locale
   * Mode curses ou console ? Tk ?

   Partie exploitation (sans doute à mettre dans un outil différent à terme) :
   ===========================================================================

   * Mises à jour des différentes structures (UF) ?? En attendant sans doute une version en ligne.
   * Analyse logs production ?
   * Divers contrôles de cohérence de la base qui ne peuvent pas être intégrés dans Django
   * Gestion des tâches périodiques (cron) ?
   * Configuration/Gestion/Vérification des sauvegardes

"""

import sys
import os
import gettext
import subprocess
import configparser
import argparse

_ = gettext.gettext


class Unit:
    """
    Une Unit est un objet qui reçoit et émet des données / messages / événements
    Il reçoit ses messages par le biais de callbacks
    """

    def __init__(self):
        self._callbacks = {}

    def callback_has(self, id):
        return id in self._callbacks

    def callback_set(self, id, func):
        self._callbacks[id] = func

    def callback_unset(self, id):
        del self._callbacks[id]

    def callback_fire(self, id, *args, **kwargs):
        if id in self._callbacks:
            return self._callbacks[id](*args, **kwargs)


class Widget(Unit):
    """Un Widget est une Unit qui peut gérer les événements en provenance et vers l'utilisateur.
    Quand un widget a le "focus", c'est lui qui reçoit les événements (clavier, souris...) en provenance de l'utilisateur
    """

    def __init__(self):
        super().__init__()
        self.has_focus = False

    def show(self):
        pass

    def hide(self):
        pass

    def handle(self, event):
        """handle a imput event"""
        raise NotImplementedError("handle method must be overloaded")

    def draw(self):
        raise NotImplementedError("draw method must be overloaded")


class StatusWidget(Widget):
    def set_text(self, text):
        pass


class MenuWidget(Widget):
    def __init__(self, entries=[]):
        self.entries = entries
        super().__init__()


class TextAreaWidget(Widget):
    pass


class UserInterface:
    def __init__(self, app):
        self.app = app
        # self.config = config
        # self.menu = menu
        self.app.current_menu = self.app.menu_tree
        self.app.current_row = 0
        self.app.current_entry = self.app.menu_tree[self.app.current_row]
        self.app.upper_menu = None

        self.widgets = []
        self.focus_widget = None

    def add_widget(self, widget):
        self.widgets.append(widget)

    def mainloop(self):
        raise NotImplementedError("mainloop method must be overloaded")


class AppSubprocess:
    def __init__(self, *args, **kwargs):
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE
        self.sp = subprocess.Popen(*args, **kwargs)
        self.out = ""
        self.err = ""

    def check(self):
        if self.sp.returncode is None:
            try:
                self.sp.communicate(None, timeout=0)
            except subprocess.TimeoutExpired:
                pass


class Entry:
    def __init__(self, app):
        self.app = app
        self.config = app.config


class QuitEntry(Entry):
    title = _("Quit")
    help = _("Quit the application")
    shortcut = _("q")


class ConsoleUI(UserInterface):
    def wait_key(self):
        '''Wait for a key press on the console and return it as a python string.'''
        result = None
        if os.name == 'nt':
            import msvcrt

            result = msvcrt.getch().decode('ascii')
        else:
            import termios

            fd = sys.stdin.fileno()

            oldterm = termios.tcgetattr(fd)
            newattr = termios.tcgetattr(fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)

            try:
                result = sys.stdin.read(1)
            except IOError:
                pass
            finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

        return result

    def mainloop(self):
        done = False
        while not done:
            print("\n" * 100)
            print("=" * 80)
            print(self.title)
            print("-" * 80)
            print()
            print(_(" t - Lancer tous les tests"))
            print()
            print(_(" q - Quitter"))
            print()
            print("-" * 80)
            print(_("Pressez une touche :"), end="")
            sys.stdout.flush()
            key = self.wait_key()
            print()

            if key == 'q':
                done = True
            elif key == 't':
                os.environ['MOZ_HEADLESS'] = "1"
                subprocess.run(["python", "manage.py", "test"])


class CursesMenuWidget(MenuWidget):
    def __init__(self, parent, window, entries=[]):
        super().__init__(entries)
        self.parent = parent
        self.styles = parent.styles
        self.curses = parent.curses
        self.win = window
        self.current_row = 0
        self.shortcuts = {}
        for entry in entries:
            shortcut = entry.get('shortcut', None)
            if shortcut:
                self.shortcuts[ord(shortcut)] = entry

    def handle(self, event):
        if event == self.curses.KEY_UP:
            if self.current_row > 0:
                self.current_row -= 1
                self.draw()
                self.callback_fire('select', self.entries[self.current_row].get('tool', None))
        elif event == self.curses.KEY_DOWN:
            if self.current_row < len(self.entries) - 1:
                self.current_row += 1
                self.draw()
                self.callback_fire('select', self.entries[self.current_row].get('tool', None))
        elif event == 10:
            self.callback_fire('activate', self.entries[self.current_row].get('tool', None))
        elif event in self.shortcuts:
            self.callback_fire('activate', self.shortcuts[event].get('tool', None))
        else:
            # Unhandled event => return it
            return event

    def draw(self):
        for row in range(len(self.entries)):
            label = self.entries[row].get('label', '')
            if row == self.current_row:
                self.win.addstr(row + 1, 2, label, self.styles['selected'])
            else:
                self.win.addstr(row + 1, 2, label, self.styles['normal'])


class CursesUI(UserInterface):
    def __init__(self, curses, app):
        self.curses = curses
        super().__init__(app)

    def vline_border(self, win, pos):
        win_h, win_w = win.getmaxyx()
        win.vline(1, pos, self.curses.ACS_VLINE, win_h - 2)
        win.addch(0, pos, self.curses.ACS_TTEE)
        win.addch(win_h - 1, pos, self.curses.ACS_BTEE)

    # def menu_draw(self, win):
    #     for row in range(len(self.app.current_menu)):
    #         entry = self.app.current_menu[row]
    #         if isinstance(entry, Entry):
    #             entry_text = entry.shortcut + ' - ' + entry.title
    #         else:
    #             entry_text = entry[1]
    #         if row == self.app.current_row:
    #             win.addstr(row + 2, 35, entry_text, self.curses.color_pair(3))
    #         else:
    #             win.addstr(row + 2, 35, entry_text)

    def menu_activate(self, tool):
        if tool is not None:
            self.win.addstr(2 + 2, 35, 'activated ! {}'.format(tool))
            self.win.refresh()
            if isinstance(tool, Entry):
                tool.launch()
            elif tool == 'quit':
                self.done = True
        # raise NotImplementedError("row {} {}".format(row, repr(self.win)))

    def entry_selected(self, tool):
        if tool is not None:
            pass

    def curses_mainloop(self, stdscr):
        self.win = stdscr
        self.done = False

        # Do not wait for a key more than 1000ms = 1s
        stdscr.timeout(1000)

        # Normal
        self.curses.init_pair(1, self.curses.COLOR_WHITE, self.curses.COLOR_BLUE)

        # Alert
        self.curses.init_pair(2, self.curses.COLOR_RED, self.curses.COLOR_WHITE)

        # Reverse
        self.curses.init_pair(3, self.curses.COLOR_BLUE, self.curses.COLOR_WHITE)

        self.styles = {
            'normal': self.curses.color_pair(1),
            'alert': self.curses.color_pair(2),
            'selected': self.curses.color_pair(3),
        }

        win = stdscr.subwin(20, 32, 1, 1)
        self.left_menu_widget = CursesMenuWidget(self, win, self.app.current_menu)
        self.add_widget(self.left_menu_widget)
        self.focus_widget = self.left_menu_widget
        self.left_menu_widget.callback_set('activate', self.menu_activate)
        self.left_menu_widget.callback_set('select', self.entry_selected)

        # Clear screen
        stdscr.clear()

        stdscr.attrset(self.curses.color_pair(1))
        stdscr.bkgd(self.curses.color_pair(1))

        while not self.done:

            stdscr.border()
            self.vline_border(stdscr, 33)

            win_h, win_w = stdscr.getmaxyx()
            if win_h < 24 or win_w < 80:
                # terminal is too small, do not draw anything
                # Clear screen
                stdscr.attrset(self.styles['alert'])
                stdscr.bkgd(self.styles['alert'])
                stdscr.clear()
                stdscr.border()
                stdscr.addstr(win_h // 2, win_w // 2 - 10, _("Terminal is too small"))
                stdscr.addstr(win_h // 2 + 1, win_w // 2 - 10, _("Resize or 'q' to quit"))
            else:

                # self.menu_draw(stdscr)

                for widget in self.widgets:
                    widget.draw()

                stdscr.refresh()

            self.curses.curs_set(0)
            k = stdscr.getch()

            # if k == ord('q'):
            #    done = True
            # else:
            k = self.focus_widget.handle(k)

            if k == -1:
                # timeout
                for subp in self.app.subprocesses:
                    subp.check()

            # elif k == self.curses.KEY_UP and self.app.current_row > 0:
            #     self.app.current_row -= 1
            # elif k == self.curses.KEY_DOWN and self.app.current_row < len(self.app.current_menu) - 1:
            #     self.app.current_row += 1

        return repr(k)

    def mainloop(self):
        self.curses.wrapper(self.curses_mainloop)


class ToolApplication:
    def __init__(self, title="Tool", menu=[]):
        parser = argparse.ArgumentParser(description=title)
        parser.add_argument(
            '-c',
            '--config',
            help=_("Utilise le fichier de configuration spécifié (format INI ; {} par défaut)").format(DEFAULT_CONFIG_FILENAME),
            default=DEFAULT_CONFIG_FILENAME,
        )
        parser.add_argument(
            '-n',
            '--no-curses',
            help=_("N'utilise pas curses même s'il est détecté"),
            action='store_true',
        )

        self.args = parser.parse_args()

        self.config = configparser.ConfigParser()
        self.config.read(self.args.config)

        # menu.append(QuitEntry(self.config))
        # self.menu_tree = menu

    def run(self):
        self.user_interface = None
        if not self.args.no_curses:
            try:
                import curses

                self.user_interface = CursesUI(curses, self)
            except ImportError:
                pass

        if self.user_interface is None:
            self.user_interface = ConsoleUI(self)

        self.subprocesses = []

        self.user_interface.mainloop()


# ==================================================================================================================================


DEFAULT_CONFIG_FILENAME = "biom_aid_devtool.ini"

CONFIG = {
    'production_server': 'trinidad',
    'production_user': 'user_dra',
}


class TestsTool(Entry):

    title = _("")
    shortcut = 't'
    help = _(
        """Blabla
"""
    )

    def check(self):
        return True, {}

    def launch(self):
        os.environ['MOZ_HEADLESS'] = "1"
        self.app.subprocesses.append(AppSubprocess(["python", "manage.py", "test"]))

        # subprocess.run(["python", "manage.py", "test"])
        return {}


"""
  Arbre de menus de l'application.

  C'est un dictionnaire (donc ordonné) avec la touche à utiliser comme clé et l'action à mener comme valeur.
  Une action peut être :
    - Un dictionnaire, qui est interprété comme un sous-menu
    - Une instance d'une sous-classe de Tool : dans ce cas, sa méthode run() est appelée,
                                               après vérification des éventuelles conditions
    - Une fonction : elle est appelée directement
    - la chaîne 'quit' : L'application est terminée

"""
MENU_TREE = {
    't': 'Lancer tous les tests',
    '': '---------------------------------------',
    'q': ('quit'),
}


class BiomAidDevTool(ToolApplication):
    def __init__(self):
        super().__init__(_("Outil d'aide au développement de BIOM_AID"))
        self.menu_tree = [
            {
                'label': _("Tests de régression"),
                'shortcut': 't',
                'tool': TestsTool(self),
            },
            {'label': '=' * 24},
            {
                'label': _("Quitter"),
                'shortcut': 'q',
                'tool': 'quit',
            },
        ]


# ==================================================================================================================================


if __name__ == '__main__':
    BiomAidDevTool().run()
