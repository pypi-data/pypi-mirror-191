import os
import re

RE_CAMEL_1 = re.compile(r"(.)([A-Z][a-z]+)")
RE_CAMEL_2 = re.compile(r"([a-z0-9])([A-Z])")


def here(f, *args):
    """
    Get the current directory and absolute path of a __file__.
    """
    return os.path.abspath(os.path.join(os.path.dirname(f), *args))


def camel_to_snake(text: str) -> str:
    f"""
    Convert a camel-cased string into a snake_cased string (eg: ``RemoveFlag` -> ``remove_flag``)
    """
    text = RE_CAMEL_1.sub(r"\1_\2", text)
    return RE_CAMEL_2.sub(r"\1_\2", text).lower()
