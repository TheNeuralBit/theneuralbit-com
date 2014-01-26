---
layout: project
title: Timelapse Photography
image: WB_peak.jpg
description: "Timelapse photography using a cheap digital camera - my first attempt at being artsy"
keywords: "timelapse, photography, nature, sky, night, cereus"
tags: [timelapse, photography, nature, sky, night, cereus]
---
I recently acquired a Canon PowerShot A530 camera, and decided to use it to take
a few timelapse videos. I installed the
[Canon Hardware Development Kit (CHDK)](http://chdk.wikia.com/wiki/CHDK) on it,
which gives me a lot more control over the camera's settings. In addition you
can use it to write scripts to automatically control the camera.  I use 
[this script](http://chdk.wikia.com/wiki/UBASIC/Scripts:_Ultra_Intervalometer) to
capture the pictures.

Once I have a series of pictures, I need to encode them into an actual video. I
use an application called mencoder. It is a command-line tool that lets you
create all sorts of videos, including videos generated from a series of images.
Under Linux (sorry, Im not sure how to do it in Windows), you can probably
install it with your distribution's package manager (``apt-get``, ``yum``,
``pacman``...).  Once it's installed simply run this command inside the folder
containing your images:

    # mencoder "mf://*.jpg" -mf fps=<framerate>; -o timelapse.avi -ovc lavc -lavcopts vcodec=mpeg4

Where ``<framerate>`` is your desired framerate.  30 frames per second is
typical, but I've found that I can get away with framerates as low as 15 frames
per second.  Also, you may need to change the ``*.jpg`` to match  your image
files.

When the command is complete the video will be in a file called ``timelapse.avi``
in that folder.

Below you can find some of the videos I've made using this technique (Click the
"vimeo" link in the bottom right corner of each video to see it in higher
resolution)

* I want a table of contents here!
{:toc}

Roadtrip
--------
The first video I took shows the end of my trip to visit my brother in
Jonesville, SC.  I set up the camera taking photos every 5 seconds in his living
room.  When I realized it would still be going when I wanted to leave I set it
up in my car, to record the trip home to Hillsborough, NC.

The video runs at 15 frames per second and each frame corresponds to 5 seconds
in real time, this means the entire video is almost 4 hours of real time.

{% vimeo 12382351 width="600" height="450" %}

Night Sky
---------
Later, I decided to try to capture the motion of the stars in the night sky outside my house.
I configured the camera to take 10 second exposures with ISO800 to make sure the stars would be bright enough.

Each shot is 25 seconds apart, and the video runs at 15 frames per second, so it corresponds to just over 2 hours of real time.

{% vimeo 13143403 width="600" height="450" %}

Night Sky Attempt 2
-------------------
I repeated my night sky timelapse video with some altered settings.
I increased the exposure length to 15 seconds to make the stars more easily visible.
Of course, this meant that each shot took longer, so the time between shots was increased to 35 seconds.

There are about 400 shots spaced 35 seconds apart, so this corresponds to jut over 4 hours of real time.

{% vimeo 13279592 width="600" height="450" %}

Nightblooming Cereus
--------------------
I also made a timelapse video of my mom's Nightblooming Cereus (sometimes called the "Queen of the Night").
It gets its name because it only blooms once a year, and each flower only blooms for one night.

There are about 1400 pictures spaced 5 seconds apart making up this video, so it corresponds to almost 2 hours of real time.

This video is higher quality, so I really recommend clicking the "vimeo" button to watch it there, where you can watch it in HD.

{% vimeo 13317489 width="600" height="450" %}

Nightblooming Cereus Attempt 2
------------------------------
My second attempt at recording the Nightblooming Cereus.
This one last a lot longer, and I managed to capture three flowers at once.

This video is also higher quality, so again, I recommend clicking the "vimeo" button to watch it there, where you can watch it in HD

{% vimeo 13388576 width="600" height="450" %}

Clouds
------
I made a timelapse video of the clouds in the sky one morning outside of my house.
The video is made up of 3,216 pictures taken 5 seconds apart, which means it lasts for about four and a half hours.

{% vimeo 13595390 width="600" height="450" %}

High-Altitude Imaging
---------------------
I made a timelapse video of my  weather balloon flight.  Read more about it <A HREF="balloon.html">here</A>

{% vimeo 27751339 width="600" height="450" %}
