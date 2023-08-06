"""Config file parser."""

import logging
import sys
from configparser import ConfigParser, Error
from pathlib import Path


def read_config() -> ConfigParser:
    """Read the config file."""
    parser = ConfigParser()
    try:
        with Path("~/.toisto.cfg").expanduser().open("r", encoding="utf-8") as config_file:
            parser.read_file(config_file)
    except (OSError, Error) as reason:
        logging.warning("Could not read ~/.toisto.cfg: %s", reason)
    if parser.get("commands", "mp3player", fallback=None) is None:
        if "commands" not in parser.sections():
            parser.add_section("commands")
        defaults = dict(darwin="afplay", linux="mpg123 --quiet")
        parser["commands"]["mp3player"] = defaults.get(sys.platform, "playsound")
    return parser
