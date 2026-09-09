default:
    just --list

# Test only this repository's standard library.
test:
    nerd test mods

# Compile an example without opening a window.
build-example example:
    mkdir -p _bin
    nerd build -r -o "_bin/{{example}}" "examples/{{example}}/{{example}}.n"

# Build and run an example using the local standard library.
run-example example:
    mkdir -p _bin
    nerd run -r -o "_bin/{{example}}" "examples/{{example}}/{{example}}.n"

alias re := run-example
