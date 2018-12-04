import React, {Component} from "react"
import {Button, ButtonGroup} from "reactstrap"
import * as api from '../../api'
import CafeCard from '../../common/CafeCard'

export default class Cafe extends Component {
    constructor(props) {
        super(props);
        this.state = {
            sorting: '',
            selected: null,
            cafes: []
        }

        // JWT를 local storage에 바로 저장한다.
        window.localStorage.setItem('token', this.props.token);
        this.getCafeList = this.getCafeList.bind(this)

    }

    componentDidMount() {
        // 처음에는 인기순으로 정렬하여 보여준다
        this.getCafeList('popularity', 1)

    }

    getCafeList(sorting, selected) {
        // sorting 옵션에 따라 카페 목록을 가져와서 업데이트 하고 해당 버튼을 눌러준다
        api.getCafes(sorting)
            .then(res => res.json())
            .then(res => {
                this.setState({
                    cafes: res,
                    selected: selected
                })
            })
            .catch(err => {
                alert(err)
            })
    }


    render() {
        let description = "여러분들이 알고 있는 카페를 등록하면 여기에 정보가 나타납니다.\n그러면 회원들이 카페에서 커모를 열 수 있어요!"
        return (
            <div className="cafe-view">
                <div className="cafe-view-title-container">
                    <div className="cafe-view-title">카페 리스트</div>
                    <div className="cafe-view-subtitle">카페인 회원들이 등록한 카페들이에요!</div>
                </div>
                <hr/>
                <div className="cafe-view-description">{description}</div>
                <ButtonGroup className="cafe-sort-button-container">
                    <Button outline color="secondary"
                            size="lg"
                            onClick={() => this.getCafeList('popularity', 1)}
                            active={this.state.selected == 1}>인기순</Button>
                    <Button outline color="secondary"
                            size="lg"
                            onClick={() => this.getCafeList('photo', 2)}
                            active={this.state.selected == 2}>사진 많은순</Button>
                    <Button outline color="secondary"
                            size="lg"
                            onClick={() => this.getCafeList('recent', 3)}
                            active={this.state.selected == 3}>최신순</Button>
                    <Button outline color="secondary"
                            size="lg"
                            onClick={() => this.getCafeList('random', 4)}
                            active={this.state.selected == 4}>랜덤랜덤</Button>
                </ButtonGroup>
                <div className="container-fluid">
                    {this.state.cafes.map((cafe, i) => {
                        return <CafeCard key={i} cafe={cafe}/>
                    })}
                </div>
            </div>
        )
    }

}
