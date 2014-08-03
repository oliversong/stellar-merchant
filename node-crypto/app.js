var express = require('express');
var path = require('path');
var favicon = require('static-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var atob = require('atob');
var sjcl = require('sjcl');
var scrypt = require('./sjcl-scrypt');

var routes = require('./routes/index');
var users = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);
app.use('/users', users);

app.post('/decrypt', function(req, res){

  var deriveKey = function(id, username, password){
    var credentials = id + username.toLowerCase() + password;
    var salt = sjcl.codec.utf8String.toBits(credentials);

    var key = scrypt(
      credentials,
      salt,
      2048,
      8,
      1,
      32
    );

    return sjcl.codec.hex.fromBits(key);
  };

  var decrypt = function(encryptedWallet, id, key){
    var rawKey = sjcl.codec.hex.toBits(key);

    var mainData = decryptData(encryptedWallet.mainData, rawKey);
    var keychainData = decryptData(encryptedWallet.keychainData, rawKey);

    var options = {
      id:           id,
      key:          key,
      mainData:     mainData,
      keychainData: keychainData
    };

    return options;
  };

  var decryptData = function(encryptedData, key) {
    // Parse the base64 encoded JSON object.
    var resultObject = JSON.parse(atob(encryptedData));

    // Extract the cipher text from the encrypted data.
    var rawCipherText = sjcl.codec.base64.toBits(resultObject.cipherText);

    // Extract the cipher text from the encrypted data.
    var rawIV = sjcl.codec.base64.toBits(resultObject.IV);

    // Extract the cipher name from the encrypted data.
    var cipherName = resultObject.cipherName;
    var mode = resultObject.mode;

    // Initialize the cipher algorithm with the key.
    var cipher = new sjcl.cipher[cipherName](key);

    // Decrypt the data in CCM mode using AES and the given IV.
    var rawData = sjcl.mode[mode].decrypt(cipher, rawCipherText, rawIV);
    var data = sjcl.codec.utf8String.fromBits(rawData);

    // Parse and return the decrypted data as a JSON object.
    return data;
  };

  var key = deriveKey(req.body.id, req.body.username, req.body.password);
  var wallet = decrypt(JSON.parse(req.body.content).data, req.body.id, key);
  // Parse and return the decrypted data as a JSON object.
  res.send(wallet);
});

/// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

/// error handlers

// development error handler
// will print stacktrace
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: err
    });
});

module.exports = app;
