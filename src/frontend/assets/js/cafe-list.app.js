import React from "react";
import ReactDOM from "react-dom"
import dataset from 'dataset'
import CafeList from "./scenes/cafe/cafe-list"

const root = document.getElementById("root")
if (root) {
    const props = {
        token: root.dataset ? root.dataset.token : dataset(root, 'token')
    }

    ReactDOM.render(<CafeList {...props} />, root)
}
