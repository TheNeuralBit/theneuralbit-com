"""
Speakerdeck Tag
---------------
This implements a Liquid-style vimeo tag for Pelican,
based on the youtube tag which is in turn based on
the jekyll / octopress youtube tag [1]_

Syntax
------
{% speakerdeck id %}

Example
-------
{% speakerdeck 82b209c0f181013106da6eb14261a8ef %}

Output
------
<script async class="speakerdeck-embed" data-id="82b209c0f181013106da6eb14261a8ef"
 data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
"""
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% speakerdeck id %}"

@LiquidTags.register('speakerdeck')
def speakerdeck(preprocessor, tag, markup):
    speakerdeck_out = """
<script async class="speakerdeck-embed" data-id="{id}"
data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js"></script>
        """.format(id=markup)

    return speakerdeck_out


# ---------------------------------------------------
# This import allows vimeo tag to be a Pelican plugin
from liquid_tags import register  # noqa
