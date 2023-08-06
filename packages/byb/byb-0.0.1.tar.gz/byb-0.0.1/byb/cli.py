"""
The `byb.cli` module packages all `byb` bots into a single cli.
"""


import os


import click


COMMAND_METHOD = "cli"

COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__), "bots")

COMMAND_NAMES = [
    filename[:-3]
    for filename in os.listdir(COMMANDS_FOLDER)
    if filename.endswith(".py")
    and not filename.startswith("__")
    and not filename.endswith("core.py")
]


class BYBCLI(click.MultiCommand):
    """
    The BYBCLI dynamically loads functions from the`byb.bots` module.
    """

    commands = COMMAND_NAMES

    def list_commands(self, ctx):
        return self.commands

    def get_command(self, ctx, name):
        if name not in self.commands:
            raise ValueError(f"Invalid bot name: {name}")

        ns = {}

        fn = os.path.join(COMMANDS_FOLDER, name + ".py")

        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns[COMMAND_METHOD]


main = BYBCLI(help="Bot your brand.")


if __name__ == "__main__":
    main()
