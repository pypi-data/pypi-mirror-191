import sys
import logging
import argparse
import subprocess

from pathlib import Path

from zxvcv.util import Git, FileStatus
from zxvcv.util import LogManager
from zxvcv.util import ArgsManager
from zxvcv.util import ADict
from zxvcv.util.Path import context_cwd
from zxvcv.util.ArgsManager import ParsePathResolvedArgument

log = logging.getLogger(__name__)


class LocalArgsManager(ArgsManager):
    def get_parser(self) -> argparse.ArgumentParser:
        self.parser.add_argument("--workspace",
            type=Path,
            action=ParsePathResolvedArgument,
            default=Path.cwd(),
            help="""Workspace. Default is cwd."""
        )
        super()._add_logging_arguments(self.parser,
            default_lvl=logging.INFO
        )
        return self.parser

def pull_all(argv=sys.argv[1:]):
    args = LocalArgsManager("zxvcv-pullall").get_parser().parse_args(argv)
    LogManager.setup_logger(__name__, level=int(args.log))
    LogManager.setup_logger("zxvcv.util", level=int(args.log))
    log.debug(f"Script arguments: {args}")

    status = ADict(dct={"done":0, "skipped":0, "failed":0})
    for path in args.workspace.iterdir():
        reset_repo = True

        if not path.is_dir():
            continue
        if str(path).startswith("."):
            continue

        log.info(f"----- REPO: {path}")

        try:
            for _, stat in Git.status(path).items():
                if stat["index"] != FileStatus.UNTRACKED or stat["wtree"] != FileStatus.UNTRACKED:
                    log.warning(f"Skipping, changes in repo: {path.relative_to(args.workspace)}")
                    reset_repo = False
                    break

            if reset_repo:
                Git.checkout("master", path)
                Git.pull(path)
                status.done += 1
            else:
                status.skipped += 1
        except Exception:
            status.failed += 1

    log.info(f"===== SUMMARY: done:{status.done} skipped:{status.skipped} failed:{status.failed}")
