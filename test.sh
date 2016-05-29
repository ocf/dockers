#!/bin/bash -eu
# Make sure the Docker images can build and execute a simple command.
set -o pipefail

find . -mindepth 1 -maxdepth 1 -type d ! -name '.git*' |
    while read d; do
        tag="${USER}-docker-${d}"
        echo "Testing ${d} with tag ${tag}:"
        docker build -t "$tag" "$d"
        output=$(docker run --rm "$tag" echo 'hello')

        if [[ "$output" != "hello" ]]; then
            echo "Expected output 'hello', got output '$output'."
            exit 1
        fi
    done
