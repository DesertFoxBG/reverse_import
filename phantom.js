var webPage = require('webpage');
var page = webPage.create();
var fs = require('fs');
var system = require('system');
var url = system.args[1];
urlString = url.toString();
console.log('url: ' + urlString);

page.open(urlString, function (status) {
  var path = 'output.html';
  var content = page.content;
  console.log('Processing...');

  console.log(content);

  fs.write(path, content, 'w');

  phantom.exit();
});