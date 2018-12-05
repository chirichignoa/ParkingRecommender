var express = require('express');
var router = express.Router();
var generator = require('../public/javascripts/parking-data-generator');

let config = {
    host: "http://avr-service",
    port: 4569,
    path: "/avr"
};

let data = {
    min: 0,
    max: 100,
    data: []
};

function processResult(result) {
    data.data = result;
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
    fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: 'cors'
        })
        .then(validateResponse)
        .then(readResponseAsJSON)
        .then(processResult())
        .catch(logError);
}

function renderView(req, res, next) {
    let date = req.params.date;
    let time = req.params.time;
    const params = { date: req.params.date, time: req.params.time };
    console.log(params);
    fetchData(params, data);
    res.render('map', { title: 'HeatMap', jsonData: data });
    //console.log(generator.generateData());
}

module.exports = { renderView };