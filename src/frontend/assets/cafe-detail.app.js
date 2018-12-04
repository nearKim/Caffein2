import React from "react";
import ReactDOM from "react-dom"
import dataset from 'dataset'
import CafeDetail from '../assets/scenes/cafeDetail'

const root = document.getElementById("root")
if (root) {
    const props = {
        token: root.dataset ? root.dataset.token : dataset(root, 'token'),
        cafe_id: root.dataset ? root.dataset.cafe_id : dataset(root, 'cafe_id')
    }

    ReactDOM.render(<CafeDetail {...props} />, root)
}
