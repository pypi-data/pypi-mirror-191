# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resume_pycli']

package_data = \
{'': ['*'],
 'resume_pycli': ['themes/base/*',
                  'themes/flat/*',
                  'themes/flat/static/bootstrap/css/*',
                  'themes/flat/static/bootstrap/fonts/*',
                  'themes/flat/static/bootstrap/js/*',
                  'themes/flat/static/octicons/*',
                  'themes/stackoverflow/*',
                  'themes/stackoverflow/partials/*',
                  'themes/stackoverflow/static/css/*',
                  'themes/stackoverflow/static/webfonts/*']}

install_requires = \
['beautifulsoup4', 'flask', 'jsonschema', 'typer[all]']

extras_require = \
{'playwright': ['playwright'], 'weasyprint': ['weasyprint']}

entry_points = \
{'console_scripts': ['resume = resume_pycli.cli:app',
                     'resumepy = resume_pycli.cli:app']}

setup_kwargs = {
    'name': 'resume-pycli',
    'version': '4.1.0',
    'description': 'CLI tool to easily setup a new resume',
    'long_description': '# resume-pycli\n\nCLI tool to build a beautiful resume from a [JSON\nResume](https://jsonresume.org/) file.\n\nThis is a Python port of\n[resume-cli](https://github.com/jsonresume/resume-cli).\n\n[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/resume-pycli)](https://libraries.io/pypi/resume-pycli)\n[![PyPI Version](https://img.shields.io/pypi/v/resume-pycli?color=4DC71F&logo=python&logoColor=fff)](https://pypi.org/project/resume-pycli/)\n\n## Features\n\n* Validate your `resume.json` against schema\n* Export your resume to HTML\n* Export your resume to PDF\n* Customize the theme of your HTML and PDF exports\n* Run a local HTTP server to preview the HTML export\n* Create an inital `resume.json` with placeholder values to get started\n\n## Installation\n\nWith [pipx](https://pipxproject.github.io/pipx/):\n\n```\npipx install resume-pycli\n```\n\n## Usage\n\n```\nUsage: resume [OPTIONS] COMMAND [ARGS]...\n\n  CLI tool to easily setup a new resume.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  export    Export to HTML and PDF.\n  init      Initialize a resume.json file.\n  serve     Serve resume.\n  validate  Validate resume\'s schema.\n  version   Show application version.\n```\n\nExport your resume with a custom theme, for exemple one located in\n`./themes/my-beautiful-theme`:\n\n```\nresume export --theme my-beautiful-theme\n```\n\nIf you want to export custom version of your resume, for example a shorter one\nlocated at `./resume.short.json`, to PDF only:\n\n```\nresume export --resume resume.short.json --pdf\n```\n\n## Themes\n\nYou can put your theme in `themes/<name>` next to your `resume.json` file. It\nuses [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) as templating engine.\nTake a look at the [included\nthemes](https://github.com/nikaro/resume-pycli/tree/main/resume_pycli/themes/base)\nthat you can take as example to write your own.\n\nSince it uses Jinja, it is not compatible with ["official" community\nthemes](https://jsonresume.org/themes/).\n',
    'author': 'Nicolas Karolak',
    'author_email': 'nicolas@karolak.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nikaro/resume-pycli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
