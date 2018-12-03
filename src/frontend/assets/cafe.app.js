import React from "react";
import ReactDOM from "react-dom"
import dataset from 'dataset'
import Cafe from "./scenes/cafe"

const root = document.getElementById("root")
if (root) {
    const props = {
        token: root.dataset ? root.dataset.token : dataset(root, 'token')
    }

    ReactDOM.render(<Cafe {...props} />, root)
}
