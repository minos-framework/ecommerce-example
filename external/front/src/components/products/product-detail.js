import React from 'react';
import {Breadcrumb, Button, Card, Col, Image, Row} from "react-bootstrap";
import axios from "axios";
import {RatingView} from "react-simple-star-rating";
import Reviews from "../reviews/reviews";

class ProductDetail extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            uuid: this.props.match.params.id
        }
    }

    componentDidMount() {
        this.getProduct()
    }

    getProduct() {
        axios.get(`http://localhost:5566/products/${this.state.uuid}`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                this.setState({...response.data})
            })
            .catch(error => {
                console.log("Error")
            })
    }

    componentWillReceiveProps(nextProps) {

    }

    render() {
        const {uuid, title, description, price, reviews_count, reviews_score} = this.state

        return (
            <div>
                <Row className="mt-3">
                    <Col>
                        <Breadcrumb>
                            <Breadcrumb.Item href="/">Home</Breadcrumb.Item>
                            <Breadcrumb.Item href="/products">
                                Products
                            </Breadcrumb.Item>
                            <Breadcrumb.Item active>{title}</Breadcrumb.Item>
                        </Breadcrumb>
                    </Col>
                </Row>
                <Row className="mt-3">
                    <Col md={6}>
                        <Image fluid
                               src="https://knowledge.insead.edu/sites/www.insead.edu/files/styles/w_650/public/styles/panoramic/public/images/2014/02/coke.jpg?itok=nMcR-Ore"/>
                    </Col>
                    <Col md={6}>
                        <h2>
                            {title}
                        </h2>
                        <p>
                            <RatingView ratingValue={reviews_score}/>
                            <span className="ml-2 align-top">{reviews_count}</span>
                        </p>

                        <hr className="mr-5"
                            style={{
                                color: "#f3f3f3",
                                backgroundColor: "#f3f3f3",
                                height: 1
                            }}
                        />
                        <h5 className="pl-0">
                            <span className="mr-2">Precio: </span>
                            <span className="font-weight-bold">{price}</span>
                            <small className="ml-2 align-top">€</small>
                        </h5>
                        <p>
                            {description}
                        </p>

                        <Button variant="add-to-cart" size="lg">Add to cart</Button>
                    </Col>
                </Row>

                <Row className="mt-3">
                    <Reviews uuid={"7f722bca-cd5f-4a9b-a6dd-d5db233e4ebf"}/>
                </Row>
            </div>
        );
    }
}

export default ProductDetail;
