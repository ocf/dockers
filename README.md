Open Computing Facility Docker images
========

[![Build Status](https://jenkins.ocf.berkeley.edu/buildStatus/icon?job=dockers/master)](https://jenkins.ocf.berkeley.edu/job/dockers/job/master/)

This repo contains OCF-flavored Docker images. They are built automatically and
hosted on [Docker Hub][dockerhub] and on the OCF's internal Docker registry.


## Usage

You can use any of the following:

* `theocf/debian:jessie`
* `theocf/debian:stretch`
* `theocf/debian:buster`
* `theocf/debian:sid`

If you're on the OCF, you probably want to prefix them with
`docker.ocf.berkeley.edu/` in order to use our internal registry.

For example, `docker run -ti docker.ocf.berkeley.edu/theocf/debian:stretch bash`.


## Making changes

Modify `Dockerfile.in` (the template) or `template.py` (contains some
parameters that go into the template for the various base images).

To test, just run `make build`. This will build images with tags prefixed with
your username so that you can do manual testing (if desired).

You should probably never push the images via `make push`; instead, push to
master and let [Jenkins][jenkins] do it for you. It will push the images to
both the public [DockerHub][dockerhub] and our own Docker registry.

You should ideally make a pull request first, which will let Jenkins run the
tests without pushing the resulting images so that you can know before you
break the build.


[dockerhub]: https://hub.docker.com/r/theocf/debian/
[jenkins]: https://jenkins.ocf.berkeley.edu/job/dockers/
