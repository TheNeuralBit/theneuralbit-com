var last_known_scroll_position = 0;
var ticking = false;

var OFFSET_TOP = 50.0;
var MAX_FONTSIZE = 46;
var MIN_FONTSIZE = 23;

var MAX_PADDING = 27;
var MIN_PADDING = 11;

color_scale = d3.scale.linear()
                .domain([0, OFFSET_TOP])
                .range(['#fff', '#f8f8f8']);
var brand = d3.select('.navbar-brand')
var nav = d3.select('nav');

function adjust_header(scroll_pos) {
  if (scroll_pos === 0) {
    enable_anagranimate();
  } else {
    disable_anagranimate();
  }

  if (scroll_pos > OFFSET_TOP) {
    scroll_pos = OFFSET_TOP;
    fontsize = MIN_FONTSIZE;
    padding = MIN_PADDING;
    nav.classed('affix-top', false);
    nav.classed('affix', true);
  } else {
    var fontsize = (scroll_pos/OFFSET_TOP)*(MIN_FONTSIZE - MAX_FONTSIZE) + MAX_FONTSIZE;
    var padding = (scroll_pos/OFFSET_TOP)*(MIN_PADDING - MAX_PADDING) + MAX_PADDING + scroll_pos;
    nav.classed('affix-top', true);
    nav.classed('affix', false);
  }
  fontsize = fontsize.toString() + 'px';
  padding = padding.toString() + 'px';
  brand.style('font-size', fontsize)
                            .style('padding-top', padding);
  nav.style('background-color', color_scale(scroll_pos));
  console.log(scroll_pos);
  console.log(color_scale(scroll_pos));
}

window.addEventListener('scroll', function(e) {
  last_known_scroll_position = window.scrollY;
  if (!ticking) {
    window.requestAnimationFrame(function() {
      adjust_header(last_known_scroll_position);
      ticking = false;
    });
  }
  ticking = true;
});
