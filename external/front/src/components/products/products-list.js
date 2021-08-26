import React from 'react';
import axios from "axios";

import ProductCard from "./product-item";
import {Row, Col, CardGroup, Breadcrumb} from "react-bootstrap";
import Cart from "../cart";
class Products extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            products: null,
        }
    }

    componentDidMount() {
        this.getProducts()
    }

    getProducts() {
        axios.get(`http://localhost:5566/products`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                this.setState({products: response.data})
            })
            .catch(error => {
                console.log("Error")
            })
    }

    render() {
        let products = []

        if (this.state.products !== null && this.state.products.length > 0) {

            for (let i = 0; i < this.state.products.length; i++) {
                let product = this.state.products[i]
                products.push(<ProductCard
                    id={product.uuid}
                    title={product.title}
                    description={product.description}
                    price={product.price}
                    reviews_count={product.reviews_count}
                    reviews_score={product.reviews_score}
                />)
            }

        }
        return (
            <div>
                <Row className="mt-3">
                    <Col>
                        <Breadcrumb>
                            <Breadcrumb.Item href="/">Home</Breadcrumb.Item>
                            <Breadcrumb.Item active>Products</Breadcrumb.Item>
                        </Breadcrumb>
                    </Col>
                </Row>
                <Row>
                    <CardGroup>
                        {products}
                    </CardGroup>
                </Row>
                <Cart/>
            </div>

        );
    }
}

export default Products;