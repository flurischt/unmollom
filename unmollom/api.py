# -*- coding: utf-8 -*-

"""
unmollom.api

implements the unmollom API

:copyright: (c) 2013 by Flurin Rindisbacher.
:license: BSD 2-Clause, see LICENSE for more details.
"""

from unmollom.util import *
from unmollom.speech_recognition import *

def solve_url(requests_session, url):
    html = requests_session.get(url).content
    return solve(requests_session, html)

def solve(requests_session, htmlsource):
    url = extract_mollom_audio_file(htmlsource)
    mp3 = requests_session.get(url).content
    speech = recognize(mp3)
    captcha =  build_captcha(speech['text'])
    return captcha