import sys
import logging
import argparse

from zxvcv.util import LogManager
from zxvcv.util import ArgsManager
from zxvcv.cmdutil.virtual_env import _VENVS_PATH

log = logging.getLogger(__name__)


class LocalArgsManager(ArgsManager):
    def get_parser(self) -> argparse.ArgumentParser:
        super()._add_logging_arguments(self.parser,
            default_lvl=logging.INFO
        )
        return self.parser

def main(argv=sys.argv[1:]):
    args = LocalArgsManager("venv-list").get_parser().parse_args(argv)
    LogManager.setup_logger(__name__, level=int(args.log))
    log.debug(f"Script arguments: {args}")

    _VENVS_PATH.mkdir(parents=True, exist_ok=True)

    print("Available Python Virtual Environments:")
    for path in _VENVS_PATH.iterdir():
        print("  " + path.name)
