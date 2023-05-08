#!/usr/bin/env python3
"""Build and optionally push images."""
import argparse
import re
import shutil
import subprocess
from pathlib import Path

from ocflib.misc.shell import bg_green
from ocflib.misc.shell import bg_yellow
from ocflib.misc.whoami import current_user
from jinja2 import Environment
from jinja2 import FileSystemLoader


def report(line, color=bg_yellow):
    print(color(line))


DEFAULT_IMAGE_OPTIONS = {
    'dumb_init_version': '1.2.5',
    'packages': {
        'ca-certificates',
        'curl',
        'gnupg',
        'heimdal-clients',
        'htop',
        'ldap-utils',
        'less',
        'libnss-ldap',
        'libsasl2-modules',
        'libsasl2-modules-gssapi-mit',
        'locales',
        'net-tools',
        'man-db',
        'manpages',
        'procps',
        'ssmtp',
        'sudo',
        'vim-tiny',
    },
    'ldap': True,
    'kerberos': True,
    'mail': True,
    'utils': True,
}

IMAGES = {
    'debian:stretch': {
        'base': 'debian:stretch',
        'ocf_apt_repo_dist': 'stretch',
        'backport_dist': 'stretch-backports',
    },
    'debian:buster': {
        'base': 'debian:buster',
        'ocf_apt_repo_dist': 'buster',
        'backport_dist': 'buster-backports',
    },
    'debian:bullseye': {
        'base': 'debian:bullseye',
        'ocf_apt_repo_dist': 'bullseye',
        'backport_dist': 'bullseye-backports',
    },
    'debian:bullseye-3.7': {
        'base': 'python:3.7-bullseye',
        'ocf_apt_repo_dist': 'bullseye',
        'backport_dist': 'bullseye-backports',
    }
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--push',
        default=False,
        action='store_true',
        help=(
            "Push images to DockerHub and OCF's internal registry. "
            'With this option, --no-cache is used to ensure we avoid stale layers. '
            'This will require you to be logged in with `docker login`.'
        ),
    )
    args = parser.parse_args()

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('Dockerfile.in')

    build = Path('build')
    if not build.is_dir():
        build.mkdir()

    for tag, params in IMAGES.items():
        report('Templating out {}'.format(tag))
        assert re.match(r'^[a-z\-:]+$', tag), tag
        p = build / tag
        if p.is_dir():
            shutil.rmtree(str(p))

        shutil.copytree('include', str(p))
        with (p / 'Dockerfile').open('w') as f:
            f.write(template.render(**dict(DEFAULT_IMAGE_OPTIONS, **params)) + '\n')

        temp_tag = '{}-test-{}'.format(current_user(), tag)
        report('Building {} (as {})'.format(tag, temp_tag))
        subprocess.check_call(
            ('docker', 'build') +
            (('--no-cache',) if args.push else ()) +
            ('-t', temp_tag, str(p))
        )
        report(
            'Successfully built {} (as {})'.format(tag, temp_tag),
            color=bg_green,
        )

        if args.push:
            for new_tag in ('theocf/{}', 'docker-push.ocf.berkeley.edu/theocf/{}'):
                new_tag = new_tag.format(tag)
                report('Tagging {} as {} for push'.format(temp_tag, new_tag))
                subprocess.check_call((
                    'docker', 'tag', temp_tag, new_tag,
                ))
                subprocess.check_call((
                    'docker', 'push', new_tag,
                ))
                report('Sucessfully pushed {}'.format(new_tag), color=bg_green)
    report('All images built!', color=bg_green)
