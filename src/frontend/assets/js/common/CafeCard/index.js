import React, {Component} from "react"
import {
    Col, Row, Card, CardImg, CardText, CardBody,
    CardTitle, CardSubtitle, CardFooter, Button
} from "reactstrap"


export default class CafeCard extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        let cafe = this.props.cafe
        return (
            <Row>
                <Col sm="3">
                    <Card>
                        <CardImg top width="100%"
                                 className="cafecard-image"
                                 src={cafe.photos.length !== 0 ?
                                     cafe.photos[0].image :
                                     'https://placeholdit.imgix.net/~text?txtsize=33&txt=318%C3%97180&w=318&h=180'}
                                 alt="Card image cap"/>
                        <CardBody>
                            <CardTitle className="cafecard-title">{cafe.name}</CardTitle>
                            <CardSubtitle className="cafecard-subtitle">
                                이 카페에서 커모가 {cafe.num_meetings}번 열렸어요!
                            </CardSubtitle>
                            <CardText className="cafecard-body">
                                {cafe.description ? cafe.description : '아직 카페 설명이 없어요. 채워주세요!'}
                            </CardText>
                            <Button>Button</Button>
                        </CardBody>
                        <CardFooter className="cafecard-footer text-muted">
                            {cafe.uploader.name} 님이 등록한 카페입니다
                        </CardFooter>
                    </Card>
                </Col>
            </Row>
        )
    }
}