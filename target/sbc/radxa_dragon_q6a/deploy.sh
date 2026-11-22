#!/bin/sh
# Stage the target package on the Q6A and keep captures and local builds.
set -eu
host=${Q6A:-radxa@radxa-dragon-q6a.local}
case "${1:-}" in ""|cam1|cam2|cam3|--*) ;; *) host=$1; shift;; esac
port=cam2
case "${1:-}" in cam1|cam2|cam3) port=$1; shift;; esac
replace=
if [ "${1:-}" = "--replace" ]; then replace=" --replace"; shift; fi
if [ "$#" -gt 0 ]; then echo "deploy.sh [ssh-host] [cam1|cam2|cam3] [--replace]" >&2; exit 2; fi
dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
stage=$(ssh -- "$host" 'mkdir -p ~/q6a-ar0234 && cd ~/q6a-ar0234 && mktemp -d .incoming.XXXXXXXX')
case "$stage" in .incoming.????????) ;; *) echo "Некорректное имя временного каталога" >&2; exit 1;; esac
case "$stage" in *[!a-zA-Z0-9.]*) exit 1;; esac
trap 'ssh -- "$host" "rm -rf -- ~/q6a-ar0234/$stage" </dev/null || :' EXIT
# Explicit package contents exclude build/, vendor/, captures and validation logs.
cd "$dir"
scp -r -- install.py replacement.py ports.py capture.py Makefile sources.json LICENSE.* overlay tools demo \
    "${host}:q6a-ar0234/$stage/"
ssh -t -- "$host" "cd ~/q6a-ar0234 && flock .deploy.lock sh -ec 'cd $stage && sudo python3 -B install.py --port $port$replace && cp -R ./* ..'"
