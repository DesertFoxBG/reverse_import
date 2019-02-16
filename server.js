var express = require('express');
var app = express();

var urls = [
    'https://www.w3schools.com/jsref/met_document_queryselector.asp',
    'https://stackoverflow.com/questions/7184562/how-to-get-elements-with-multiple-classes'
]

var count = 0;

app.get('/', function (req, res) {
    console.log('\nScraping...');
    var rand = Math.floor(Math.random() * 2);
    var exec = require('child_process');
    var toFile = require('child_process');
    var jsdom = require('child_process');
    
    toFile.exec('phantomjs phantom.js ' + urls[0], {maxBuffer: 1024 * 500}, function(error, stdout, stderr) {
        if(error instanceof Error) {
            throw error
        }
        
        count++;
        console.log('\ncount: ' + count);

        process.stderr.write(stderr);
        process.stdout.write(stdout);

        jsdom.exec('node jsdom.js', {maxBuffer: 1024 * 1024}, function(error, stdout, stderr) {
            if (error instanceof Error) {
                throw error;
            }
    
            //count++;
            console.log('\ncount: ' + count);
    
            process.stderr.write(stderr);
            process.stdout.write(stdout);

            exec.exec('python geturl.py divs.txt classes.txt styles.json', {maxBuffer: 1024 * 1024}, function(error, stdout, stderr) {
                if (error instanceof Error) {
                    throw error;
                }
        
                //count++;
                console.log('\ncount: ' + count);
        
                process.stderr.write(stderr);
                process.stdout.write(stdout);
            });
        });
    });
})

app.listen(9999, function () {
   console.log("App listening on port 9999")
})