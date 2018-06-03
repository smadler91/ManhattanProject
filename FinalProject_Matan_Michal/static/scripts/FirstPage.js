//  Java Script for First Page.HTML:

$("#id_postjson").click(function () {
    $.ajax({
        url: "getname",
        method: 'POST',
        data: { name: "guy", color: "green" },
        context: document.body
    }).done(function (data) {
        console.log(data);
        alert(data);
    });
});

$("#id_getjson").click(function () {
    $.ajax({
        url: "getjson",
        context: document.body
    }).done(function (data) {
        console.log(data);
        alert(JSON.stringify(data));
    });
});

$(document).ready(function () {
    navigator.geolocation.getCurrentPosition(success, error, options);
});

var options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
};

function success(pos) {

    var mapCanvas = document.getElementById("map");
    var crd = pos.coords;
    var myLat = 40.7830603; //crd.latitude;
    var myLon = -73.97124880000001; //crd.longitude;
    var myCenter = new google.maps.LatLng(myLat, myLon);
    var mapOptions = {
        center: myCenter,
        zoom: 10,
        panControl: true,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        overviewMapControl: false,
        rotateControl: false
    };
    var map = new google.maps.Map(mapCanvas, mapOptions);

    addMarker(map, myLat, myLon, 'RED')
    getNearestBusiness(map, myLat, myLon) 
    getAllBusinesses(map)    
}

function error(err) {
    var x = document.getElementById("errors");
    x.innerHTML = "Geolocation is not supported by this browser.";
}

function addMarker(map, lat, lon, color) {
    var new_marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(lat, lon),
        icon: iconPath(color),
    });       
}

function iconPath(color) {
    if (color == 'YELLOW') {
        return "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"
    }
    else if (color == 'GREEN') {
        return "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
    }
    else {
        return "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
    }
}

function getNearestBusiness(map, lat, lon) {
    $.ajax({
        url: "getNearestBusiness",
        method: 'POST',
        data: { Lat: lat, Lon: lon },
        context: document.body
    }).done(function (data) {
        console.log(data);
        var lat = JSON.stringify(data['Lat'])
        var lon = JSON.stringify(data['Lon'])
        addMarker(map, lat, lon, 'YELLOW')
    });
}

function getAllBusinesses(map) {
    $.ajax({url: "getAllBusinesses",context: document.body}).done(function (data) {
        console.log(data);
        var POIs = data['POIs'];
        var len = POIs.length;
        for (i = 0; i < len; i++) {
            
            var POI = POIs[i]
            alert(POI);
            var lat = float(POI[0]);
            var lon = float(POI[1]);
            var name = POI[2];
            var id = int(POI[3]);
            var popularity = int(POI[4]);
            var type = POI[5];
            addMarker(map, lat, lon, 'GREEN');
        };
    });
        /*
        var json = {
            "st_asgeojson": {
                "type": "LineString",
                "coordinates": [
                    [40.6892494, -74.0445004],
                    [40.6994748, -74.0395586999999],
                    [40.71313, -74.0154149999999],
                    [40.711576, -74.0132769],
                    [40.7060006, -74.008801],
                    [40.7032775, -74.0170279]
                ]
            }
        }

        var coords = json.st_asgeojson.coordinates;

        coords.forEach(function (entry) {
            var lat = entry[0];
            var lon = entry[1];
            addMarker(map, lat, lon, 'GREEN')
        });*/
}