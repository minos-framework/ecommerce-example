import React from 'react';
import axios from "axios";

import ProductCard from "./product-item";
import {Row, Col, CardGroup} from "react-bootstrap";

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

        if(this.state.products !== null && this.state.products.length > 0) {

            for (let i = 0; i < this.state.products.length; i++) {
                let product = this.state.products[i]
                products.push(<ProductCard
                    uuid={product.uuid}
                    title={product.title}
                    description={product.description}
                    price={product.price}
                    reviews_count={product.reviews_count}
                    reviews_score={product.reviews_score}
                />)
            }

        }
        return (
            <Row>
                <CardGroup>
                    {products}
                </CardGroup>
            </Row>
        );
    }
}

export default Products;