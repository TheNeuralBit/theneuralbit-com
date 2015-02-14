#!/usr/bin/env python
# jek2pely.py (C)2012 by Jan-Piet Mens
# Quick and very dirty experimental hack to convert Jekyll .markdown posts to
# a format recognized by Pelican. (Whether or not I'll be using this, I
# don't know, but Pelican does look nice ... :-)
#
# Jekyll uses a header like:
#
#  |---
#  |title: 'An action plugin for Ansible to handle SSH host keys and DNS SSHFP records'
#  |date: 2012-11-03 15:06:12
#  |published: true
#  |expires: never
#  |post_id: 4052
#  |layout: post
#  |tags:
#  | - DNS
#  | - Ansible
#  |---
#
# Pelican needs: (slug and some of the others not required, but *I* want them)
#
#  |title: An action plugin for Ansible to handle SSH host keys and DNS SSHFP records
#  |slug: an-action-plugin-for-ansible-to-handle-ssh-host-keys
#  |layout: post
#  |expires: never
#  |post_id: 4052
#  |published: True
#  |date: 2012-11-03 15:06:12
#  |tags: DNS, Ansible

import sys, os
import yaml
import re
from codecs import open

_HI_START = re.compile(r"\{%(\s+)?highlight\s+([^\s]+)(\s+)?%\}")
_HI_END   = re.compile(r"{%(\s+)?endhighlight(\s+)?%}")
_MEDIADIR = re.compile(r"\{\{(\s+)?site.mediadirectory(\s+)?\}\}")

def convert(filename, slug):

    slurp = False
    new_lines=[]
    header = []
    post = []

    header.append('---')
    header.append("slug: %s" % (slug))


    for l in open(filename, encoding='utf-8').readlines()[1:]:
        l = l.rstrip()
        if l == '---':
            slurp = True
            continue

        if slurp == False:
            header.append(l)
        else:
            if _MEDIADIR.search(l):
                l = _MEDIADIR.sub("|filename|", l)


            if _HI_START.search(l):
                s =_HI_START.sub("```" + r"\2", l)
                new_lines.append(s)
            elif _HI_END.search(l):
                new_lines.append('```')
            else:
                new_lines.append(l)

    hdr = yaml.load("\n".join(header))
    # print hdr

    for k in ['title', 'slug', 'layout', 'expires', 'snippet', 'post_id', 'published', 'date', 'tags']:
        if k != 'tags' and k in hdr:
            post.append("%s: %s" % (k, hdr[k]))
        elif k == 'tags' and 'tags' in hdr:
            post.append("%s: %s" % (k, ', '.join(hdr[k])))

    post.append("")   # separate headers and content


    for n in new_lines:
        post.append(n)

    return post

dirname = '/Users/jpm/Auto/sites/jpmens.net/_posts'
newdir = 'content/import'

for filename in os.listdir(dirname):

    print filename

# Use original filename as slug because some of the titles don't map to slugs
# and I have links to the slug'ed filenames

    slug = filename[11:]    # 2012-11-09-
    if slug.endswith('.markdown'):
        slug = slug[:-len('.markdown')]

    post = convert(dirname + '/' + filename, slug)

    f = open(newdir + '/' + filename, 'w', encoding='utf-8')

    f.writelines("\n".join(post))
    f.close()
