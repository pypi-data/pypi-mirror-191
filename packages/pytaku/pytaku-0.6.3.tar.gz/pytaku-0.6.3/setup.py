# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mangoapi',
 'pytaku',
 'pytaku.database',
 'pytaku.database.migrations',
 'pytaku.scripts']

package_data = \
{'': ['*'],
 'pytaku': ['js-src/*',
            'js-src/routes/*',
            'static/*',
            'static/feathericons/*',
            'static/js/*',
            'static/vendored/*',
            'templates/*']}

install_requires = \
['argon2-cffi>=21,<22',
 'bbcode>=1,<2',
 'flask>=2,<3',
 'goodconf>=1,<2',
 'gunicorn>=20,<21',
 'requests>=2,<3']

entry_points = \
{'console_scripts': ['pytaku = pytaku:serve',
                     'pytaku-collect-static = pytaku:collect_static',
                     'pytaku-dev = pytaku:dev',
                     'pytaku-generate-config = pytaku:generate_config',
                     'pytaku-migrate = pytaku:migrate',
                     'pytaku-scheduler = pytaku:scheduler']}

setup_kwargs = {
    'name': 'pytaku',
    'version': '0.6.3',
    'description': 'Self-hostable web-based manga reader',
    'long_description': 'Live demo: https://pytaku.imnhan.com\n(db may be hosed any time, also expect bugs)\n\nProduction instance coming When It\'s Ready (tm).\n\n# Pytaku [![builds.sr.ht status](https://builds.sr.ht/~nhanb/pytaku/commits/master.svg)](https://builds.sr.ht/~nhanb/pytaku/commits/master?)\n\nPytaku is a WIP web-based manga reader that keeps track of your reading\nprogress and new chapter updates. Its design goals are:\n\n- Self-host friendly - if you have a UNIX-like server with python3.7+ and can\n  run `pip install`, you\'re good.\n\n- Phone/tablet friendly - although I hardly read any webtoons these days so the\n  phone experience may not be as polished.\n\n- KISSFFS, or **K**eep **I**t rea**S**onably **S**imple you **F**-ing\n  architecture/tooling **F**etishi**S**ts! Oftentimes I have enough practice on\n  industrial grade power tools at work so at home I want a change of pace.\n  Flask + raw SQL has been surprisingly comfy. On the other side, mithril.js\n  provides a good baseline of SPA functionality without having to pull in the\n  Rube Goldberg machine that is """modern""" JS devtools.\n\n# Keyboard shortcuts\n\nOn Chapter page, press `?` to show keyboard shortcuts.\n\n# Development\n\n```sh\n## Backend ##\npoetry install\npip install --upgrade pip\npip install https://github.com/rogerbinns/apsw/releases/download/3.34.0-r1/apsw-3.34.0-r1.zip \\\n      --global-option=fetch --global-option=--version --global-option=3.34.0 --global-option=--all \\\n      --global-option=build --global-option=--enable-all-extensions\n# (using apsw 3.34 here to match the version on debian 11)\n\npytaku-generate-config > pytaku.conf.json\n# fill stuff as needed\n\n# run migration script once\npytaku-migrate\n\n# run 2 processes:\npytaku-dev -p 8000  # development webserver\npytaku-scheduler  # scheduled tasks e.g. update titles\n\n\n## Frontend ##\n\nsudo pacman -S entr  # to watch source files\nnpm install -g --prefix ~/.node_modules esbuild # to bundle js\n\n# Listen for changes in js-src dir, automatically build minified bundle:\nfind src/pytaku/js-src -name \'*.js\' | entr -rc \\\n     esbuild src/pytaku/js-src/main.js \\\n     --bundle --sourcemap --minify \\\n     --outfile=src/pytaku/static/js/main.min.js\n```\n\n### Dumb proxy\n\nEventually mangasee started using a somewhat aggressive cloudflare protection\nso cloudscraper alone is not enough (looks like our IP got blacklisted or\nthrottled all the time), so now I have to send requests through a crappy\n[GAE-based proxy](https://git.sr.ht/~nhanb/gae-proxy). You\'ll need to spin up\nyour own proxy instance (Google App Engine free tier is enough for personal\nuse), then fill out OUTGOING_PROXY_NETLOC and OUTGOING_PROXY_KEY accordingly.\n\nYes it\'s not a standards-compliant http(s) proxy so you can\'t just use yours. I\nchose the cheapest (free) way to get a somewhat reliable IP-rotating proxy.\n\n## Tests\n\nCan be run with just `pytest`. It needs a pytaku.conf.json as well.\n\n## Code QA tools\n\n- Python: black, isort, flake8 without mccabe\n- JavaScript: jshint, prettier\n\n```sh\nsudo pacman python-black python-isort flake8 prettier\nnpm install -g --prefix ~/.node_modules jshint\n```\n\n# Production\n\n**Gotcha:** mangasee image servers will timeout if you try to download images\nvia ipv6, so you\'ll need to disable IPv6 on your VM. It\'s unfortunate that\npython-requests [doesn\'t][https://github.com/psf/requests/issues/1691] have an\nofficial way to specify ipv4/ipv6 on its API, and I\'m too lazy to figure out\nalternatives.\n\nI\'m running my instance on Debian 11, but any unix-like environment with these\nshould work:\n\n- python3.7+\n- apsw (on Debian, simply install the `python3-apsw` package)\n- the rest are all pypi packages that should be automatically installed when\n  you run `pip install pytaku`\n\nThe following is a step-by-step guide on Debian 11.\n\n```sh\nsudo apt install python3-pip python3-apsw\npip3 install --user pytaku\n# now make sure ~/.local/bin is in your $PATH so pytaku commands are usable\n\npytaku-generate-config > pytaku.conf.json\n# fill stuff as needed\n\n# run migration script once\npytaku-migrate\n\n# run 2 processes:\npytaku -w 7  # production web server - args are passed as-is to gunicorn\npytaku-scheduler  # scheduled tasks e.g. update titles\n\n# don\'t forget to setup your proxy, same as in development:\n# https://git.sr.ht/~nhanb/gae-proxy\n\n# upgrades:\npip3 install --user --upgrade pytaku\npytaku-migrate\n# then restart `pytaku` & `pytaku-scheduler` processes\n```\n\nIf you\'re exposing your instance to the internet, I don\'t have to remind you to\nproperly set up a firewall and a TLS-terminating reverse proxy e.g.\nnginx/caddy, right?\n\nAlternatively, just setup a personal [tailscale](https://tailscale.com/)\nnetwork and let them worry about access control and end-to-end encryption for\nyou.\n\n## Optional optimization\n\nWith the setup above, you\'re serving static assets using gunicorn, which is not\nideal performance-wise. For private usage this doesn\'t really matter. However,\nif you want to properly serve static assets using nginx and the like, you can\ncopy all static assets into a designated directory with:\n\n```sh\npytaku-collect-static target_dir\n```\n\nThis will copy all assets into `target_dir/static`. You can now instruct\nnginx/caddy/etc. to serve this dir on `/static/*` paths. There\'s an example\ncaddyfile to do this in the ./contrib/ dir.\n\n# LICENSE\n\nCopyright (C) 2021 Bùi Thành Nhân\n\nThis program is free software: you can redistribute it and/or modify it under\nthe terms of the GNU Affero General Public License version 3 as published by\nthe Free Software Foundation.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A\nPARTICULAR PURPOSE.  See the GNU Affero General Public License for more\ndetails.\n\nYou should have received a copy of the GNU Affero General Public License along\nwith this program.  If not, see <https://www.gnu.org/licenses/>.\n',
    'author': 'Bùi Thành Nhân',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
