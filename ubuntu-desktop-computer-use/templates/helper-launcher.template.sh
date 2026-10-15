#!/bin/sh
# Copy to an owned per-user launcher and change only HELPER below.
# Select the current matching helper explicitly; never guess an install path.
# This exports persistence inside the child, after host environment filtering.
set -eu

# CONFIGURATION: an absolute executable path discovered on this machine.
HELPER='/absolute/path/to/computer-use-linux'

case "$HELPER" in
    /absolute/path/to/computer-use-linux)
        printf '%s\n' 'Configure HELPER before using this launcher.' >&2
        exit 2
        ;;
    /*) ;;
    *)
        printf '%s\n' 'HELPER must be an absolute executable path.' >&2
        exit 2
        ;;
esac

if [ ! -f "$HELPER" ] || [ ! -x "$HELPER" ]; then
    printf '%s\n' 'The selected helper is unavailable.' >&2
    exit 2
fi

export COMPUTER_USE_LINUX_PERSIST_REMOTE_DESKTOP=1
exec "$HELPER" "$@"
