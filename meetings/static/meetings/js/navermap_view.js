/*
OfficialMeeting, CoffeeEducation DetailView에서 사용할 네이버지도 자바스크립트.
각 템플릿에서 장소의 mapx, mapy, 장소명을를 각각 x,y,location 변수로 받아야 한다.
 */

let position = new naver.maps.Point(x, y)

map = new naver.maps.Map("map", {
    center: position,
    zoom: 10,
    mapTypes: new naver.maps.MapTypeRegistry({
        'normal': naver.maps.NaverMapTypeOption.getNormalMap({
            projection: naver.maps.TM128Coord
        })
    }),
})
marker = new naver.maps.Marker({
    map: map,
    position: position,
    zIndex: 100,
})
infoWindow = new naver.maps.InfoWindow({
    content: location_title,
    backgroundColor: "#eee",
    anchorSize: new naver.maps.Size(30, 30),
    anchorSkew: true,
    anchorColor: "#eee",

    pixelOffset: new naver.maps.Point(20, -20)
})
naver.maps.Event.addListener(marker, 'click', () => {
    infoWindow.getMap() ? infoWindow.close() : infoWindow.open(map, marker)
})