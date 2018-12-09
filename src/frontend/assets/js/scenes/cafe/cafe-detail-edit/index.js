import React, {Component} from "react"
import * as api from '../../../api'
import CafeDetailView from "./scenes/CafeDetailView";

export default class CafeDetailEdit extends Component {
    constructor(props) {
        super(props)

        this.state = {
            viewmode: null,
            cafe: null,
            photos: []
        }

        // JWT를 local storage에 바로 저장한다.
        window.localStorage.setItem('token', this.props.token);

        this.getCafeData = this.getCafeData.bind(this)
        this.onCafeEditButtonClicked = this.onCafeEditButtonClicked.bind(this)
    }

    componentDidMount() {
        // cafe 데이터와 카페 사진들을 넣어준다
        this.getCafeData()
    }

    // 단일 카페 데이터를 받아온 후 카페 사진들을 따로 flatten시켜서 state로 관리해준다
    getCafeData() {
        api.getCafe(this.props.cafe_id)
            .then(res => res.json())
            .then(res => {
                this.setState({
                    viewmode: 'detail',
                    cafe: res,
                    photos: res.photos.flatMap(photo => photo.image)
                })
            })
    }

    // 카페 수정하기 버튼이 눌렸을때 viewmode를 바꿔준다.
    onCafeEditButtonClicked(event) {
        event.preventDefault()
        this.setState({viewmode: 'edit'})
    }

    render() {
        return (
            <div className="cafe-detail">
                {this.state.viewmode == 'detail' ?
                    <CafeDetailView
                        cafe={this.state.cafe}
                        photos={this.state.photos}
                        editButtonClickHandler={this.onCafeEditButtonClicked}/>
                    : null}
            </div>
        )
    }
}