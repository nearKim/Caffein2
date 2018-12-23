import React, {Component} from "react"
import { Button, Form, FormGroup, Label, Input, FormText } from 'reactstrap';

export default class CafeEditView extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        let {name, address, description, phone, machine, grinder,
            price, from_time, to_time, closed_day, closed_holiday, link} = this.props.cafe
        // TODO: implement here
        return (
            <Form className="cafe-edit-form">
                <FormGroup>
                    <Label/>
                    <Input />
                </FormGroup>

            </Form>
        )
    }
}