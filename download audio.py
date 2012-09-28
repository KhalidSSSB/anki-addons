# -*- mode: python ; coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
"""
Download audio.

An add-on for Anki 2 srs to download audio from Google TTS and
Japanese audio from Japanesepod.
"""


## If you are learning a language other than Japanese, set the
## default_audio_language_code in the file language.py in the
## downloadaudio folder to the right two-letter code.


import downloadaudio.conflanguage
import downloadaudio.download
