const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'utf8');
const js = fs.readFileSync('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'utf8');

// replace import with empty so it doesn't crash node JSDOM if module not supported, actually jsdom has limited support.
// let's just find syntax errors using a regex check or something.
