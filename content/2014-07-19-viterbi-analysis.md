title: Analyzing the Viterbi Algorithm
slug: viterbi-analysis
layout: post
tags: CS5114, VT, MATLAB, DSP


This summer I am taking CS5114 - Theory of Algorithms at Virginia Tech.
Our first Project was to analyze a Dynamic Programming algorithm, and compare
it to other approaches that solve the same problem. Since I am focusing on
DSP/Communications, I decided to look at the
[Viterbi algorithm](http://en.wikipedia.org/wiki/Viterbi_algorithm), a Dynamic
Programming approach to decoding Convolutional Codes.

<!-- more -->

For the project I investigated why the Viterbi algorithm is so much more
efficient than alternative approaches to decoding convolutional codes (Such as
a brute force or recursive technique).  The answer quickly becomes clear -
as with most problems that can be solved with Dynamic Programming, standard
approaches often re-compute the same values several
times rather than just storing the values. In this case, the values that are
being constanstly recomputed are the pth metrics for each transition in the
Trellis diagram.

Of course the advantage of the Viterbi algorithm is that it finds a way to just
compute each path metric once.  This allows it to run in linear time, rather
than exponential time like a recursive approach.

You can view my presentation below, or for a more complete treatment you
can read the [paper]({filename}/media/paper.pdf).

{% speakerdeck 82b209c0f181013106da6eb14261a8ef %}
<br/>

I've also posted all of the MATLAB code for my project on GitHub.  The repository
includes implementations of a Brute Force algorithm, a Recursive algorithm,
and finally the Viterbi algorithm. There are also scripts to prove that they all
work and to test the runtime.

{% githubrepo theneuralbit/viterbi %}
