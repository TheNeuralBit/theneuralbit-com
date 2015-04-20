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

SYNTAX = "{% githubrepo [user]/[repo] %}"

GITHUBREPO_REGEX = re.compile(r'^([^\/]*)\/(\S*)')

PROTOTYPE = """<div class="github-widget" data-repo="{user}/{repo}"></div>"""

@LiquidTags.register('githubrepo')
def githubrepo(preprocessor, tag, markup):
    match = GITHUBREPO_REGEX.search(markup)
    url = None
    if match:
        groups = match.groups()
        user = groups[0]
        repo = groups[1]

    return PROTOTYPE.format(user=user, repo=repo)

# ---------------------------------------------------
# This import allows soundcloud tag to be a Pelican plugin
from liquid_tags import register  # noqa
