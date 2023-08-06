# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixations']

package_data = \
{'': ['*'],
 'fixations': ['fix_repository_2010_edition_20200402/*',
               'fix_repository_2010_edition_20200402/FIX.4.0/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.1/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.2/*',
               'fix_repository_2010_edition_20200402/FIX.4.2/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.3/Base/*',
               'fix_repository_2010_edition_20200402/FIX.4.4/Base/*',
               'fix_repository_2010_edition_20200402/FIX.5.0/Base/*',
               'fix_repository_2010_edition_20200402/FIX.5.0SP1/Base/*',
               'fix_repository_2010_edition_20200402/FIX.5.0SP2/Base/*',
               'fix_repository_2010_edition_20200402/FIXT.1.1/Base/*',
               'fix_repository_2010_edition_20200402/Unified/*',
               'fix_repository_2010_edition_20200402/schema/*',
               'fix_repository_2010_edition_20200402/xsl/*',
               'templates/*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'flask>=2.2.2,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pytest>=7.2.0,<8.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'termcolor>=2.1.1,<3.0.0',
 'urwid>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['fix_parse_log = fixations.fix_parse_log:main',
                     'fix_tags = fixations.fix_tags:main',
                     'webfix = fixations.webfix:main']}

setup_kwargs = {
    'name': 'fixations',
    'version': '0.2.12',
    'description': 'This is a set of tools to look up / visualize FIX protocol data',
    'long_description': '# FIXations!\n## A set of tools to handle FIX protocol data\n - **fix_tags** - _explore FIX tags and their associated values either as CLI output or a GUI-like textual interface_\n - **fix_parse_log** - _extract FIX lines from a (log) file and present them in a nicely formatted grid_\n - **webfix** - _present copy-n-paste\'d FIX lines into a nicely formatted grid_\n\n### Installation\n`pip3 install fixations`\n\n### Examples of running these applications\n#### fix_tags\n_Click on the link below since it was too small to asciicast in this page_\n[![asciicast](https://asciinema.org/a/551910.svg)](https://asciinema.org/a/551910?autoplay=1&t=2)\n\n#### fix_parse_log\n![fix_parse_log_demo](images/fix_parse_log_demo.gif)\n\n#### webfix\nWebfix needs to be used with either Flask (for dev purposes) \n```commandline\n$ python -m flask --app fixations.webfix run\n * Serving Flask app \'fixations.webfix\'\n * Debug mode: off\nWARNING: This is a development server. Do not use it in a production deployment. \nUse a production WSGI server instead.\n * Running on http://127.0.0.1:5000\nPress CTRL+C to quit\n```\n\nor something like gunicorn (or other WSGI servers) for production uses:\n```commandline\n$ gunicorn fixations.wsgi:app\n[2023-01-16 19:55:31 -0500] [3380019] [INFO] Starting gunicorn 20.1.0\n[2023-01-16 19:55:31 -0500] [3380019] [INFO] Listening at: http://127.0.0.1:8000 (3380019)\n[2023-01-16 19:55:31 -0500] [3380019] [INFO] Using worker: sync\n[2023-01-16 19:55:31 -0500] [3380028] [INFO] Booting worker with pid: 3380028\n```\n\n![webfix_session](images/webfix_session.png)\n\n\n## FIX reference data source\nThe data is extracted from the FIX specs available here: \n\n> https://www.fixtrading.org/packages/fix-repository-2010/ \n(see fix_repository_2010_edition_20200402.zip).\n\nNOTE: it requires the creation of a login/password to access it.\n\n## TODO:\n 1. create hyperlink to FIX specs for each tag based on FIX version\n 2. [DONE] add more info to README.md. Use rule80A and 47 as example for fix_args\n 3. add more example(s)\n 4. add some pytest to detect the FIX version for example\n 5. add "direction" to columns to show whether it\'s a request or a response\n 6. catch exceptions and display them into the webpage\n 7. deploy to https://vercel.com/\n 8. allow to create an ASCII table equivalent suitable to be cut-n-paste into a document for exanple\n 9. [DONE] add shortlink ala tinyurl and save it into a sqlite3 db store\n 10. black theme?\n 11. [DONE] allow to have no leading timestamp and use the timestamp FIX tags instead\n 12. add proper Logger\n 13. add DB stats\n 14. pypi.org can\'t display the ASCII screencast images. Need to reference github full path?\n\n',
    'author': 'Jerome Provensal',
    'author_email': 'jeromegit@provensal.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jeromegit/fixations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
