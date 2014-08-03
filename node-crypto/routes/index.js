var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res) {
  res.render('index', { title: 'Express' });
});

router.get('/buy', function(req, res) {
  res.render('buy', { title: 'Express' });
});

router.get('/goback', function(req, res) {
  res.render('great');
});

router.get('/received', function(req, res) {
  res.render('thanks');
});

router.get('/failure', function(req, res) {
  res.render('failure');
});

module.exports = router;
