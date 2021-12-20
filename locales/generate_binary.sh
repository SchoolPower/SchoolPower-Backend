#!/bin/bash
# Generates a base.mo file for the base.po file of each locale,
# using python3's implementation of GNU msgfmt https://github.com/python/cpython/blob/main/Tools/i18n/msgfmt.py
for locale in */; do
  python3 msgfmt.py -o "$locale/LC_MESSAGES/base.mo" "$locale/LC_MESSAGES/base.po"
done
