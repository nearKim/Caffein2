import React, {Component} from "react"
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
        return (
            <div>
                test
            </div>
        )
    }
}