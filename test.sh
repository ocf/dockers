#!/bin/bash
# Make sure the Docker images can build and execute a simple command.
set -euo pipefail

find . -mindepth 1 -maxdepth 1 -type d ! -name 'include' ! -name '.git*' |
    while read d; do
        d=$(basename "$d")
        tag="${USER}-docker-${d}"
        echo "Testing ${d} with tag ${tag}:"
        docker build -t "$tag" "$d"
        output=$(docker run --rm "$tag" echo 'hello')

        if [[ "$output" != "hello" ]]; then
            echo "Expected output 'hello', got output '$output'."
            exit 1
        fi
    done
