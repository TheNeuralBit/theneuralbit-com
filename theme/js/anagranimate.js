"use strict";
var trigger_buf = 50;
var header = d3.select('.navbar-brand');
var header_rect = header[0][0].getBoundingClientRect();
var w = header_rect.right - header_rect.left;
var h = header_rect.bottom - header_rect.top;

var padding_left = parseInt(header.style('padding-left').slice(0, -2), 10);
var padding_top = parseInt(header.style('padding-top').slice(0, -2), 10);

var svg = d3.select('#logo')
    .style('position', 'absolute')
    .style('width', '' + w + 'px')
    .style('height', '' + h + 'px')
    .style('left', '' + -padding_left + 'px');
['font-size', 'font-family'].map(function (key) {
    svg.style(key, header.style(key));
});

svg.style('display', 'block');
header.style('visibility', 'hidden');


var tester = svg.append('text');
var space_width = tester.text('a a').node().getBBox().width -
    tester.text('aa').node().getBBox().width;
tester.remove();

// Turn strings into lists of objects with some additional information
function strParse(str) {
    var x = d3.scale.ordinal()
        .domain(d3.range(str.length))
        .rangePoints([20, w - 20], 1),
        rtrn = [],
        char_count = {},
        curr_x = padding_left,
        bbox, this_object, is_space, i;
    tester = svg.append('text');

    for (i = 0; i < str.length; i += 1) {
        if (char_count[str[i]] !== undefined) {
            char_count[str[i]] += 1;
        } else {
            char_count[str[i]] = 0;
        }
        is_space = str[i] === " ";
        bbox = tester.text(is_space ? "l" : str[i]).node().getBBox();
        if (is_space) {
            bbox.width = space_width;
        }

        curr_x += bbox.width / 2;
        // These are the objects were adding to the list
        // c:       the char
        // count:   # of previous occurrences of this letter (used for the d3 key)
        // x, y:    initial positions for force layour
        // cx, cy:  assigned positions for gravity force - letters will be attracted
        //          here
        // radius:  used for collision detection
        // w, h:    width and height of the letter
        this_object = {
            c: str[i],
            count: char_count[str[i]],
            x: curr_x,
            y: padding_top + bbox.height / 2,
            cx: curr_x,
            cy: padding_top + bbox.height / 2,
            radius: is_space ? 0 : bbox.width / 2,
            w: bbox.width,
            h: bbox.height
        };
        curr_x += bbox.width / 2;
        rtrn.push(this_object);
    }
    tester.remove();
    return {
        'string': str,
        'data': rtrn
    };
}

var str1 = strParse('the neural bit');
var str2 = strParse('brian hulette');
var mouse_node = {};

var curr_str = str1;


// Use this key for d3 selections, so that when we change out strings we
// associate corresponding characters in the anagrams correctly
function key(d) {
    return d.c + d.count;
}

// Create the initial text objects
var text = svg.selectAll('text')
    .data(str1.data)
    .enter()
    .append('text')
    .attr('text-anchor', 'middle')
    .attr('alignment-baseline', 'middle')
    .attr('x', function (d, ignore) {
        return d.x;
    })
    .attr('y', function (d, ignore) {
        return d.y;
    })
    .attr('fill', header.style('color'))
    .text(function (d) {
        return d.c;
    });

var min_x = d3.min(text.data(), function (d) {
    return d.x - d.w / 2;
}) - trigger_buf;
var max_x = d3.max(text.data(), function (d) {
    return d.x + d.w / 2;
}) + trigger_buf;
var min_y = d3.max(text.data(), function (d) {
    return d.y - d.h / 2;
}) - trigger_buf;
var max_y = d3.max(text.data(), function (d) {
    return d.y + d.h / 2;
}) + trigger_buf;

var trigger_rect = svg.append('rect')
    .attr('x', Math.max(0, min_x))
    .attr('width', max_x - min_x)
    .attr('y', Math.max(0, min_y))
    .attr('height', max_y - min_y)
    .attr('fill-opacity', '0');

function updateBBox() {
    var tester = svg.append('text'),
        curr_x = 0,
        bbox,
        is_space,
        i;
    for (i = 0; i < curr_str.length; i += 1) {
        is_space = curr_str[i].c === " ";
        bbox = tester.text(is_space ? "l" : curr_str[i].c).node().getBBox();
        curr_x += bbox.width / 2;

        curr_str[i].cx = curr_x;
        curr_str[i].radius = bbox.width / 2 - 2;

        curr_x += bbox.width / 2;
    }
    tester.remove();
}

function gravity(alpha) {
    return function (d) {
        d.y += (d.cy - d.y) * alpha;
        d.x += (d.cx - d.x) * alpha;
    };
}

function collide(node) {
    var r = node.radius + 16,
        nx1 = node.x - r,
        nx2 = node.x + r,
        ny1 = node.y - r,
        ny2 = node.y + r;
    return function (quad, x1, y1, x2, y2) {
        if (quad.point && (quad.point !== node)) {
            var x = node.x - quad.point.x,
                y = node.y - quad.point.y,
                l = Math.sqrt(x * x + y * y);
            r = node.radius + quad.point.radius;
            if (l < r) {
                l = (l - r) / l * 0.5;
                x *= l;
                y *= l;
                node.x -= x;
                node.y -= y;
                quad.point.x += x;
                quad.point.y += y;
            }
        }
        return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
    };
}

// Create force layout
var force = d3.layout.force()
    .nodes([mouse_node].concat(str1.data))
    .links([])
    .gravity(0)
    .size([w, h])
    .charge(0);

var epsilon = 1;

force.on("tick", function (e) {
    var cw, ch, q, i;

    // Attract each node towards its assigned position
    text.each(gravity(0.15 * e.alpha));

    // Do collision detection between every node
    q = d3.geom.quadtree(curr_str);
    i = 0;
    while (i < curr_str.length) {
        q.visit(collide(curr_str[i]));
        i += 1;
    }

    // Move each character to its assigned position
    cw = svg.node().getBoundingClientRect().width;
    ch = svg.node().getBoundingClientRect().height;
    text
        .attr('x', function (d) {
            var x = Math.max(d.w / 2, Math.min(cw - d.w / 2, d.x));
            if (Math.abs(d.px - d.x) < epsilon && Math.abs(d.cx - d.x) < epsilon) {
                x = d.cx;
            }
            return x;
        })
        .attr('y', function (d) {
            var y = Math.max(d.h / 2, Math.min(ch - d.h / 2, d.y));
            if (Math.abs(d.py - y) < epsilon && Math.abs(d.cy - y) < epsilon) {
                y = d.cy;
            }
            return y;
        });
    //circles
    //  .attr('cx', function (d) {
    //    var x = Math.max(0, Math.min(cw - d.w, d.x));
    //    return x;
    //  })
    //  .attr('cy', function (d) {
    //    var y = Math.max(d.h, Math.min(ch, d.y));
    //    return y;
    //  });
});

// Handle mouse/touch events
// enter: switch between strings using toggle() and turn on charge for node that
//        follows mouse
// leave: turn off charge for mouse node
// move:  move mouse node to actual mouse position
var active = true;

function toggle(str) {
    force.nodes([mouse_node].concat(str));

    var old_str = text.data();
    old_str.forEach(function (item) {
        str.forEach(function (other) {
            if (key(item) === key(other)) {
                other.x = item.x;
                other.y = item.y;
                other.px = item.px;
                other.py = item.py;
            }
        });
    });
    text.data(str, key);
    curr_str = str;
    force.start();
}

function do_toggle() {
    if (active) {
        toggle(str2.data);
        header.text(str2.string);
        document.title = str2.string;
    } else {
        toggle(str1.data);
        header.text(str1.string);
        document.title = str1.string;
    }
    active = !active;
}

function startmouse() {
    force.charge(function (ignore, i) {
        return i === 0 ? -1000 : 1;
    });
    force.start();
}

function endmouse() {
    force.charge(0);
    force.start();
}

function movemouse() {
    var p1 = d3.mouse(this);
    mouse_node.x = p1[0];
    mouse_node.y = p1[1];
    force.resume();
}

trigger_rect.on('mouseenter', do_toggle);
svg.on('mouseenter', startmouse);
svg.on('touchstart', startmouse);
svg.on('mouseleave', endmouse);
svg.on('touchend', endmouse);
svg.on('touchcancel', endmouse);
svg.on('mousemove', movemouse);
svg.on('touchmove', movemouse);

// Start up the force layout once everything is defined
force.start();

function enable_anagranimate() {
    svg.style('display', 'block');
    header.style('visibility', 'hidden');
    force.start();
}

function disable_anagranimate() {
    svg.style('display', 'none');
    header.style('visibility', 'visible');
    force.stop();
}
