# -*- coding: utf-8 -*-
# ...
import keen
import os
# available languages

SUPPORTED_LANGUAGES = {'it': 'Italiano', 'de': 'Deutsch'}
BABEL_DEFAULT_LOCALE = 'it'
BABEL_DEFAULT_TIMEZONE = 'UTC'

WTF_CSRF_ENABLED = False

KEEN_PROJECT_ID = os.environ.get('KEEN_PROJECT_ID')
KEEN_WRITE_KEY = os.environ.get('KEEN_WRITE_KEY')