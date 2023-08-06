# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'cafram'}

packages = \
['cafram', 'paasify']

package_data = \
{'': ['*'],
 'paasify': ['assets/*',
             'assets/collections/paasify/*',
             'assets/collections/paasify/_TITI/*',
             'assets/collections/paasify/_TOTO/*',
             'assets/collections/paasify/debug/*',
             'assets/collections/paasify/dns/*',
             'assets/collections/paasify/dummy/*',
             'assets/collections/paasify/example/*',
             'assets/collections/paasify/home/*',
             'assets/collections/paasify/home/icons/*',
             'assets/collections/paasify/network/*',
             'assets/collections/paasify/proxy/*']}

install_requires = \
['anyconfig>=0.13.0,<0.14.0',
 'giturlparse>=0.10.0,<0.11.0',
 'jsonnet>=0.19.1,<0.20.0',
 'jsonschema>=4.17.0,<5.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'semver>=2.13.0,<3.0.0',
 'sh>=1.14.3,<2.0.0',
 'single-version>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['paasify = paasify.cli:app']}

setup_kwargs = {
    'name': 'paasify',
    'version': '0.1.0a3',
    'description': 'Paasify your docker-compose files',
    'long_description': '<p align=\'center\'>\n<img src="logo/paasify_brand.svg" alt="Paasify">\n</p>\n\n<p align=\'center\'>\n<a href="https://gitter.im/barbu-it/paasify">\n<img src="https://img.shields.io/gitter/room/barbu-it/paasify" alt="Gitter"></a>\n<a href="https://pypi.org/project/paasify/">\n<img src="https://img.shields.io/pypi/v/paasify" alt="PyPI"></a>\n<a href="https://pypistats.org/packages/paasify">\n<img src="https://img.shields.io/pypi/dm/paasify" alt="PyPI - Downloads"></a>\n<a href="https://github.com/barbu-it/paasify/releases">\n<img src="https://img.shields.io/piwheels/v/paasify?include_prereleases" alt="piwheels (including prereleases)"></a>\n<a href="https://github.com/barbu-it/paasify/graphs/code-frequency">\n<img src="https://img.shields.io/github/commit-activity/m/barbu-it/paasify" alt="GitHub commit activity"></a>\n<a href="https://www.gnu.org/licenses/gpl-3.0">\n<img src="https://img.shields.io/badge/License-GPL%20v3-blue.svg" alt="License: GPL v3"></a>\n</p>\n\n<p align="center">\n<img src="https://img.shields.io/pypi/pyversions/paasify" alt="PyPI - Python Version">\n<img src="https://img.shields.io/pypi/format/paasify" alt="PyPI - Format">\n<img src="https://img.shields.io/pypi/status/paasify" alt="PyPI - Status">\n</p>\n\n-------\n\n<p align=\'center\'>\nPlease :star: this project if like it of if you want to support it!\n</p>\n\n<p align=\'center\'>\n:warning: This project is currently in alpha stage, use at your own risks! :warning:\n</p>\n\n<p align=\'center\'>\nOfficial documentation is available on [https://barbu-it.github.io/paasify/]\n</p>\n\n-------\n\n\nDeploy your docker-compose applications with ease and manage your infrastructure as code!\n\nPaasify is a Python tool that will help you to deploy large collections of `docker-compose.yml` files. It\'s an thin overlay to the `docker compose` command\nand it will generate the `docker-compose.yml` you need. It provides some ways to fetch Apps collections, to deploy them and then ensure their state\ncan be committed into version control.\n\n\nFrom an high level perspective, this looks like:\n\n<p align=\'center\'>\n<img src="docs/src/static/overview.svg" alt="Overview">\n</p>\n\n\nThis project try to overstep the missing gap between the docker-compose deployment and static code in way to achieve infrastructure as a code. If you are asking yourself on why you would use Paasify:\n\n* Manage a lot of differents `docker-compose.yml`\n* Make your `docker-compose.yml` based infrastructure [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)\n* Write large collections of `docker-compose.yml` apps once, deploy them many times\n* Integrate your apps into other services, like you can automagically add Traefik labels to your containers\n* Deploy apps in a sequential way\n* Commit your infrastructure configuration into git\n\n\n## :memo: Table of Content\n\n\n  * [Quickstart](#quickstart)\n    + [Installation with pip](#installation-with-pip)\n    + [Installation with docker](#installation-with-docker)\n    + [Usage/Examples](#usage-examples)\n    + [Demo](#demo)\n  * [Overview](#overview)\n    + [Features](#features)\n    + [Documentation](#documentation)\n    + [Requirements](#requirements)\n    + [Environment Variables](#environment-variables)\n  * [Getting help](#getting-help)\n    + [Known issues](#known-issues)\n    + [FAQ](#faq)\n    + [Support](#support)\n    + [Feedback](#feedback)\n  * [Develop](#develop)\n  * [Project information](#project-information)\n\n\n## :fire: Quickstart\n\nThere are different ways to install Paasify:\n\n* [Installation with pip](#installation-with-pip): This is the recommended installation method for people who wants to try and/or develop infrastructure.\n* [Installation with docker](#installation-with-docker): Docker installation is more recommended for production environment.\n* [Installation with git](https://barbu-it.github.io/paasify/develop/install/): If you want to improve or contribute to Paasify itself.\n\n\n### Installation with pip\n\nInstall Paasify with pip:\n\n```bash\npip install paasify\npaasify --help\n```\n\n### Installation with docker\n\nThe idea is to create a simple alias that will call the paasify image:\n\n```bash\nalias paasify=\'docker run --rm -w /work -v $PWD:/work -ti ghcr.io/barbu-it/paasify:latest paasify \'\n\npaasify --help\n```\n\n\n### Usage/Examples\n\nYou need to have docker daemon running. See requirements section for further details. Let\'s try to deploy a Hello World project with paasify. It consists in deploying a proxy, for managing incoming traffic (we uses Traefik here) and a simple page that will list all the services you deployed with paasify.\n\n```bash\npaasify new devbox\ncat <<EOF\n# My new project\n\nsources:\n  - name: community\n    remote: https://github.com/barbu-it/paasify-collection-community\n\nconfig:\n  vars:\n    app_expose_ip: 127.0.0.1\n    app_domain: ${app_expose_ip}.nip.io\n\n  tag_prefix:\n    - homepage\n    - traefik-svc\n\nstack:\n  - app: traefik\n  - app: homepage\n  - app: community:wordpress\n    tags:\n      - phpmyadmin\nEOF\n\npaasify apply\n```\n\nThen you can visit: [http://homepage.127.0.0.1.nip.io](http://homepage.127.0.0.1.nip.io). Of course you can manage your own domains and manage SSL with let\'s encrypt. To have an idea of what app you can install, please checkout official collections:\n\n* [barbu-it/paasify-collection-community](https://github.com/barbu-it/paasify-collection-community): Apps provided for and by the community\n* [barbu-it/paasify-collection-infra](https://github.com/barbu-it/paasify-collection-infra): Dev et devops oriented Apps\n\n\n## :sparkles: Overview\n\n### Features\n\n- Only use the classical syntax of docker compose\n- Allow to use any app without effort\n- Transform your own applications into collection, and publish them as git repositories\n- Allow to centralized collections into git repositories\n- Provides a powerful `docker-compose.<TAG>.yml` assemblage\n- Provides a simple but powerful variable management and templating model\n- Provides jsonnet support for more complex transformations\n- Allow to track your infrastructure changes into git\n\nPlease check the documentation to know more and see the Road Map below to see what\'s coming.\n\n\n### Documentation\n\nThe main documentation website is at [https://barbu-it.github.io/paasify/](https://barbu-it.github.io/paasify/).\n\n### Requirements\n\nThe following system requirements are:\n\n* Linux x86 based OS (not tested yet on other platforms than Linux so far)\n* `docker`\n* `docker compose` or `docker-compose`\n* `jq`\n\nFor development:\n\n* [git](https://git-scm.com/)\n* [poetry](https://python-poetry.org/)\n* [task](https://taskfile.dev/)\n\n### Environment Variables\n\nYou may use the following environment variables to adjust paasify behavior:\n\n`PAASIFY_DEBUG=false`: Show extra log levels if set to `true`\n\n`PAASIFY_TRACE=false`: Show python traces if set to `true`\n\n## :question: Getting help\n\n### Known issues\n\n* Paasify is still at this alpha stage, and not recommended (yet) for production.\n* Paasify has only been tested on Linux, more platform *may* come later.\n* Paasify heavily use the usage of docker labels, so deploying in an existing infrastructure may lead to conflicts.\n\n\n\n### FAQ\n\n#### Does paasify involve any long running services ?\n\nNope, Paasify build your `docker-compose.yml` files and do a `docker compose up`. It\'s a simple CLI program that will super-charge your `docker compose` commands.\n\n#### Is there a web UI for deployments ?\n\nNope, the intended audience of this tool is people who want to do code as infrastructure. It may be the purpose of another project tho.\n\n#### Is it possible to have it in Go?\n\nGo is a pretty good language for this kind of tool, however the author does not known Go, so it\'s too late now. Use the docker image to get a no install setup.\n\n\n### Support\n\nThere is no support outside of community support at this stage of the project. The project is still considered as immature, getting into the project as the date of today may still require you to be comfortable with programming.\n\n\n### Feedback\n\nIf you have any feedback, please open an issue.\n\n\n## :pray: Develop\n\nHere are the basic step to hack into paasify code. A more complete guide is available in the documentation.\n\n### Installation with git\n\nClone the project\n\n```bash\n  git clone https://github.com/barbu-it/paasify\n```\n\nGo to the project directory\n\n```bash\n  cd paasify\n```\n\nInstall dependencies\n\n```bash\n  task install\n```\n\n\n### Running Tests\n\nTo run tests, run the following command\n\n```bash\n  task run_tests\n```\n\nRun the quality suite\n\n```bash\n  task run_qa\n```\n\n### Contributing\n\nContributions are always welcome!\n\nSee `contributing.md` for ways to get started.\n\nPlease adhere to this project\'s `code of conduct`.\n\n\n## :earth_africa: Project information\n\n### Roadmap\n\n- Volume and secret management\n- Docker Swarm support\n\n\n### License\n\n[GNU General Public License v3.0](LICENSE.txt)\n\n### Authors\n\nThis project is brought to you thanks to Barbu-IT.\n\n- [@mrjk](https://www.github.com/mrjk)\n\n\n### Used By\n\nThis project is used by the following companies:\n\n- Barbu-IT\n\n\n### Related\n\nHere are some related projects:\n\n* [Dokku](https://github.com/dokku/dokku)\n\n\n### Support this project\n\nYou can :star: this project, contribute or donate to original author [@mrjk](https://www.github.com/mrjk):\n\n* Bitcoin: `bc1qxdtn24vl9n8e04992dwcq3pdumes0l2dqardvh`\n',
    'author': 'MrJK',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/barbu-it/paasify',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
