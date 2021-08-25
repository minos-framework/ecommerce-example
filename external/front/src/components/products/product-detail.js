import React from 'react';
import {Button, Card, Col} from "react-bootstrap";
import axios from "axios";

class ProductDetail extends React.Component {

    constructor(props) {
        super(props);

        this.state = {}
    }

    componentDidMount() {
        this.getProduct()
    }

    getProduct() {
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

    componentWillReceiveProps(nextProps) {

    }

    render() {
        const { uuid, title, description, price, reviews_count, reviews_score } =  this.state

        return (
            <Col>
                <Card style={{ width: '18rem' }}>
                  <Card.Img variant="top" src="https://knowledge.insead.edu/sites/www.insead.edu/files/styles/w_650/public/styles/panoramic/public/images/2014/02/coke.jpg?itok=nMcR-Ore" />
                  <Card.Body>
                    <Card.Title>{title}</Card.Title>
                    <Card.Text>
                        {description}
                    </Card.Text>
                    <Button variant="primary">Add to cart</Button>
                  </Card.Body>
                </Card>
            </Col>
        );
    }
}

export default ProductDetail;
