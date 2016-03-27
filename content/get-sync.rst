Syncing ``GET`` Arguments and AngularJS Models
##############################################

:date: 2016-01-24 11:56
:tags: web, javascript, angular, $location
:slug: get-sync
:category: misc
:authors: Brian Hulette
:layout: post

As I was working on my `D3 daylight visualization <http://theneuralbit.github.io/daylight>`_ 
I ran into a problem. After showing the first iteration to my friends, they set
out to find every single edge case that broke the tool. Obvously, I
wanted to fix every case, but the bug report process was *so* laborious:

#. Friend copies latitude/longitude
#. Friend sends me that latitude/longitude
#. I open the tool
#. I enter the latitude/longitude and inspect the problem
#. I fix the problem

Ok so maybe this isn't such a big deal, but it bugged me nonetheless. My idea
for streamining this process was to sync the models for the lat/long with the
URL, so whenever a friend runs into an issue:

#. Friend copies the URL, which includes the latitude/longitude: ``http://awesome.site/#lat=xx.xx&lng=yy.yy``
#. Friend sends me the URL
#. I navigate to that URL and inspect the problem
#. I fix the problem

This cuts out one entire step! and we only have to copy/paste one thing (URL) rather
than latitude *and* longitude. Incredible.

So here's how I accomplished it. I was already using angularJS for this tool,
which it turns out includes everything I need within the ``$location`` service
(`docs <https://docs.angularjs.org/api/ng/service/$location>`_) . First, I include the ``$location`` service as a dependency:

.. code-block:: javascript

    app.controller('DaylightController', function($scope, $location, ...) {
        ...
    });


Then, I add watchers to the latitude and longitude models to modify the URL
whenever those models change:

.. code-block:: javascript

    $scope.$watch(function() {
      return ctrl.lat;
    }, function() {
      $location.search('lat', ctrl.lat).replace();
    }, true);

    $scope.$watch(function() {
      return ctrl.lng;
    }, function() {
      $location.search('lng', ctrl.lng).replace();
    }, true);

Now whenever ``lat`` or ``lng`` change, ``$location.search()`` is called in its
setter configuration, and ``.replace()`` is added to make sure we overwrite the
old argument.

Ok so now my friends can easily copy a URL that includes a latitude and
longitude, but now I need the tool to recognize these arguments when I navigate
to a URL which includes them.  This just requires a few extra lines of
initialization:

.. code-block:: javascript

    var keys = $location.search();

    ctrl.lat = parseFloat(keys.lat) || default_lat;
    ctrl.lng = parseFloat(keys.lng) || default_lng;

And there you go! If you need some proof, check out the goofy daylight hours in `Alaska <http://theneuralbit.github.io/daylight/#?lat=65.366&lng=-150.468>`_ - why do they even bother with daylight savings time?

You can see this code in place in the project's `github repo <https://github.com/TheNeuralBit/daylight/blob/gh-pages/daylight.js>`_.
