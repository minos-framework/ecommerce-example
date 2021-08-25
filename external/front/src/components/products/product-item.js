import React from 'react';
import {Button, Card, Col} from "react-bootstrap";
import {RatingView} from 'react-simple-star-rating'
import StyledLink from '../shared/styled-link'

class ProductCard extends React.Component {

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
        const {uuid, title, description, price, reviews_count, reviews_score} = this.state

        return (
            <Col>
                <Card style={{width: '18rem'}} className="mt-3">
                    <StyledLink to={"/product/" + uuid}>

                    <Card.Img variant="top"
                              src="https://knowledge.insead.edu/sites/www.insead.edu/files/styles/w_650/public/styles/panoramic/public/images/2014/02/coke.jpg?itok=nMcR-Ore"/>
                    <Card.Body className="pl-0 pr-0 pb-2">
                        <Card.Title>{title}</Card.Title>
                        <RatingView ratingValue={reviews_score}/>
                        <span className="ml-2 align-top">{reviews_count}</span>
                        <Card.Text>
                            <h5>
                                <span className="font-weight-bold">{price}</span>
                                <small className="ml-2 align-top">€</small>
                            </h5>

                            {description}
                        </Card.Text>
                    </Card.Body>
                        </StyledLink>
                    <Button variant="add-to-cart" size="lg">Add to cart</Button>
                </Card>
            </Col>
        );
    }
}

export default ProductCard;
