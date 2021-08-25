import React from 'react';
import {Button, Card, Col, Image, Row} from "react-bootstrap";
import axios from "axios";
import {RatingView} from "react-simple-star-rating";

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
        axios.get(`http://localhost:5566/products/product/${this.state.uuid}`, {
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

                    <p>
                        <hr className="mr-5"
                            style={{
                                color: "#f3f3f3",
                                backgroundColor: "#f3f3f3",
                                height: 1
                            }}
                        />
                    </p>
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
        );
    }
}

export default ProductDetail;
