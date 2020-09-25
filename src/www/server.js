// Load Node JS Modules
var http = require('http');
var path = require('path');
var request = require('request');
var express = require('express');
var app = express();

// Set port to 3000
app.set('port', 3000);

http.createServer(app).listen(app.get('port'), function() {});
