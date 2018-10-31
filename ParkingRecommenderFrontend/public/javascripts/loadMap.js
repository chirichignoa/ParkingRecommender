// const rp = require('request-promise');
let startPos;
let lat, lon;
const url = "http://172.21.0.5:5000/predict";
const LOW_AVAILABILITY = 0.33,
    MEDIUM_AVAILABILITY = 0.66,
    HIGH_AVAILABILITY = 1;
let mymap = L.map('mapid').setView([-37.328836, -59.136921], 16);

const LeafIcon = L.Icon.extend({
    options: {
        shadowUrl: '../images/marker_shadow.png'
    }
});

const greenIcon = new LeafIcon({ iconUrl: '../images/marker_green.png' }),
    redIcon = new LeafIcon({ iconUrl: '../images/marker_red.png' }),
    yellowIcon = new LeafIcon({ iconUrl: '../images/marker_yellow.png' }),
    blueIcon = new LeafIcon({ iconUrl: '../images/marker_blue.png' });

let geoSuccess = function(position) {
    startPos = position;
    lat = startPos.coords.latitude;
    lon = startPos.coords.longitude;
    L.marker([lat, lon]).addTo(mymap);
};

let errorCallbackLowAccuracy = function errorCallback_lowAccuracy(error) {
    let msg = "Can't get your location (low accuracy attempt). Error = ";
    if (error.code === 1)
        msg += "PERMISSION_DENIED";
    else if (error.code === 2)
        msg += "POSITION_UNAVAILABLE";
    else if (error.code === 3)
        msg += "TIMEOUT";
    msg += ", msg = " + error.message;
    console.log(msg);
};

let errorCallback = function errorCallback_highAccuracy(error) {
    if (error.code === error.TIMEOUT) {
        navigator.geolocation.getCurrentPosition(geoSuccess,
            errorCallbackLowAccuracy, { maximumAge: 600000, timeout: 10000, enableHighAccuracy: false });
        return;
    }
    let msg = "Can't get your location (high accuracy attempt). Error = ";
    if (error.code === 1)
        msg += "PERMISSION_DENIED";
    else if (error.code === 2)
        msg += "POSITION_UNAVAILABLE";
    msg += ", msg = " + error.message;
    console.log(msg);
};

let roundTime = (time, minutesToRound) => {

    let [hours, minutes] = time.split(':');
    hours = parseInt(hours);
    minutes = parseInt(minutes);

    // Convert hours and minutes to time in minutes
    time = (hours * 60) + minutes;

    let rounded = Math.round(time / minutesToRound) * minutesToRound;
    let rHr = '' + Math.floor(rounded / 60);
    let rMin = '' + rounded % 60;

    return rHr.padStart(2, '0') + ':' + rMin.padStart(2, '0');
};


function processResult(result) {
    let marker;
    clearMarkers();
    for (let prediction of result) {
        marker = new L.marker(new L.LatLng(prediction.lat, prediction.lon), { icon: getIcon(prediction.prediction) })
            .bindPopup(prediction.dir + "\n " + (prediction.prediction * 100).toFixed(2).toString() + "%")
            .addTo(mymap);
        markers.push(marker);
    }
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

function fetchPrediction(lat, lon, currentDate) {
    let url = "http://172.21.0.5:5000/predict";
    fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: 'cors',
            body: JSON.stringify({
                lat: lat,
                lon: lon,
                time: roundTime(currentDate.toTimeString(), 15),
                dow: currentDate.getDay()
            })
        })
        .then(validateResponse)
        .then(readResponseAsJSON)
        .then(processResult)
        .catch(logError);
}

let doubleClickMarker;
let markers = [];

function clearMarkers() {
    if (markers.length > 0) {
        for (let i = 0; i < markers.length; i++) {
            mymap.removeLayer(markers[i]);
        }
    }
}

function getIcon(prediction) {
    if (prediction <= LOW_AVAILABILITY)
        return redIcon;
    else if (prediction <= MEDIUM_AVAILABILITY)
        return yellowIcon;
    return greenIcon;
}

let dblClickCallback = function onMapClick(e) {
    console.log(e.latlng.lat, e.latlng.lng);
    if (typeof(doubleClickMarker) === 'undefined') {
        doubleClickMarker = new L.marker(e.latlng, { icon: blueIcon, draggable: true });
        doubleClickMarker.addTo(mymap);
    } else {
        doubleClickMarker.setLatLng(e.latlng);
    }
    let currentDate = new Date();
    fetchPrediction(e.latlng.lat, e.latlng.lng, currentDate);
};

window.onload = function() {
    navigator.geolocation.getCurrentPosition(geoSuccess,
        errorCallback, { maximumAge: 600000, timeout: 5000, enableHighAccuracy: true });
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 16,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiY2hpcmljaGlnbm9hIiwiYSI6ImNqaXVteTNtejB4dmQza2xnNWJ5NXNsYjgifQ.5tA7QptUogzoAmQ8S3m10g'
    }).addTo(mymap);
    mymap.doubleClickZoom.disable();
    mymap.on('dblclick', dblClickCallback);
};