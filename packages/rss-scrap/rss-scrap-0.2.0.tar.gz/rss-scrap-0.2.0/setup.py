# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['torss', 'torss.feeds']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'beautifulsoup4>=4.9.0,<5.0.0']

entry_points = \
{'console_scripts': ['rss-scrap = torss.app:main']}

setup_kwargs = {
    'name': 'rss-scrap',
    'version': '0.2.0',
    'description': 'Web scrapper which converts sites to RSS feeds.',
    'long_description': '# RSS Scrap\n\nrss-scrap is a command line utility which scraps contents of web pages and\nconverts them to RSS feeds. Specific web scrapers must be implemented for\neach page.\n\nrss-scrap works asynchronously, meaning that many web pages can be scraped\nsimultaneously.\n\nCurrently scraping for the following pages is implemented:\n\n- The Economist, World This Week section\n- Wikipedia Current Events\n- Warnings of Główny Inspektorat Sanitarny (Polish Government Agency)\n',
    'author': 'Michal Goral',
    'author_email': 'dev@goral.net.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.goral.net.pl/mgoral/rss-scrap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
