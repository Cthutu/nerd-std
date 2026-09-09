# Nerd standard library

An independent standard library for Nerd, with local `core`, `std`, and `os`
modules under `mods/`.

Text and UTF-8 support live in `std.text`: `utf8_decode` and `utf8_validate`,
`Rune.utf8_length`, `Rune.utf8_encode`, and display-width methods on `Rune` and
`string`. The imported `std.utf8` module has been absorbed into this API.

Install Nerd, Python 3, and `just`, then run:

```sh
just test
just build-example simple_window
just build-example triangle
just run-example simple_window
just re triangle
```

The examples build in release mode into `_bin/`. `simple_window` opens a window;
`triangle` renders a coloured OpenGL triangle. Escape or Q closes either example.
Linux builds need the X11 and OpenGL development libraries (for example,
`libx11-dev` and `libgl-dev` on Debian/Ubuntu); running needs an X11 display and
an OpenGL driver. The Windows backend uses Win32 and WGL.

All build, run, and test recipes use `tools/nerd.py`. It runs from this repo with
the local `nerd.json`, clears `NERD_INSTALL_LIB_PATH`, and copies the compiler
into a temporary directory without bundled modules. This prevents Nerd's
executable-relative module fallback: missing local dependencies fail instead
of silently using the installed standard library. The compiler's native runtime
is still used. Set `NERD_BIN` to select a compiler executable.

For other compiler commands, use the same launcher, for example:

```sh
python3 tools/nerd.py check examples/triangle/triangle.n
```

`nerd.json` also points ordinary Nerd invocations from this directory at `mods`,
but only the launcher disables installed module fallback.

Frame, OpenGL, UTF-8, time, core, and the two examples were imported from
`Cthutu/nerd` at `c9caeead79f393624cde9fc362cbc1628e278a4b`. Linux X11/GLX and
clock support are exported through the existing `os.linux` folder module.
Windows window/WGL bindings are exported through `os.windows`, with the needed
kernel types, key codes, and timing calls merged into `kernel32` alongside its
existing memory APIs.
