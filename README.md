# Nerd standard library

An independent standard library for Nerd, with local `core`, `std`, and `os`
modules under `mods/`.

Text and UTF-8 support live in `std.text`: `utf8_decode` and `utf8_validate`,
`Rune.utf8_length`, `Rune.utf8_encode`, and display-width methods on `Rune` and
`string`. The imported `std.utf8` module has been absorbed into this API.

Install Nerd and `just`, then run:

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

All build, run, and test recipes invoke Nerd directly from this repository.
`nerd.json` sets `NERD_LIB_PATH` to `mods`, replacing the compiler's bundled
library path completely, including implicit `core` lookup. Missing local modules
produce a diagnostic. This requires Nerd commit `4010ae22` or later; older
versions allowed installed-library fallback.

For other compiler commands, invoke Nerd from this directory, for example:

```sh
nerd check examples/triangle/triangle.n
```

Frame, OpenGL, UTF-8, time, core, and the two examples were imported from
`Cthutu/nerd` at `c9caeead79f393624cde9fc362cbc1628e278a4b`. Linux X11/GLX and
clock support are exported through the existing `os.linux` folder module.
Windows window/WGL bindings are exported through `os.windows`, with the needed
kernel types, key codes, and timing calls merged into `kernel32` alongside its
existing memory APIs.
