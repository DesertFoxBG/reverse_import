var express = require('express');
var app = express();

var urls = [
    'http://www.jivotno.com/',
    'http://blog.bg/'
]

var count = 0;

app.get('/', function (req, res) {
    console.log('\nScraping...');
    var rand = Math.floor(Math.random() * 2);
    var exec = require('child_process');
    var toFile = require('child_process');
    
    toFile.exec('phantomjs phantom.js ' + urls[1], {maxBuffer: 1024 * 500}, function(error, stdout, stderr) {
        if(error instanceof Error) {
            throw error
        }
        
        count++;
        console.log('\ncount: ' + count);

        process.stderr.write(stderr);
        process.stdout.write(stdout);

        exec.exec('python geturl.py output.html', function(error, stdout, stderr) {
            if (error instanceof Error) {
                throw error;
            }
    
            //count++;
            console.log('\ncount: ' + count);
    
            process.stderr.write(stderr);
            process.stdout.write(stdout);
        });
    });
})

app.listen(9999, function () {
   console.log("App listening on port 9999")
})