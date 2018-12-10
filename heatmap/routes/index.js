var express = require('express');
var router = express.Router();
var indexController = require("../controllers/indexController");

/* GET home page. */
router.get('/:date/:hour?',indexController.renderView);

module.exports = router;
