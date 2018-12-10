global.fetch = require('isomorphic-fetch');
var express = require('express');
var router = express.Router();
var generator = require('../public/javascripts/parking-data-generator');

let config = {
    host: "http://172.19.0.2",
    port: 4570,
    path: "/get_avr"
};

var ret = {
    min: 0,
    max: 100,
    data: []
};

function processResult(result) {
    // console.log('-------------------------------------------------------------------');
    // console.log('data: ' + ret);
    // console.log('-------------------------------------------------------------------');
    // console.log('Setting data');
    // console.log(result);
    ret.data.push(result);
}

function logError(error) {
    console.log('Looks like there was a problem: \n', error);
}

function validateResponse(response) {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}

function readResponseAsJSON(response) {
    return response.json();
}

function fetchData(params) {
    let query = Object.keys(params)
        .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
        .join('&');
    const url = config.host + ':' + config.port + config.path + '?' + query;
    console.log(url);
    return fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: 'cors'
        })
        .then(validateResponse)
        .then(readResponseAsJSON)
        .catch(logError);
}

function renderView(req, res, next) {
    let date = req.params.date;
    let hour = req.params.hour;
    const params = { date: req.params.date, hour: req.params.hour };
    console.log(params);
    fetchData(params)
    .then((result) => {
        res.render('map', { title: 'HeatMap', jsonData: { min: 0, max: 100, data: result }});
    });
    //console.log(generator.generateData());
}

module.exports = { renderView };