from gettext import gettext as _
from argparse import ArgumentParser
import time
from cmd import Cmd
from subprocess import run, Popen, STDOUT, DEVNULL, PIPE
from signal import SIGINT
import os
import code

# import readline  # optional, will allow Up/Down/History in the console
from playwright.sync_api import sync_playwright


def biomaid_launch(args):
    # TODO: Check for errors instead of throwing stderr to /dev/null...
    # TODO: Check virtual environment ?
    # TODO: parametric host:port
    # TODO: parametric time travel destination
    # ensure we use the mktest database
    os.environ['MKTEST'] = '1'
    # make Django believe we are in the past :-) (needs a hacked manage.py)
    os.environ['TIME_TRAVEL'] = '2020-08-15 03:00:00'
    # TODO: Check database ? How ?
    print("Empty database...")
    run(['python', 'manage.py', 'reset_db', '--no-input'], stdout=DEVNULL, stderr=STDOUT)
    print("Migrate...")
    run(['python', 'manage.py', 'migrate'], stdout=DEVNULL, stderr=STDOUT)
    print("Load tests DB...")
    run(['python', 'manage.py', 'loaddata', 'fixtures/tests_db.json'], stdout=DEVNULL, stderr=STDOUT)
    print("Launch Django server...")
    # pipe stdout to a pipe so we can monitor its behaviour
    server = Popen(
        ['python', 'manage.py', 'runserver', '--insecure', 'localhost:8123'],
        stdout=PIPE,
        stderr=STDOUT,
        encoding='UTF-8',
    )

    stdout = ''
    launched = False
    while not launched:
        data = server.stdout.readline()
        stdout += data
        if "Quit the server with CONTROL-C" in data:
            time.sleep(1)
            launched = True
        if server.poll() is not None:
            print(stdout)
            break
    if launched:
        return server


class Cli(Cmd):
    prompt = 'BiomAid MkTest CLI > '
    intro = _("Do whatever you want !\nType 'help' to get some help :-)")

    def __init__(self, args):
        self.args = args
        super().__init__()
        self.registred_users = {
            'root': {
                'name': "Super utilisateur",
                'description': "Super utilisateur",
                'password': 'introuvable',
            },
            'tomiela': {
                'name': "Lana Tomie",
                'description': "Experte métier sur l'UF 1001 (USLD), dispatcheuse campagne équipements TEST",
                'password': 'yQ6FfiKypa7h8Hc',
            },
            'enbaveyv': {
                'name': "Yvon Enbaver",
                'description': "Cadre supérieur de pôle sur l'UF 0003",
                'password': 'yQ6FfiKypa7h8Hc',
            },
            'deboziel': {
                'name': "Ella de Bozieux",
                'description': "Directrice adjointe UF 0001 et 0002 et Directrice référente UF 0003",
                'password': 'yQ6FfiKypa7h8Hc',
            },
            'cekilesy': {
                'name': "Sylvie Cekilépamor",
                'description': "Cheffe de pôle UF 0003",
                'password': 'yQ6FfiKypa7h8Hc',
            },
            'couranth': {
                'name': "Théo Courant",
                'description': "Cadre de santé UF 0003",
                'password': 'yQ6FfiKypa7h8Hc',
            },
            'timettvi': {
                'name': "Vincent Timettre",
                'description': "Expert métier sur les UF 0001, 0002 et 0003",
                'password': 'yQ6FfiKypa7h8Hc',
            },
            'bonbeuje': {
                'name': "Jean Bonbeurre",
                'description': "Expert métier travaux sur l'établissement support ETS",
                'password': "yQ6FfiKypa7h8Hc",
            },
            'zonloilo': {
                'name': "Laurie Zonlointain",
                'description': "Ingénieure travaux sur l'établissement support ETS, dispatcheur campagne travaux TVXCT",
                'password': "yQ6FfiKypa7h8Hc",
            },
            'arbitre_biomed': {
                'name': "Harry Staukrate",
                'description': "Arbitre programme BIO-00-PE",
                'password': 'yQ6FfiKypa7h8Hc',
            },
            'igonnepa': {
                'name': "Paul Igonne",
                'description': "Arbitre programme TVX-00-PC",
                'password': 'yQ6FfiKypa7h8Hc',
            },
        }
        self.server = biomaid_launch(args)
        if self.server:
            print("Do something with ready server...")

    def browser_launch(self, username=None, shell=False):
        with sync_playwright() as p:
            # Make sure to run headed.
            browser = p.chromium.launch(headless=False)

            # Setup context however you like.
            context = browser.new_context()  # Pass any options
            # context.route('**/*', lambda route: route.continue_())

            # Pause the page, and start recording manually.
            page = context.new_page()
            page.goto("http://localhost:8123/")
            if username is not None:
                user = self.registred_users[username]
                page.get_by_label("Nom d’utilisateur :").fill(username)
                page.get_by_label("Nom d’utilisateur :").press("Tab")
                page.locator("#id_password").fill(user['password'])
                page.get_by_role("button", name="Se connecter").click()
            page.pause()
            if shell:
                variables = globals().copy()
                variables.update(locals())
                shell = code.InteractiveConsole(variables)
                shell.interact()

    def do_lh(self, line):
        "Tada !"
        if 'help' in line:
            print(f"{line=}")
        else:
            print(
                _(
                    "Recognized commands :\n"
                    " help: Display this help\n"
                    " quit: Quit this CLI without saving anything\n"
                    " save: Save the tests database into fixtures/tests_db.json file\n"
                    " browse_as *user*: Open a web browser on the tests server then connect as *user*. Possibles users are :\n{users:s}"
                ).format(
                    users="".join(
                        '  - ' + username + ': ' + userdesc.get('description', '') + '\n'
                        for username, userdesc in self.registred_users.items()
                    )
                )
            )

    def __del__(self):
        # This is the CLI end !
        print("Done.")
        self.server.send_signal(SIGINT)

    def help_u(self):
        print(
            "Listes des utilisateurs enregistrés :\n{users}".format(
                users=''.join(
                    " - '" + user + "' : " + desc['name'] + ", " + desc['description'] + "\n"
                    for user, desc in self.registred_users.items()
                )
            )
        )

    def do_b(self, line):
        "Open a browser, connect as a registred user then wait"
        if line in self.registred_users:
            self.browser_launch(username=line or None)
        else:
            print(f"Utilisateur inconnu : '{line}'")
            print(
                "Listes des utilisateurs enregistrés :\n{users}".format(
                    users=''.join(
                        " - '" + user + "' : " + desc['name'] + ", " + desc['description'] + "\n"
                        for user, desc in self.registred_users.items()
                    )
                )
            )
        return False

    def do_bs(self, line):
        "Open a browser, connect as a registred user then open a python shell"
        if line in self.registred_users:
            self.browser_launch(username=line or None, shell=True)
        else:
            print(f"Utilisateur inconnu : '{line}'")
            print(
                "Listes des utilisateurs enregistrés :\n{users}".format(
                    users=''.join(
                        " - '" + user + "' : " + desc['name'] + ", " + desc['description'] + "\n"
                        for user, desc in self.registred_users.items()
                    )
                )
            )
        return False

    def do_s(self, line):
        "Save the tests database into backup.json.bz2"
        run(['python', 'manage.py', 'backup'])

    def do_EOF(self, line):
        "Terminate the CLI"
        return True

    def do_q(self, line):
        "Terminate the CLI"
        return True


def main(args):
    Cli(args).cmdloop()


if __name__ == '__main__':
    parser = ArgumentParser(description=_("A simple CLI to help building tests for the BiomAid project"))
    args = parser.parse_args()
    main(args)
