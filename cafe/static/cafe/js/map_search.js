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
        // 초기화면의 경우, 검색 결과가 없는 경우, 빈칸을 입력한 경우 아무것도 보여주지 않는다.
        // TODO: 검색 결과가 없는 경우 alert창을 띄워주는 것이 좋다.
        break
    case 1:
        // GET을 통해 들어온 경우 지도만 보여준다.
        if (places[0] === 'init') break
        let position = new naver.maps.Point(places[0].mapx, places[0].mapy)
        map.setCenter(position)
        map.setZoom(10)
        break
    default:
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

markers.forEach((marker, index) => naver.maps.Event.addListener(marker, 'click', () => {
    // TODO: infoWindow의 인덱스와 marker의 인덱스가 항상 동일해야 한다. 보장되는지 확인 필요.
    // TODO: marker에 클릭 리스너 등록 필요
    let infoWindow = infoWindows[index]
    infoWindow.getMap() ? infoWindow.close() : infoWindow.open(map, marker)
    document.getElementById('selected-marker').innerText = infoWindow.contentElement.innerText
}))

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
    console.log(marker)
}

function hideMarker(map, marker) {
    if (!marker.setMap()) return;
    marker.setMap(null);
}

// 해당 마커의 인덱스를 seq라는 클로저 변수로 저장하는 이벤트 핸들러를 반환합니다.
// function getClickHandler(seq) {
//     return e => {
//         var marker = markers[seq]
//         var infoWindow = infoWindows[seq]
//         infoWindow.getMap() ? infoWindow.close() : infoWindow.open(map, marker)
//     }
// }

