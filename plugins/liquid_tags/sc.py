"""
Soundcloud Tag
---------
This implements a Liquid-style soundcloud tag for Pelican,
based on the soundcloud API reference [1]_

Syntax
------
{% soundcloud [url] %}

Example
-------
{% soundcloud https://soundcloud.com/brian-hulette/comfortably-numb-synthesis %}

Output
------
<div style="width:640px; height:480px;">
    <iframe
        src="//player.vimeo.com/video/10739054?title=0&amp;byline=0&amp;portrait=0"
        width="640" height="480" frameborder="0"
        webkitallowfullscreen mozallowfullscreen allowfullscreen>
    </iframe>
</div>

[1] https://developers.soundcloud.com/docs/api/guide#playing
"""
import re
import soundcloud
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% sc [url] %}"

SOUNDCLOUD = re.compile(r'(https?\:\/\/.*)')

CLIENT_ID = 'ebb0751100a870643e78012bc3394fe5'

@LiquidTags.register('sc')
def sc(preprocessor, tag, markup):
    match = SOUNDCLOUD.search(markup)
    url = None
    if match:
        groups = match.groups()
        url = groups[0]

    if url:
        client = soundcloud.Client(client_id=CLIENT_ID)
        embed_info = client.get('/oembed', url=url, maxheight=166)
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return embed_info.html


# ---------------------------------------------------
# This import allows soundcloud tag to be a Pelican plugin
from liquid_tags import register  # noqa
