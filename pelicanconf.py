#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Brian Hulette'
SITENAME = u'the neural bit'
SITESUBTITLE = u'a nerd doing nerdy things and writing about them'
SITEURL = ''
STATIC_PATHS = ['images', 'media', 'code']

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
THEME = "pelican-octopress-theme"
HEADER_IMAGE = "/images/neuron_header.png"

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["render_math", "pelican_gist", "liquid_tags.vimeo", "liquid_tags.sc", "liquid_tags.speakerdeck"]
MATH_JAX = {"color": "#000000"}
SOUNDCLOUD_CLIENT_ID = 'ebb0751100a870643e78012bc3394fe5'
