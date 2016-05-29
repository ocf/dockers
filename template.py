#!/usr/bin/env python3
import re
import shutil
from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader


DEFAULT_IMAGE_OPTIONS = {
    'dumb_init_version': '1.0.2',
    'packages': {
        'ca-certificates',
        'curl',
        'htop',
        'net-tools',
        'sudo',
        'vim-tiny',
        'libnss-ldap',
    },
    'ldap': True,
}

IMAGES = {
    'debian:jessie': {
        'base': 'debian:jessie',
        'ocf_apt_repo_dist': 'jessie',
    },
    'debian:stretch': {
        'base': 'debian:stretch',
    },
    'debian:sid': {
        'base': 'debian:sid',
    },
}


if __name__ == '__main__':
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('Dockerfile.in')

    for tag, params in IMAGES.items():
        assert re.match(r'^[a-z\-:]+$', tag), tag
        p = Path(tag)
        if p.is_dir():
            shutil.rmtree(str(p))

        shutil.copytree('include', str(p))
        with (p / 'Dockerfile').open('w') as f:
            f.write(template.render(**dict(DEFAULT_IMAGE_OPTIONS, **params)) + '\n')
