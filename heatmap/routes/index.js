var express = require('express');
var router = express.Router();
var indexController = require("../controllers/indexController");

/* GET home page. */
router.get('/:date/:time?',indexController.renderView);

module.exports = router;
