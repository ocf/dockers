Open Computing Facility Docker images
========

This repo contains OCF-flavored Docker images. They are built automatically and
hosted on [Docker Hub](https://hub.docker.com/r/theocf/debian/).


## Usage

You can use any of the following:

* `theocf/debian:wheezy`
* `theocf/debian:jessie` (aka `theocf/debian`)
* `theocf/debian:stretch`
* `theocf/debian:sid`

For example, `docker run -ti theocf/debian bash`.


## Making changes

Modify `Dockerfile.in` (never the individual Dockerfiles), then run `make
Dockerfiles`, commit, and push.
