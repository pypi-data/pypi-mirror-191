import os
import sys
import shutil
import logging
import argparse

from pathlib import Path

from zxvcv.util import LogManager
from zxvcv.util import ArgsManager
from zxvcv.cmdutil.virtual_env import _VENVS_PATH

log = logging.getLogger(__name__)


class LocalArgsManager(ArgsManager):
    def get_parser(self) -> argparse.ArgumentParser:
        self.parser.add_argument("name",
            type=str,
            help="""Name for virtual environment."""
        )
        super()._add_logging_arguments(self.parser,
            default_lvl=logging.INFO
        )
        return self.parser

def main(argv=sys.argv[1:]):
    args = LocalArgsManager("venv-remove").get_parser().parse_args(argv)
    LogManager.setup_logger(__name__, level=int(args.log))
    log.debug(f"Script arguments: {args}")

    if "VIRTUAL_ENV" in os.environ and Path(os.environ['VIRTUAL_ENV']).name == args.name:
        log.error(f"Cannot remove active Virtual Environment.")
        return

    env_path = _VENVS_PATH/args.name

    if not env_path.exists():
        log.error(f"Python Virtual Environment with name '{args.name}' not exist.")
        return

    shutil.rmtree(env_path)
    log.info(f"Python Virtual Environment '{args.name}' removed.")
