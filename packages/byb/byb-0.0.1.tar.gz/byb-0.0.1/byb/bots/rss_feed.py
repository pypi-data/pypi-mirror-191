"""TODO: post new rss entries to a platform
"""
import click

from byb.bots.core import platform_opt

@click.command()
@platform_opt
def cli(**kwargs):
    print("TODO")
