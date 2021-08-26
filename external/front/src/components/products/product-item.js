import React, {useState} from 'react';
import {Button, Card, Col} from "react-bootstrap";
import {RatingView} from 'react-simple-star-rating'
import StyledLink from '../shared/styled-link'
import { useCart } from "react-use-cart";

function ProductCard(props) {
    const [product] = useState({...props});

    const { addItem } = useCart();

    return (
            <Col>
                <Card style={{width: '18rem'}} className="mt-3">
                    <StyledLink to={"/product/" + product.id}>

                    <Card.Img variant="top"
                              src="https://knowledge.insead.edu/sites/www.insead.edu/files/styles/w_650/public/styles/panoramic/public/images/2014/02/coke.jpg?itok=nMcR-Ore"/>
                    <Card.Body className="pl-0 pr-0 pb-2">
                        <Card.Title>{product.title}</Card.Title>
                        <RatingView ratingValue={product.reviews_score}/>
                        <span className="ml-2 align-top">{product.reviews_count}</span>
                        <Card.Text>
                            <h5>
                                <span className="font-weight-bold">{product.price}</span>
                                <small className="ml-2 align-top">€</small>
                            </h5>

                            {product.description}
                        </Card.Text>
                    </Card.Body>
                        </StyledLink>
                    <Button onClick={() => addItem(product)} variant="add-to-cart" size="lg">Add to cart</Button>
                </Card>
            </Col>
        );
}

export default ProductCard;
