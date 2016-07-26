title: Fun with git stash
slug: fun-with-git-stash
layout: post
category: blog
tags: git, cli
date: 2016-07-26

git stash list
stapply = "!f() { git stash apply stash@{$1}; }; f"
stunapply = "!f() { git stash show -p stash@{$1} | git apply --reverse; git status; }; f"
