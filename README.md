Open Computing Facility Docker images
========

This repo contains OCF-flavored Docker images. They are built automatically and
hosted on [Docker Hub](https://hub.docker.com/r/theocf/debian/).


## Usage

You can use any of the following:

* `ocf/debian:wheezy`
* `ocf/debian:jessie` (aka `ocf/debian`)
* `ocf/debian:stretch`
* `ocf/debian:sid`

For example, `docker run -ti ocf/debian bash`.


## Making changes

Modify `Dockerfile.in` (never the individual Dockerfiles), then run `make
Dockerfiles`, commit, and push.
