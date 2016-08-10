title: Fun with git stash
slug: fun-with-git-stash
layout: post
category: blog
tags: cli, git, stash
date: 2016-08-10

If you're anything like me, the only times you've ever used `git stash` it went
something like this: In the middle of working on branch **A** you decided you
should test something out on branch **B**.  So you quickly run `git stash`,
checkout branch **B** and test something, then come back to branch **A**, run `git
stash apply` and pick back up where you left off.

Well it turns out `git stash` is much more powerful than that, and we've all
been missing out *for years*. I always knew somewhere in the back of my head that
`git stash` operated some kind of stack, but I just kept happily pushing things
onto the stack without worrying about what that really meant.

One day I decided to take a look at [`git help
stash`](https://git-scm.com/docs/git-stash) and I suddenly realized I could
be getting a lot more use out of this little command.  First I learned about
the `list` subcommand, which shows the entire contents of that stack. The first
time I tried it out it was a mess:

``` sh
# git stash list
stash@{0}: WIP on master: ad4304a fixed bug
stash@{1}: WIP on master: bffb5b9 added feature
stash@{2}: WIP on master: 4a70758 it works!
stash@{3}: WIP on master: 4a70758 it works!
stash@{4}: WIP on feature-a: d5d384a wow this is great
stash@{5}: WIP on master: d2abda9 finally fixed it
...
```

What happened here? It turns out every time I had run `git stash` before
I knew what I was doing I was pushing a new stash onto the stack. Then when
I got my changes back by running `git stash apply`, git just peeked at the most
recent stash , applied its changes, and left it sitting on the stack. There's
another command, `pop`, which applies the stash *and* pops it off the stack.

So every single stash I've ever created is just hanging out here on the stack,
and that is reflected in the `git stash list` output.

So there's a stack? So what?
============================
So all I've really learned at this point is that I should use `pop` instead
of `apply` to make sure I clean up after myself, but does this stack let me
do anything else?

For a lot of projects I have a few small changes I find myself making and
undoing all the time. For example changing the configuration to point to a
development server, or adding some sort of debug output. I realized that I can
use the stash stack to store these various patches and apply them at will.

My new stash Workflow
---------------------
If you run `git stash save` explicitly instead of the shortcut, `git stash`,
you can specify a message for the stash, something more descriptive than "WIP
on ...", like `git stash save add debug info`. So now, after adding a few
useful stashes, my stack looks like this:

``` sh
# git stash list
stash@{0}: On master: add debug info
stash@{1}: On master: use local server
```

Much better! Now how do I use these patches? Since I want to apply the patch
while still keeping it around on the stack, I can go back to my old friend
`apply`. It turns out you can also specify which stash you want to apply,
so I can switch to the local server by running `git stash apply stash@{1}`.

Now what if I've made some other changes, and I'd like to "unapply" that stash?
There's no built-in way to do it, but [this SO
answer](http://stackoverflow.com/a/1021867) points out a way to hack it
together, by printing out the patch and applying it in reverse:

``` sh
git stash show -p stash@{1} | git apply --reverse
```

These commands are useful, but a little bit wordy. I added some aliases to
`~/.gitconfig` to make it easier:

```
stapply = "!f() { git stash apply stash@{$1}; }; f"
stunapply = "!f() { git stash show -p stash@{$1} | git apply --reverse; git status; }; f"
```

Now all I have to type is `git stapply 1` and `git stunapply 1` to toggle the
local server on and off.
