---
layout: project
title: This website
image: WB_peak.jpg
description: "This Jekyll-powered site is adapted from my old, pure HTML site"
keywords: "jekyll, github, blog, markdown"
tags: [jekyll, html5, javascript, css]
---

This site was adapted from my [old, static HTML website]({{ root_url }}/old_site).
The old site was beginning to show its age, and it was becoming too difficult to 
maintain.  I didn't create it with any sort of templating to begin with, so if
I ever wanted to change the appearance, my changes had to be manually propogated
to every page.

If only there was some way for me to write the content for each page independent
of it's appearance... Of course I was aware of blogging frameworks like 
wordpress, but these aren't really customizable enough for my tastes -  I wanted to
be in complete control.  Fortunately, I stumbled upon 
[jekyll](http://jekyllrb.com/), a very hackable framework that allows you to 
write content for your pages in markdown, and create the style using CSS and
HTML templates.

Eventually I also found [octopress](http://TODO), another framework built on top 
of jekyll which adds some nice features like a nifty default template and a ruby
plugin architecture.  After adding some plugins (links in the credits below TODO:link),
converting my project pages to markdown, and doing a little customization I was 
off and runing.


Credits
-------
{% githubrepo sotsy/githubrepo-octopress %}

{% githubrepo soupdiver/octopress-soundcloud %}

{% githubrepo optikfluffel/octopress-responsive-video-embed %}
