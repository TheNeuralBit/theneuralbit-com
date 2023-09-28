all: css js

static/style.css: less/style.less
	lessc less/style.less static/style.css

static/js/%.min.js: js/%.js
	uglifyjs $< > $@

css: static/style.css

js: static/js/anagranimate.min.js static/js/scrollspy.min.js
