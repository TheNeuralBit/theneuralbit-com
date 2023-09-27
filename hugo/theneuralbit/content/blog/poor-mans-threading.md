+++
title = "Poor Man's Threading (in Javascript)"
slug = "poor-mans-threading"
categories = ["blog"]
type = "post"
date = 2016-10-23
draft = "True"
+++
Javascript is single-threaded.

I hear that all the time, but I think people's interpretation of it is often
an oversimplification. That statement is true within a single browser tab, but
there are plenty of ways to get that browser to thread for you:

* **Asynchronous I/O (AJAX or FileReader).** The browser handles all the details of
  this for you, but at the end of the day it's doing some kind of
  multi-threading to handle the request, so your browser tab can do other
  work in the meantime.
* **Create new contexts: WebWorker, ServiceWorker, etc...** Each worker is
  operating in its own separate context, which is in its own thread.
* And in this post I'd like to talk about a third technique I like to call
  **Poor Man's Threading**.

