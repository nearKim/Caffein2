// 초기화 및 상수 선언
let markers = []
let infoWindows = []
let positions = []
let places = appConfig.places

let map = new naver.maps.Map("map", {
    // 서울대학교
    center: new naver.maps.Point(307362, 540205),
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
})

// places의 결과 개수에 따라 분기해야 한
switch (places.length) {
    case 0:
        console.log("0")
        alert('검색 결과가 없습니다.')
        break
    case 1:
        console.log("1")
        let position = new naver.maps.Point(places[0].mapx, places[0].mapy)
        map.setCenter(position)
        map.setZoom(10)
        break
    default:
        console.log("other")
        console.log(places)
        places.forEach(place => {
            let position = new naver.maps.Point(place.mapx, place.mapy)
            let contentString = [
                '<div class="iw_inner">',
                '<h3>' + place.title + '</h3>',
                '<p>' + place.roadAddress + '</p>',
                '<p>' + place.address + '</p>',
                '<p>' + place.description + '</p>',
                '<a href="' + place.link + '">' + place.link + '</a>',
                '</div>'
            ].join('');

            positions.push(position)
            markers.push(new naver.maps.Marker({
                map: map,
                position: position,
                title: place.title,
                zIndex: 100
            }))
            infoWindows.push(new naver.maps.InfoWindow({
                content: contentString
            }))
        })

        map.fitBounds(positions)
        naver.maps.Event.addListener(map, 'idle', () => updateMarkers(map, markers))


}

for (var i = 0, ii = markers.length; i < ii; i++) {
    naver.maps.Event.addListener(markers[i], 'click', getClickHandler(i));
}

function updateMarkers(map, markers) {

    var mapBounds = map.getBounds();
    markers.map(marker => {
        let position = marker.getPosition()
        mapBounds.hasPoint(position) ? showMarker(map, marker) : hideMarker(map, marker)
    })
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
    return e => {
        var marker = markers[seq]
        var infoWindow = infoWindows[seq]
        infoWindow.getMap() ? infoWindow.close() : infoWindow.open(map, marker)
    }
}

