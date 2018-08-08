//var items = appConfig.items;
//alert(appConfig.items[0])


var map = new naver.maps.Map("map", {
    //center: new naver.maps.LatLng(37.3595316, 127.1052133),
    center: new naver.maps.Point(307362, 540205),
    //center: new naver.maps.Point(Number(items[0].mapx), Number(items[0].mapy)),
    zoom: 10,
    mapTypes: new naver.maps.MapTypeRegistry({
            'normal': naver.maps.NaverMapTypeOption.getNormalMap({
                projection: naver.maps.TM128Coord
            }),
            'terrain': naver.maps.NaverMapTypeOption.getTerrainMap({
                projection: naver.maps.TM128Coord
            }),
            'satellite': naver.maps.NaverMapTypeOption.getSatelliteMap({
                projection: naver.maps.TM128Coord
            }),
            'hybrid': naver.maps.NaverMapTypeOption.getHybridMap({
                projection: naver.maps.TM128Coord
            })
        }),
    mapTypeControl: true
});
//var bounds = map.getBounds();
    //southWest = bounds.getSW(),
    //northEast = bounds.getNE(),
    //lngSpan = northEast.lng() - southWest.lng(),
    //latSpan = northEast.lat() - southWest.lat();
if(items.length != 0) {
    var items = appConfig.items;
    var markers = [],
        infoWindows = [],
        positions = [];

    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var position = new naver.maps.Point(item.mapx, item.mapy);
        var marker = new naver.maps.Marker({
            map: map,
            position: position,
            title: i,
            zIndex: 100
        });
        var contentString = [
            '<div class="iw_inner">',
            '<h3>' + item.title + '</h3>',
            '<p>' + item.roadAddress + '</p>',
            '<p>' + item.address + '</p>',
            '<p>' + item.description + '</p>',
            '<a href="' + item.link + '">' + item.link + '</a>',
            '</div>'
        ].join('');
        var infoWindow = new naver.maps.InfoWindow({
            content: contentString
        });
        markers.push(marker);
        infoWindows.push(infoWindow);
        positions.push(position);
    }
    ;

    naver.maps.Event.addListener(map, 'idle', function () {
        updateMarkers(map, markers);

    });

    if (items.length == 1) {
        var position = new naver.maps.Point(items[0].mapx, items[0].mapy);
        map.setCenter(position);
        map.setZoom(10);
    } else {
        map.fitBounds(positions);
    }

    function updateMarkers(map, markers) {

        var mapBounds = map.getBounds();
        var marker, position;

        for (var i = 0; i < markers.length; i++) {

            marker = markers[i]
            position = marker.getPosition();
            //if (mapBounds.hasLatLng(position)) {
            if (mapBounds.hasPoint(position)) {
                showMarker(map, marker);
            } else {
                hideMarker(map, marker);
            }
        }
    }

    function showMarker(map, marker) {

        if (marker.setMap()) return;
        marker.setMap(map);
    }

    function hideMarker(map, marker) {

        if (!marker.setMap()) return;
        marker.setMap(null);
    }

// 해당 마커의 인덱스를 seq라는 클로저 변수로 저장하는 이벤트 핸들러를 반환합니다.
    function getClickHandler(seq) {
        return function (e) {
            var marker = markers[seq],
                infoWindow = infoWindows[seq];

            if (infoWindow.getMap()) {
                infoWindow.close();
            } else {
                infoWindow.open(map, marker);
            }
        }
    }

    for (var i = 0, ii = markers.length; i < ii; i++) {
        naver.maps.Event.addListener(markers[i], 'click', getClickHandler(i));
    }
}
/*

var infoWindow = new naver.maps.InfoWindow({
    anchorSkew: true
});

map.setCursor('pointer');

// search by tm128 coordinate
function searchCoordinateToAddress(latlng) {
    var tm128 = naver.maps.TransCoord.fromLatLngToTM128(latlng);

    infoWindow.close();

    naver.maps.Service.reverseGeocode({
        location: tm128,
        coordType: naver.maps.Service.CoordType.TM128
    }, function(status, response) {
        if (status === naver.maps.Service.Status.ERROR) {
            return alert('Something Wrong!');
        }

        var items = response.result.items,
            htmlAddresses = [];

        for (var i=0, ii=items.length, item, addrType; i<ii; i++) {
            item = items[i];
            addrType = item.isRoadAddress ? '[도로명 주소]' : '[지번 주소]';

            htmlAddresses.push((i+1) +'. '+ addrType +' '+ item.address);
        }

        infoWindow.setContent([
            '<div style="padding:10px;min-width:200px;line-height:150%;">',
            '<h4 style="margin-top:5px;">검색 좌표</h4><br />',
            htmlAddresses.join('<br />'),
            '</div>'
        ].join('\n'));

        infoWindow.open(map, latlng);
    });
}

// result by latlng coordinate
function searchAddressToCoordinate(address) {
    naver.maps.Service.geocode({
        address: address
    }, function(status, response) {
        if (status === naver.maps.Service.Status.ERROR) {
            return alert('Something Wrong!');
        }

        var item = response.result.items[0],
            addrType = item.isRoadAddress ? '[도로명 주소]' : '[지번 주소]',
            point = new naver.maps.Point(item.point.x, item.point.y);

        infoWindow.setContent([
            '<div style="padding:10px;min-width:200px;line-height:150%;">',
            '<h4 style="margin-top:5px;">검색 주소 : '+ response.result.userquery +'</h4><br />',
            addrType +' '+ item.address +'<br />',
            '</div>'
        ].join('\n'));


        map.setCenter(point);
        infoWindow.open(map, point);
    });
}

function initGeocoder() {
    map.addListener('click', function(e) {
        searchCoordinateToAddress(e.coord);
    });

    $('#address').on('keydown', function(e) {
        var keyCode = e.which;

        if (keyCode === 13) { // Enter Key
            searchAddressToCoordinate($('#address').val());
        }
    });

    $('#submit').on('click', function(e) {
        e.preventDefault();

        searchAddressToCoordinate($('#address').val());
    });

    searchAddressToCoordinate('');
}

naver.maps.onJSContentLoaded = initGeocoder;*/
