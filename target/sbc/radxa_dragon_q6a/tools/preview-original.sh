#!/bin/sh
set -eu
exec cam -c 1 -s width=1920,height=1200 --capture --sdl
