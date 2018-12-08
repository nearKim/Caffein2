import React, {Component} from "react"
import Slider from "react-slick";
import {Table, Button} from "reactstrap"
import * as api from '../../api'

export default class CafeDetail extends Component {
    constructor(props) {
        super(props)

        this.state = {
            cafe: null,
            photos: []
        }

        // JWT를 local storage에 바로 저장한다.
        window.localStorage.setItem('token', this.props.token);

        this.getCafeData = this.getCafeData.bind(this)
    }

    componentDidMount() {
        // cafe 데이터와 카페 사진들을 넣어준다
        this.getCafeData()
    }

    getCafeData() {
        // 단일 카페 데이터를 받아온 후 카페 사진들을 따로 flatten시켜서 state로 관리해준다
        api.getCafe(this.props.cafe_id)
            .then(res => res.json())
            .then(res => {
                this.setState({
                    cafe: res,
                    photos: res.photos.flatMap(photo => photo.image)
                })
                //  카페 데이터가 모두 전송되면 네이버지도에 데이터를 뿌려준다
                this.loadNaverMap(res.mapx, res.mapy)
            })
    }

    loadNaverMap(x, y) {
        let position = new naver.maps.Point(x, y)

        let map = new naver.maps.Map(this.navermap, {
            center: position,
            zoom: 10,
            mapTypes: new naver.maps.MapTypeRegistry({
                'normal': naver.maps.NaverMapTypeOption.getNormalMap({
                    projection: naver.maps.TM128Coord
                })
            }),
        })
        let marker = new naver.maps.Marker({
            map: map,
            position: position,
            zIndex: 100,
        })
    }

    render() {
        let photos = this.state.photos
        let cafe = this.state.cafe

        const settings = {
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 1,
            slidesToScroll: 1
        };

        return (
            <div className="cafe-detail">
                {cafe ?
                    <div className="cafe-detail-container">
                        <div className="cafe-detail-main">
                            <p>{cafe.name}</p>
                            <p className="cafe-detail-upload-info">
                                <img src={cafe.uploader.profile_pic}/> {cafe.uploader.name}님이 {cafe.created}에 등록한 카페입니다.
                            </p>
                            {cafe.last_modifier ?
                                <p className="cafe-detail-modify-info">
                                    <img src={cafe.last_modifier.profile_pic}/> {cafe.last_modifier.name}님이 {cafe.modified}에 마지막으로 수정했습니다.</p>
                                : null}
                        </div>
                        {photos.length == 0 ?
                            <div className="cafe-detail-no-photos">아직 사진이 없습니다. 카페 사진을 업로드해주세요!</div>
                            :
                            <Slider className="cafe-detail-photo-slider" {...settings}>
                                {photos.map((photo, i) => {
                                    return (
                                        <div key={i} className="cafe-detail-photo">
                                            <img src={photo}/>
                                        </div>
                                    )
                                })}
                            </Slider>
                        }
                        <Table className="cafe-detail-info-table" responsive>
                            <tbody>
                            <tr>
                                <th>카페</th>
                                <td>{cafe.name}</td>
                            </tr>
                            <tr>
                                <th>주소</th>
                                <td>{cafe.address}</td>
                            </tr>
                            <tr>
                                <th>전화번호</th>
                                <td>{cafe.phone}</td>
                            </tr>
                            <tr>
                                <th>에스프레소 머신</th>
                                <td>{cafe.machine ? cafe.machine : '아직 몰라요!'}</td>
                            </tr>
                            <tr>
                                <th>그라인더</th>
                                <td>{cafe.grinder ? cafe.grinder : '아직 몰라요!'}</td>
                            </tr>
                            <tr>
                                <th>영업시간</th>
                                <td>{cafe.from_time ? cafe.from_time : '아직 몰라요!'} ~ {cafe.to_time ? cafe.to_time : '아직 몰라요!'}</td>
                            </tr>
                            <tr>
                                <th>휴무일 / 공휴일 휴무</th>
                                <td>{cafe.closed_day ? cafe.closed_day : '아직 몰라요!'} / {cafe.closed_holiday ? cafe.closed_holiday : '아직 몰라요!'}</td>
                            </tr>
                            <tr>
                                <th>가격대</th>
                                <td>{cafe.price ? cafe.price : '아직 몰라요!'}</td>
                            </tr>
                            </tbody>
                        </Table>
                        <div className="cafe-detail-description">
                            <p>Description</p>
                            {cafe.description ? cafe.description : '카페 설명을 입력해주세요!'}

                        </div>
                        <div className="cafe-detail-navermap"
                             ref={ref => {
                                 this.navermap = ref
                             }}
                             style={{width: '100%', height: 500}}></div>
                        <div className="cafe-detail-button-container">
                            <Button outline color="primary" className="cafe-detail-cafe-list-btn">카페 리스트로</Button>
                            <Button outline color="primary" className="cafe-detail-cafe-edit-btn">정보 수정하기</Button>
                            <Button color="primary" className="cafe-detail-coffeemeeting-create-btn">커모 열기!</Button>
                        </div>
                    </div>
                    : null}
            </div>
        )
    }
}