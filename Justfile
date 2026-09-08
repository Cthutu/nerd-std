default:
    just --list

# Test only this repository's standard library.
test:
    python3 tools/nerd.py test mods
    python3 -m unittest discover -s tools -p 'test_*.py'

# Compile an example without opening a window.
build-example example:
    mkdir -p _bin
    python3 tools/nerd.py build -r -o "_bin/{{example}}" "examples/{{example}}/{{example}}.n"

# Build and run an example using the local standard library.
run-example example:
    mkdir -p _bin
    python3 tools/nerd.py run -r -o "_bin/{{example}}" "examples/{{example}}/{{example}}.n"

alias re := run-example
