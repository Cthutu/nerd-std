"""Integration check that installed Nerd modules cannot hide missing imports."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent


class LocalLibraryTests(unittest.TestCase):
    def test_installed_module_fallback_is_disabled(self):
        compiler = shutil.which(os.environ.get("NERD_BIN", "nerd"))
        self.assertIsNotNone(compiler, "Install nerd or set NERD_BIN")
        with tempfile.TemporaryDirectory(prefix="nerd-install-test-") as directory:
            installation = Path(directory) / "installation"
            modules = installation / "mods"
            modules.mkdir(parents=True)
            executable = installation / Path(compiler).name
            shutil.copy2(compiler, executable)
            (modules / "fallback_probe.n").write_text("pub value :: 42\n")
            source = Path(directory) / "probe.n"
            source.write_text(
                "use fallback_probe\nmain :: fn () { assert value == 42 }\n"
            )
            env = os.environ.copy()
            env["NERD_BIN"] = str(executable)
            env["NERD_INSTALL_LIB_PATH"] = str(modules)
            arguments = ["check", str(source)]

            # Ordinary Nerd can find the fake installed module.
            direct = subprocess.run(
                [str(executable), "--config", str(ROOT / "nerd.json"), *arguments],
                cwd=ROOT, env=env, capture_output=True, text=True,
            )
            self.assertEqual(direct.returncode, 0, direct.stdout + direct.stderr)

            # The local launcher must reject the same import, even when invoked
            # outside the repository with an inherited install-library path.
            isolated = subprocess.run(
                [sys.executable, str(ROOT / "tools/nerd.py"), *arguments],
                cwd=directory, env=env, capture_output=True, text=True,
            )
            self.assertNotEqual(isolated.returncode, 0)
            self.assertIn("known module", isolated.stdout + isolated.stderr)
            self.assertIn("fallback_probe", isolated.stdout + isolated.stderr)


if __name__ == "__main__":
    unittest.main()
