import React, {Component} from "react"
import Slider from "react-slick";
import {Button, ButtonGroup} from "reactstrap"
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
            })
    }

    render() {
        let cafe = this.state.cafe
        const settings = {
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 1,
            slidesToScroll: 1
        };

        return (
            <div>
                <Slider {...settings}>
                    <div>
                        <h3>1</h3>
                    </div>
                    <div>
                        <h3>2</h3>
                    </div>
                    <div>
                        <h3>3</h3>
                    </div>
                    <div>
                        <h3>4</h3>
                    </div>
                    <div>
                        <h3>5</h3>
                    </div>
                    <div>
                        <h3>6</h3>
                    </div>
                </Slider>
            </div>
        )
    }
}