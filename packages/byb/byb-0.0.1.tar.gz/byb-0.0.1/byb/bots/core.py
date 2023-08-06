import click

from byb.platforms import get_platform

platform_opt = click.option(
    "--platforms",
    default=None,
    type=lambda x: [get_platform(p.strip()) for p in x.split(",")],
    help="A list of valid `bybe.core.Platform` names to post content to.",
)
