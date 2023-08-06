# Gurmukhi Utils

Python utilities library for converting, analyzing, and testing Gurmukhi strings. This project is an original work inspired by the JavaScript library [gurmukhi-utils](https://github.com/shabados/gurmukhi-utils).

## WIP

This library is a work in progress! Note that the API can change unexpectedly when upgrading. It will not be using [SemVer](https://semver.org/) until version 1.0.0. Please do not use for critical projects yet.

## Installation

```shell
pip3 install gurmukhiutils
```

```shell
poetry add gurmukhiutils
```

## Usage

This is a cursory overview of the functions available. To learn more, see any function's docstring in the source code.

**Module `gurmukhiutils.unicode`**

- `unicode` - Converts any ascii gurmukhi characters and sanitizes to unicode gurmukhi. Supports markup language of [Sant Lipi](https://github.com/shabados/SantLipi).
- `unicode_normalize` - Normalizes Gurmukhi according to Unicode Standards.
- `sort_diacritics` - Orders the gurmukhi diacritics in a string according to Unicode standards.
- `sanitize_unicode` - Use single char representations of constructed characters.

**Module `gurmukhiutils.convert`**

Converts text from a script to another. Currently only supports lossless Gurmukhi to Roman transliteration. Gurmukhi to Roman transcription is a WIP.

**Module `gurmukhiutils.remove`**

- `remove` - Removes substrings from string.
- `remove_regex` - Removes regex patterns from string.
- `remove_line_endings` - Attempts to remove line endings as best as possible.
- `remove_vishrams` - Removes all vishram characters.

**`gurmukhiutils.ascii`** - Converts Gurmukhi to ASCII for Open Gurbani Akhar font.

**Example**

```python
>>> from gurmukhiutils.unicode import unicode
>>> unicode("gurU")
'ਗੁਰੂ'

>>> from gurmukhiutils.convert import convert
>>> convert("ਗੁਰੂ")
'gurū'
```

## Contribute

If you want to help, please get started with the [CONTRIBUTING.md](./CONTRIBUTING.md) doc.

## Community

The easiest way to communicate is via [GitHub issues](https://github.com/shabados/viewer/issues). Please search for similar issues regarding your concerns before opening a new issue.

Get organization updates for Shabad OS by following us on [Instagram](https://www.instagram.com/shabad_os/) and [Twitter](https://twitter.com/shabad_os/). We also invite you to join us on our public chat server hosted on [Slack](https://chat.shabados.com/).

Our intention is to signal a safe open-source community. Please help us foster an atmosphere of kindness, cooperation, and understanding. By participating, you agree to abide by the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).

If you have a concern that doesn't warrant opening a GitHub issue, please reach out to us:

Bhajneet S.K., Author, Maintainer, Project Lead: [@bhajneet](https://github.com/bhajneet/)
