<span class="purple"> 🤖 <code>byb</code>: bot your brand </purple>
=====================

`byb` is a toolkit for automating the maintenance of our personal brand. with `byb`, we define a set of creative `bots` and point them at `platforms`.

## <span class="blue"> 🛠️ installation / configuration </span>

- clone this repository: `git clone https://github.com/gltd/byb && cd byb`
- open up [`.env.sample`](.env.sample), update with your platform credentials, and save the file as `.env`.
- create a virtual environment: `pipenv shell`
- install the library in "editable" mode for easy devving: `pip3 install -e .`

## <span class="blue"> 🗒️ usage </span>

`byb` is a command line tool constructed using [`click`](https://click.palletsprojects.com/en/7.x/). every `bot` is just a `click` Command, saved in a separate python file under [`byb/bots/`](byb/bots/).

for example [`geocities-archive-crawler`](byb/bots/01_geocities_archive_crawler.py) can be run via `byb bots geocities-archive-crawler`.

you can see all the options for `byb` by running `byb --help`

each bot should add a series of configurable options via `click.option` and a description using a docstring.

## <span class="blue"> 🏁 patterns </blue>

`bots` can do anything. ideally they should create some sort of content (words, images, sounds, experiences, or some combination thereof) and distribute it to one or more `platforms`.

if the desired platform doesn't have a publishing API (e.g. Instagram), we can upload generated content to an intermediate platform, like a [SlackChannel](byb/platforms/slack.py). Upon receiving the message, we manually post the content to the desired platform ourselves.

we can also treat `byb` as purely-suggestive. in this scenario, we would post everything to an intermediate platform and then "curate" the resulting content on other platforms as we see appropriate.

as the number of bots grow, we might begin to make bots which generate content by responding to other bots.

bots should be designed to run on-demand, and not as long-running processes.

bots should not overwhelm, and do not need to post every time they run.

bots should have heuristics for beauty.

## <span class="blue"> 🪞 platforms </span>

`platforms` are outlets for `bots`. `byb` treats `platforms` primarily as content receptacles, but they can also be useful in the content generation process. all interactions with platforms, including methods for _reading_ content, should live in [`byb.platforms`](byb/platforms) in an appropriately named file. this pattern might change over time.
