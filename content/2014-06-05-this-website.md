title: This website
slug: this-website
layout: project
tags: jekyll, html5, javascript, css


This site was adapted from my [old, static HTML website]({filename}/old_site).
I wrote the original site way back in high school (with many updates throughout
college), and it was beginning to show its age.  The biggest issue was that I
didn't create it with any sort of templating to begin with, so when I wanted to
update the appearance, my changes had to be manually propogated to every page.
Enter [jekyll](http://jekyllrb.com/) and [octopress](http://octopress.org).

<!--more-->

I knew for a long time that I needed some kind of templating engine for my
webpage so I could separate the appearance from the content. Unfortunately, I
was only aware of things like Wordpress, which really didn't give me the control I
wanted - I wanted to be able to open up the tool, try things out, and generally
just hack around. Fortunately, I eventually stumbled upon
[jekyll](http://jekyllrb.com/), a very hackable framework that allows you to
write content for your pages in markdown, and create the style using CSS and
HTML templates.

A little while after I started playing with jekyll, I also found
[Octopress](http://octopress.org), another framework built on top of jekyll
which adds some nice features like a nifty default template and a ruby plugin
architecture.  Once I saw that Octopress calls itself "A blogging framework for
hackers," I knew I'd found what I needed. I converted my original project pages
to markdown with the help of [heck yes markdown](http://heckyesmarkdown), added
some [plugins](#plugins), created a custom page just to list my
[projects]({filename}/projects), and I was good to go.

This is by no means the final iteration of this site, I fully intend to continue
to fiddle with my templates and try out new things. After all, why bother using
a templating engine if you don't ever change the templates?

<a name="plugins"></a>
Plugins
-------
{% githubrepo sotsy/githubrepo-octopress %}

<br/>

{% githubrepo soupdiver/octopress-soundcloud %}

<br/>

{% githubrepo optikfluffel/octopress-responsive-video-embed %}
