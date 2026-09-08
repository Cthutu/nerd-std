#!/usr/bin/env python3
"""Run Nerd against this repository without installed module fallbacks."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    compiler = shutil.which(os.environ.get("NERD_BIN", "nerd"))
    if compiler is None:
        sys.exit("Nerd compiler not found; install nerd or set NERD_BIN.")

    # Nerd also searches beside its executable, even with NERD_LIB_PATH set.
    # A real copy (not a symlink) prevents access to its bundled mods directory.
    with tempfile.TemporaryDirectory(prefix="nerd-std-") as directory:
        executable = Path(directory) / Path(compiler).name
        shutil.copy2(compiler, executable)
        env = os.environ.copy()
        env["NERD_LIB_PATH"] = str(root / "mods")
        env["NERD_INSTALL_LIB_PATH"] = ""
        result = subprocess.run(
            [str(executable), "--config", str(root / "nerd.json"), *sys.argv[1:]],
            cwd=root,
            env=env,
        )
        return result.returncode


if __name__ == "__main__":
    sys.exit(main())
