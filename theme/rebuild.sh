#! /bin/bash
lessc less/style.less static/style.css
uglifyjs js/anagranimate.js > static/js/anagranimate.min.js
uglifyjs js/scrollspy.js > static/js/scrollspy.min.js
