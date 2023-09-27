+++
title = "Anagranimation"
slug = "anagranimation"
categories = ["projects"]
type = "post"
date = 2016-01-18
draft = "False"
+++
The name of this website is an anagram. It's possible to rearrange all of the
letters in **the neural bit** to form **brian hulette**.
That's a simple concept I set out to illustrate concisely with the
site's logo.

For the first iteration of this webpage, way back when I was in late high
school and early college (ca. 2007), I just pulled up the Gimp, which I had
probably learned to use just the previous week, and drew up the following
image. It shows the two words in bright letters and a few intermediate
iterations with letters swapped in between them.

![Original logo](./images/original_header.jpg)

This gets the job done, but it leaves a lot to be desired.

After I moved to my [new static site](./this-website.html) I didn't bring the
original logo, so I was stuck without a concise illustration for a while...
until I learned about [D3](http://d3js.org). After reading some of [Mike
Bostock's](http://bost.ocks.org/mike/) excellent blog posts about
[selections](http://bost.ocks.org/mike/circles/),
[object constancy](http://bost.ocks.org/mike/constancy/), and
[transitions](http://bost.ocks.org/mike/transition/)[ref]If you aren't familiar with
D3 and you'd like to be I would *highly* recommend you start with some of these
posts[/ref], I realized that an anagram is a perfect use case for D3's data binding
model.

My basic idea was to take the letters in a string and bind them to `svg:text`
elements, which are then positioned based on their index in the string. Later
a _new_ string, which is an anagram of the first, is bound to the elements. The
positions of the elements are updated, with the transition in between animated.
Then we can toggle back and forth between the two strings to our heart's content.

Confused? So was I. Let's start from the beginning.

Binding characters to `svg:text` Elements
-----------------------------------------
We'll start by just drawing a string using a bunch of separate
`svg:text` elements. We create a selecton of `svg:text` elements, then
bind the string data to the selction. Then we grab the `enter()` selection
to get just the elements that are new, which is all of them in this case.
We then set the elements' text to that datum, and set their `x` positions based
on the character's position in the string.

<iframe width="100%" height="400" src="//jsfiddle.net/theneuralbit/hazkxg07/6/embedded/result,js/" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

Binding a new String
--------------------
Once the original string has been bound we can bind a new string that has all of
the same characters. Then we just recompute the `x` attribute based on the _new_
indices in the string.

Unfortunately there's one catch: by default D3 will just check the new
characters for equality with the old characters to bind the new data. Normally
this is a reasonable behavior, but in this case it will cause problems since we
have duplicates of the same character. To solve this problem I wrote a function,
`transform()` that turns a string into a list of objects. Each object has one
attribute indicating the actual character, and another attribute that is an index
to ensures it is unique.

For example, `transform('the neural bit')` would return:
```
[{c: 't', i: 0},
 {c: 'h', i: 0},
 {c: 'e', i: 0},
 {c: ' ', i: 0},
 {c: 'n', i: 0},
 {c: 'e', i: 1},
 ...
 {c: 'i', i: 0},
 {c: 't', i: 1}]
```

Note that the second _e_ and the second _t_ both have an index of 1, to
distinguish them from the first occurrences.

With these new objects D3's default behavior will be sufficient to ensure
a reasonable mapping from the old string to the new string. The first _t_ will
be associated with the other first _t_ and the second _e_ will be associated
with the other second _e_, and so on.

The following example uses the new transformed strings to toggle between _the
neural bit_ and _brian hulette_ using a timer. Note that I only have to set the
text of each element once, in the initial `svg.selectAll()`. Within the
`setInterval()` function, all I do is bind the toggled string and update the `x`
attribute based on the character's position in the new string.

<iframe width="100%" height="600" src="//jsfiddle.net/theneuralbit/hazkxg07/7/embedded/result,js/" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

Well that result is... underwhelming. You really can't tell that those are
actually the _same_ `svg:text` elements each time it toggles. It just looks
like we're swapping out a new string. We need to animate the transition between
each state...

Adding Transitions
------------------
Fortunately D3 makes this easy - all we have to do is add a `.transition()`
call to the method chain before binding an attribute to some new function, and
D3 handles the rest!  It will set keyframes and set up easing functions all by
itself. You can read a lot more about the transition capability in the
[docs](https://github.com/mbostock/d3/wiki/Transitions), I'm only scratching
the surface here.

In the following example, I also added a call to `.duration()`, which makes
sure the animation takes one second, and a call to `attrTween()` which defines
intermediate values for the `y` attribute. This makes the characters follow
a parabolic trajectory.

In the example below you can see these changes reflected after the
`svg.selectAll()` call within `setInterval()`.

<iframe width="100%" height="600" src="//jsfiddle.net/theneuralbit/hazkxg07/8/embedded/result,js/" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

This is a pretty great little animation, and I thought about stopping here. It
does get the point across, but I still wasn't totally happy with it.
The letters are clearly "on rails", and they cut through each other's paths.
Fortunately, I found way to make the animation much more dynamic.


D3 Force Layout
---------------
Yet again, I followed Mike Bostock's lead here. I knew I wanted to use a force
layout to create something like his
[Multi-Foci Force Layout](http://bl.ocks.org/mbostock/1021953). My idea was
that each character would have a focus associated with it, which is set based
on the letter's position in the string.  I then used the same approach as
Bostock's Multi-Foci Layout to attract each character to its focus. When
toggling strings we simply change these focus positions and the letters will
shuffle around.  To make things more interesting I also added a few more
features:

* Mousing over the logo triggers the transition
* Collision forces between the letters
* A strong repulsion between the characters and the cursor
* Instead of assuming a fixed size for each character, like I did in the
  previous examples, I measure the size of each character to space out their
  respective foci appropriately

You can see this Force Layout implementation, in all its gory detail, in the
jsfiddle below or on [github](https://github.com/TheNeuralBit/anagranimate). If
you'd rather just see it in action, scroll up and mouse over my logo!

<iframe width="100%" height="600" src="//jsfiddle.net/hazkxg07/10/embedded/result,js" allowfullscreen="allowfullscreen" frameborder="0"></iframe>
