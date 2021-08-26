import React from 'react';
import {Button, Card, Col, Image, Row} from "react-bootstrap";
import {RatingView} from 'react-simple-star-rating'
import StyledLink from '../shared/styled-link'

class Review extends React.Component {

    constructor(props) {
        super(props);

        this.state = {}
    }

    componentDidMount() {
        this.setState({
            ...this.props,
        });
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            product: nextProps.product,
        });
    }

    render() {
        const {uuid, title, description, score, product_title, username, date} = this.state

        return (
            <div className="ml-2 mb-3">
                <Row>
                    <Col lg={12} className="">
                        <Image style={{height: "30px"}} fluid
                               src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8aeC_UjZe73ObBPqh-v_FlnBli69L7lcqonvSlp2WlOtjtV3u9PHJrGUuWzLPzEUzE2o&usqp=CAU"/>
                        <span className="ml-2 align-top ">{username}</span>
                    </Col>
                </Row>
                <Row>
                    <Col lg={12} className="ml-4 mt-1 d-flex">
                        <RatingView ratingValue={score}/>
                        <h5 className="ml-2 align-top font-weight-bold">{title}</h5>
                    </Col>
                </Row>
                <Row>
                    <Col lg={12} className="ml-4 mt-1 d-flex">
                        {description}
                    </Col>
                </Row>
            </div>

        );
    }
}

export default Review;
