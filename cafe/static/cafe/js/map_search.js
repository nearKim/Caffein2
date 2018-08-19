// 초기화
// markers는 place_search에 선언된 전역변수를 사용한다
infoWindows = appConfig.infoWindows
positions = appConfig.positions
places = appConfig.places

map = new naver.maps.Map("map", {
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
                '<div class="iw_inner" >',
                '<h3>' + place.title + '</h3>',
                '<p>' + place.roadAddress + '</p>',
                '<p>' + place.address + '</p>',
                '<p>' + place.description + '</p>',
                '</div>'
            ].join('');

            // 전역 배열들에 데이터를 푸시한다.
            positions.push(position)
            appConfig.markers.push(new naver.maps.Marker({
                map: map,
                position: position,
                zIndex: 100,
                title: place.title,

                //  자동 필드 추가를 위해 마커에 지역정보를 포함시킨다
                address: place.address ? place.address : place.roadAddress,
                // 지번주소가 없다면 디폴트로 도로명주소가 주소에 삽입된다. 이경우 도로명주소를 따로 저장할 필요는 없다.
                roadAddress: place.address ? place.roadAddress : null,
                description: place.description ? place.description : '',
                telephone: place.telephone ? place.telephone : '',
                link: place.link
            }))
            infoWindows.push(new naver.maps.InfoWindow({
                content: contentString,

                backgroundColor: "#eee",
                anchorSize: new naver.maps.Size(30, 30),
                anchorSkew: true,
                anchorColor: "#eee",

                pixelOffset: new naver.maps.Point(20, -20)
            }))
        })

        map.fitBounds(positions)
        naver.maps.Event.addListener(map, 'idle', () => updateMarkers(map, appConfig.markers))


}

appConfig.markers.forEach((marker, index) => naver.maps.Event.addListener(marker, 'click', () => {
    // TODO: infoWindow의 인덱스와 marker의 인덱스가 항상 동일해야 한다. 보장되는지 확인 필요.
    let infoWindow = infoWindows[index]
    infoWindow.getMap() ? infoWindow.close() : infoWindow.open(map, marker)

    // Cafe create에서 이 페이지가 로드되었을 경우 각 폼을 자동으로 채워준다
    if ($('input[name="name"]').length) {
        // 네이버 지역정보 쿼리 결과는 title이 <b> 태그로 둘러쌓여있다. 태그를 제거해준다.
        $($('input[name="name"]')).val((marker.title).replace(/<\/?[^>]+(>|$)/g, ""))
        $($('input[name="address"]')).val(marker.address)
        $($('input[name="phone"]')).val(marker.telephone)
        $($('textarea[name="description"]')).val(marker.description)
        $($('input[name="link"]')).val(marker.link)
        // 이하 Hidden Input
        $($('input[name="road_address"]')).val(marker.roadAddress)
        $($('input[name="mapx"]')).val(marker.position.x)
        $($('input[name="mapy"]')).val(marker.position.y)
    }
    // Officialmeeting create이나 CoffeeEducation Create에서 넘어온 경우 location 폼을 채워준다
        $($('input[name="location"]')).val((marker.title).replace(/<\/?[^>]+(>|$)/g, ""))
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
}

function hideMarker(map, marker) {
    if (!marker.setMap()) return;
    marker.setMap(null);
}
