title: GitHub Hash Search
slug: github-hash-search
layout: post
category: projects
tags: probability, python, bash
date: 2018-01-01

A few weeks ago my co-worker issued a challenge to my team as a response to
a random conversation:

> The first one to find one of these as a legitimate commit ID wins:
>
> [https://en.wikipedia.org/wiki/Magic_number_(programming)#Magic_debug_values](https://en.wikipedia.org/wiki/Magic_number_(programming)#Magic_debug_values)

We speculated a little bit about how you might accomplish it - mostly some
varation on "clone some large git repo and grep through the commits", but
quickly shrugged it off. I found myself thinking about it later that day and
couldn't help but really dive into the problem.

Estimating the scale
====================

First I thought a little bit about the scale of the problem - how many git
commits do I need to search before I can reasonably expect one of them to begin
with a magic string?

git uses 160 bit SHA1 hashes for commit IDs so there are $2^{160}$ possible hashes.
I want to find any commit that has a magic string *at the beginning* of
it's hash.  The typical length of the strings is about 7 (hex) characters = 3.5 bytes = **28 bits** so for
each magic string, there are $2^{160-28}$ possible commit hashes that start
with that string.

The probability of any given hash starting with a particular magic string is
$\frac{2^{160-28}}{2^{160}} = 2^{-28}\approx\frac{1}{250\text{ million}}$.
Since I actually have close to 40 different strings that are approximately
7 characters each (of course some are shorter, but I'm only trying to get
a rough estimate here), the probability that a commit hash starts with *some*
magic string is about $\frac{40}{250\text{ million}}$ or about 1 in 6 million.
So if I can somehow collect on the order of 10 million git commit hashes
I should find one of these strings.

I later [wrote a script](https://github.com/TheNeuralBit/github-hash-search/blob/master/hashes_needed.py)
to compute these odds more precisely for a given set of magic strings, and
found that 1 in 7,642,290 hashes should start with one of the magic strings.


Collecting the hashes
=====================

Alright so now where am I going to find around 10 million git commit hashes?
I thought about cloning a few large git repos, like [the linux
kernel](https://github.com/torvalds/linux), but that would require downloading
a ton of actual diff data that I don't care about, and even then the linux
kernel only has 722,647 commits at the time of writing, so I'd need to find 10
or so different repositories of a similar scale.

Before attempting that I poked around in the man pages a bit and found [`git
ls-remote`](https://git-scm.com/docs/git-ls-remote.html). It takes a git
remote url and returns a list of references available on the remote along with
their commit IDs. Here's the output for this website's git repo:

``` sh
$ git ls-remote git@github.com:TheNeuralBit/theneuralbit.git
fb6bac0e6efff6f8f74a35a726a2e411ec00d1ad    HEAD
47e11c77a29862b8875e60aea8c9a755c84c31ee    refs/heads/custom-theme
fe6f73099c2c7a40997c32396eab60c65a5ef06c    refs/heads/git-stash
fb6bac0e6efff6f8f74a35a726a2e411ec00d1ad    refs/heads/master
...
```

Of course the catch is that `ls-remote` only returns commit IDs for
*references* like tags and branches, and most git repos don't have that many
of them, even the linux kernel only has about 2000:

``` sh
$ git ls-remote git@github.com:torvalds/linux.git | wc -l
1977
```

but if I can somehow find a ton of git remotes this might work!

Enter GitHub
============

An obvious source for a large number of git remotes is GitHub. GitHub hosts
about 25 million public repositories[ref]I found this in the [State of the
Octoverse](https://octoverse.github.com/)[/ref], and it has a public
[API](https://developer.github.com/v3/) for accessing them. I wrote a python script
to hit the search API:

``` sh
$ python git_urls.py pie
git@github.com:blazingcloud/pie.git
git@github.com:lipka/piecon.git
git@github.com:SaswatPadhi/PIE.git
git@github.com:coverity/pie.git
git@github.com:apertureless/vue-chartjs.git
git@github.com:bboyairwreck/PieMessage.git
git@github.com:RetroPie/RetroPie-Setup.git
git@github.com:google/pienoon.git
git@github.com:fritzy/pie.git
git@github.com:rendro/easy-pie-chart.git
git@github.com:AndersMalmgren/FreePIE.git
git@github.com:Nikesh/Pie-Menu.git
...
```

Then, used my machine's built-in dictionary to run through every dictionary word:

``` sh
$ cat /usr/share/dict/american-english | grep -v "'" | xargs -I{} python git_urls.py {}
Searching for A...
git@github.com:angular/a.git
git@github.com:fmtn/a.git
git@github.com:heroku/hatchet.git
...
```

Then I ran `git ls-remote` on every remote and collected all the
references (with their commit hashes) in a file.
[`git_all_hashes.sh`](https://github.com/TheNeuralBit/github-hash-search/blob/master/git_all_hashes.sh)
chains all these steps together and generates a `hashes` file with all the
results.  The search API only allows 30 requests per minute which seriously
rate limits the entire process, but at least its fully automated. I let the
script run for several days, and eventually collected 57.8M unique commit
hashes.

Once I'd collected all these results in a file its a simple matter to grep the
results for magic strings... right?


Searching the Results
=====================
I figured searching the results would be relatively easy, and it was at first,
but once I had gigabytes of GitHub commit hashes it started to take
a significant amount of time to search the file.

Initially, I ran my searches with the command:
``` sh
cat hashes_to_find.txt | xargs -P4 -I{} grep ^{} hashes
```
This uses xargs to spawn an independent grep process for each commit hash, and
run up to 4 different searches in parallel.  I eventually realized that this is
a pretty silly approach - each process scans through the entire file
separately, when a single process could easily scan through the file once
searching for every string.

I wrote a second command that does just that. It uses a short python
script to generate a regex of the form
`^facade|^1badb002|^8badf00d|^abababab...`, which is then passed to `grep -E`.

``` sh
$ grep -E `cat hashes_to_find.txt | python -c "import sys; print('|'.join('^' + line.strip() for line in sys.stdin))`"
```

I also investigated using `grep
-F`, a version of grep that uses the
[Aho-Corasick Algorithm](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm)[ref][Wikipedia](https://en.wikipedia.org/wiki/Grep#Variations) has a really useful write-up on the variations of grep[/ref].
Aho-Corasick is supposed to be faster than regex when searching for a set of fixed
length strings, which sounds perfect. Unfortunately, `grep -F` searches for
matches anywhere in the line, and I'm only interested in matches at the
beginning.

I [benchmarked](https://github.com/TheNeuralBit/github-hash-search/blob/master/compare_search_methods.sh)
the different approaches and found that searching with a single `grep -E`
command is about 10x faster on my machine.


Enough! Tell me what you found!
===============================
Ok enough explanation - here's a rundown of the commits that I found.  After
running a GitHub API search for every word in my system's dictionary
I collected 57.8M unique commit hashes. Out of those, I found 12 that begin
with a magic string:

* [akka/akka:**c0ffee**](https://github.com/akka/akka/commit/c0ffee)
* [Neufund/ico-contracts:**c0ffee**](https://github.com/Neufund/ico-contracts/commit/c0ffee)
* [everypolitician/viewer-sinatra:**c0ffee**](https://github.com/everypolitician/viewer-sinatra/commit/c0ffee)
* [nette/nette-minified:**c0ffee**](https://github.com/nette/nette-minified/commit/c0ffeec)
* [afa/ipod-maintain:**c0ffee**](https://github.com/afa/ipod-maintain/commit/c0ffee)
* [bradfitz/deadbeef:**deadbeef**](https://github.com/bradfitz/deadbeef/commit/deadbeef)
* [fsprojects/FSharp.Data.GraphQL:**ebebebeb**](https://github.com/fsprojects/FSharp.Data.GraphQL/commit/ebebebeb)
* [caitlin/cinch-onuwwgame:**facade**](https://github.com/caitlin/cinch-onuwwgame/commit/facade)
* [ajgilbert/ICHiggsTauTau:**facade**](https://github.com/ajgilbert/ICHiggsTauTau/commit/facade)
* [dmitrizzle/Analog.Cafe:**facade**](https://github.com/dmitrizzle/Analog.Cafe/commit/facade)
* [juneryo/tdui:**facade**](https://github.com/juneryo/tdui)[ref]For whatever
  reason I can't link directly do this commit on GitHub. but if you run `git
  ls-remote` on the remote the commit is there[/ref]
* [ipeirotis/Troia-Server:**feedface**](https://github.com/ipeirotis/Troia-Server/commit/feedface)

The astute reader will notice that according to my probability estimate of 1 in
~7.5M I should have found ~7.7 magic strings in this dataset. Obviously the
standard disclaimer applies - we're talking about probabilities here, just because
you saw 10 heads in a row doesn't mean the coin is broken, it means you saw one
strange but equally likely outcome. *Also* my numbers were thrown off a bit
by [bradfitz](https://github.com/bradfitz), who wrote a [go
program](https://github.com/bradfitz/gitbrute) that brute-forces a desired
commit hash. He used it to generate [a commit with the hash
`deadbeef`](https://github.com/bradfitz/deadbeef/commit/deadbeef), which
I found in my search.

Needless to say, I won my co-worker's challenge. Still not sure what the prize
is.
