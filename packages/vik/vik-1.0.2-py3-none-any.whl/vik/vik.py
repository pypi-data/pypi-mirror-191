#!/usr/bin/env python3

import os
import platform
import subprocess
import sys
from importlib import resources
from tempfile import TemporaryDirectory

IS_WINDOWS = platform.system() == "Windows"


def _create_vimrc_file(directory: str) -> str:
    vimrc = resources.files("vik").joinpath(".vimrc").read_text(encoding="utf-8")
    vimrc_path = os.path.join(directory, ".vimrc")
    with open(vimrc_path, "w", encoding="utf-8") as f:
        f.write(vimrc)
    return vimrc_path


def main():
    with TemporaryDirectory() as tmp_dir:
        if len(sys.argv) < 2:
            sys.stderr.write("File not specified\n")
            sys.exit(2)
        vimrc_path = _create_vimrc_file(tmp_dir)
        subprocess.run(["vim", "-u", vimrc_path, sys.argv[1]], shell = IS_WINDOWS)


if __name__  == "__main__":
    main()
