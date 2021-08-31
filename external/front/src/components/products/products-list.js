import React from 'react';
import axios from "axios";

import ProductCard from "./product-item";
import {Row, Col, Breadcrumb} from "react-bootstrap";
import styles from './ProductsGrid.module.scss';

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
                    photo="https://knowledge.insead.edu/sites/www.insead.edu/files/styles/w_650/public/styles/panoramic/public/images/2014/02/coke.jpg?itok=nMcR-Ore"
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
                <div className={styles.p__grid}>
                    {products}
                </div>
            </div>

        );
    }
}

export default Products;