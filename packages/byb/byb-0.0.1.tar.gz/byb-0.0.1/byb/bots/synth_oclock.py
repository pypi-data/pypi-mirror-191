import csv
import logging
import random
import textwrap
from collections import defaultdict
from datetime import datetime

import click
import pytz

from byb.core import Bot, PostContent
from byb.bots.core import platform_opt
from byb.utils.path import here

log = logging.getLogger(__name__)


class SynthOClockBot(Bot):
    def __init__(self, **kw):
        self.config = kw

    def load_synths(self):
        """ """
        self.synths = defaultdict(list)
        for r in csv.DictReader(open(here(__file__, "assets/synths.csv"), "r")):
            self.synths[r["time"]].append(r)

    def synth_for_time(self, dt):
        """ """
        key = dt.strftime("%l%M").strip()
        if key not in self.synths:
            return
        synth = random.choice(self.synths[key])
        synth["am_pm"] = dt.strftime("%p")
        synth["text"] = textwrap.dedent(
            f"""
        it's {synth["name"]} {synth["am_pm"]}.
        .
        .
        .
        .
        #bot #byb #geocitiesarchive #screenshots
        """
        ).lower()
        return synth

    def now(self):
        """ """
        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=pytz.timezone("UTC"))
        tz = pytz.timezone(self.config["timezone"])
        dt = dt.astimezone(tz)
        return dt

    def trigger(self):
        """ """
        return random.choice(range(0, 100)) <= self.config["probability"] * 100

    def generate(self, **kwargs) -> PostContent:
        """ """
        self.config.update(kwargs)
        self.load_synths()
        dt = self.now()
        synth = self.synth_for_time(dt)
        if synth and self.trigger():
            return PostContent(
                media=synth["img"], text=synth["text"], urls=[synth["url"]]
            )
        else:
            log.info(f"No synth for for {dt}")


@click.command()
@click.option("--timezone", default="US/Eastern", help="The timezone to check against.")
@click.option(
    "--probability",
    default=0.1,
    help="The probability that this bot will publish content.",
)
@platform_opt
def cli(**kwargs):
    """
    Post an image of a synthesizer at a time that matches its name, eg 8:08 pm.
    """
    SynthOClockBot().post_content_to_platforms(**kwargs)
