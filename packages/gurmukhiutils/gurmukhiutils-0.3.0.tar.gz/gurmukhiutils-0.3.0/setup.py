# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gurmukhiutils', 'gurmukhiutils.converters']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gurmukhiutils',
    'version': '0.3.0',
    'description': 'Python utilities library for converting, analyzing, and testing Gurmukhi strings',
    'long_description': '# Gurmukhi Utils\n\nPython utilities library for converting, analyzing, and testing Gurmukhi strings. This project is an original work inspired by the JavaScript library [gurmukhi-utils](https://github.com/shabados/gurmukhi-utils).\n\n## WIP\n\nThis library is a work in progress! Note that the API can change unexpectedly when upgrading. It will not be using [SemVer](https://semver.org/) until version 1.0.0. Please do not use for critical projects yet.\n\n## Installation\n\n```shell\npip3 install gurmukhiutils\n```\n\n```shell\npoetry add gurmukhiutils\n```\n\n## Usage\n\nThis is a cursory overview of the functions available. To learn more, see any function\'s docstring in the source code.\n\n**Module `gurmukhiutils.unicode`**\n\n- `unicode` - Converts any ascii gurmukhi characters and sanitizes to unicode gurmukhi. Supports markup language of [Sant Lipi](https://github.com/shabados/SantLipi).\n- `unicode_normalize` - Normalizes Gurmukhi according to Unicode Standards.\n- `sort_diacritics` - Orders the gurmukhi diacritics in a string according to Unicode standards.\n- `sanitize_unicode` - Use single char representations of constructed characters.\n\n**Module `gurmukhiutils.convert`**\n\nConverts text from a script to another. Currently only supports lossless Gurmukhi to Roman transliteration. Gurmukhi to Roman transcription is a WIP.\n\n**Module `gurmukhiutils.remove`**\n\n- `remove` - Removes substrings from string.\n- `remove_regex` - Removes regex patterns from string.\n- `remove_line_endings` - Attempts to remove line endings as best as possible.\n- `remove_vishrams` - Removes all vishram characters.\n\n**`gurmukhiutils.ascii`** - Converts Gurmukhi to ASCII for Open Gurbani Akhar font.\n\n**Example**\n\n```python\n>>> from gurmukhiutils.unicode import unicode\n>>> unicode("gurU")\n\'ਗੁਰੂ\'\n\n>>> from gurmukhiutils.convert import convert\n>>> convert("ਗੁਰੂ")\n\'gurū\'\n```\n\n## Contribute\n\nIf you want to help, please get started with the [CONTRIBUTING.md](./CONTRIBUTING.md) doc.\n\n## Community\n\nThe easiest way to communicate is via [GitHub issues](https://github.com/shabados/viewer/issues). Please search for similar issues regarding your concerns before opening a new issue.\n\nGet organization updates for Shabad OS by following us on [Instagram](https://www.instagram.com/shabad_os/) and [Twitter](https://twitter.com/shabad_os/). We also invite you to join us on our public chat server hosted on [Slack](https://chat.shabados.com/).\n\nOur intention is to signal a safe open-source community. Please help us foster an atmosphere of kindness, cooperation, and understanding. By participating, you agree to abide by the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).\n\nIf you have a concern that doesn\'t warrant opening a GitHub issue, please reach out to us:\n\nBhajneet S.K., Author, Maintainer, Project Lead: [@bhajneet](https://github.com/bhajneet/)\n',
    'author': 'Bhajneet S.K.',
    'author_email': 'bhajneet@gmail.com',
    'maintainer': 'Bhajneet S.K.',
    'maintainer_email': 'bhajneet@gmail.com',
    'url': 'https://github.com/shabados/gurmukhiutils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
