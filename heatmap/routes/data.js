var express = require('express');
var router = express.Router();
var fecha = require('fecha');
var generator = require('../public/javascripts/parking-data-generator');

router.get('/:date/:hour?', function(req, res, next) {
    let date = req.params.date;
    let time = req.params.hour;
    console.log(date);
    console.log(time);
    generator.generateData(date, time).then((fulfilled) => {
        if(fulfilled) {
            res.status(200).send(fulfilled);
        }
    }).catch((err)=>{
        return res.status(200).send(err);
    });
});

module.exports = router;