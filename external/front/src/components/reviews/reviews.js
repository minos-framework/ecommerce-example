import React from 'react';
import axios from "axios";

import {Row, Col, CardGroup} from "react-bootstrap";
import Review from "./review";

class Reviews extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            reviews: null
        }
    }

    componentDidMount() {
        this.setState({
            uuid: this.props.uuid,
        });
        this.setState({uuid: this.props.uuid}, () => {
            this.getReviews()
        });
    }

    getReviews() {
        axios.get(`http://localhost:5566/reviews/product/${this.state.uuid}`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                this.setState({reviews: response.data})
                console.log(this.state)
            })
            .catch(error => {
                console.log("Error")
            })
    }

    render() {
        let reviews = []

        console.log(this.state.reviews)
        if (this.state.reviews !== null && this.state.reviews.length > 0) {

            for (let i = 0; i < this.state.reviews.length; i++) {
                let review = this.state.reviews[i]
                reviews.push(<Review
                    uuid={review.uuid}
                    title={review.title}
                    description={review.description}
                    score={review.score}
                    product_title={review.product_title}
                    username={review.username}
                    date={review.date}
                />)
            }
        }

        return (
            <div>
                <Row>
                    <Col>
                        <h2 className="ml-4">Customer feedback</h2>
                    </Col>
                </Row>
                <div className="ml-4">
                    {reviews}
                </div>
            </div>
        );
    }
}

export default Reviews;