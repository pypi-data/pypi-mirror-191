import sys
import logging
import argparse

from venv import EnvBuilder

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
    args = LocalArgsManager("venv-initalize").get_parser().parse_args(argv)
    LogManager.setup_logger(__name__, level=int(args.log))
    log.debug(f"Script arguments: {args}")

    env_path = _VENVS_PATH/args.name

    if env_path.exists():
        log.error(f"Python Virtual Environment with name '{args.name}' already exist.")
        return

    builder = EnvBuilder(
        system_site_packages=False,
        clear=False,
        symlinks=False,
        upgrade=False,
        with_pip=True,
        prompt=args.name,
        upgrade_deps=True
    )

    builder.create(_VENVS_PATH/args.name)
    log.info(f"Python Virtual Environment created with name '{args.name}'")
