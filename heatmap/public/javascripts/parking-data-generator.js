// var mysql = require('mysql');
// var express = require('express');
// var request = require('request');
// var rp = require('request-promise');
// var app = express();

// let con = mysql.createConnection({
//     host: "localhost",
//     user: "parking_user",
//     password: "parking",
//     database: "parking"
// });

// let config = {
//     host: "http://avr-service",
//     port: 4569,
//     path: "/avr"
// };

// con.connect(function(err) {
//     if (err) {
//         throw err;
//     }
//     console.log('MySQL connected');
// });

// function logError(error) {
//     console.log('Looks like there was a problem: \n', error);
// }

// function validateResponse(response) {
//     if (!response.ok) {
//         throw Error(response.statusText);
//     }
//     return response;
// }

// function readResponseAsJSON(response) {
//     return response.json();
// }

// function processResult(result) {

// }

// function fetchData(lat, lon, currentDate) {
//     const params = { lat: lat, lon: lon, time: roundTime(currentDate.toTimeString(), 15), dow: currentDate.getDay() };


//     let query = Object.keys(params)
//         .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
//         .join('&');
//     const url = config.host + ':' + config.port + config.path + '?' + query;
//     fetch(url, {
//             method: 'GET',
//             headers: {
//                 'Accept': 'application/json',
//                 'Content-Type': 'application/json'
//             },
//             mode: 'cors'
//         })
//         .then(validateResponse)
//         .then(readResponseAsJSON)
//         .then(processResult)
//         .catch(logError);
// }

// function generateData(date, time) {
//     let promise = new Promise(function(resolve, reject) {
//         var sql = 'SELECT AVR.lat, AVR.lon, AVR.avr AS count ' +
//             ' FROM parking_avr AVR ' +
//             'WHERE  AVR.time = concat_ws(\' \', ' + mysql.escape(date) + ' , SEC_TO_TIME(FLOOR((TIME_TO_SEC(TIME_FORMAT(' + mysql.escape(time) + ', \'%H:%i:%s\'))+450)/900)*900));';
//         con.query(sql, function(err, result) {
//             if (err) reject(err);
//             console.log(result.length);
//             resolve(result);
//         });
//     });
//     return promise;
// }
// module.exports = { generateData };