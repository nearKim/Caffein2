import React, {Component} from "react"
import * as api from '../../api'

export default class Cafe extends Component {
    constructor(props) {
        super(props);
        // JWT를 local storage에 바로 저장한다.
        window.localStorage.setItem('token', this.props.token);
    }

    componentDidMount() {
        api.getCafes().then(res => res.json()).then(res => console.log(res))
    }

    render() {
        return (
            <h1>test</h1>
        )
    }
}