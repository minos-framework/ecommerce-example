import React, {useState} from 'react';
import {useCart} from "react-use-cart";
import {formatNumber} from "../../helpers/utils";
import {Link} from "react-router-dom";
import {RatingView} from "react-simple-star-rating";

function ProductCard(props) {
    const [product] = useState({...props});
    const detail_link = "/product/" + product.id
    const {addItem, inCart} = useCart();

    return (
        <div className="card card-body">
            <img style={{display: "block", margin: "0 auto 10px", maxHeight: "200px"}} className="img-fluid"
            src={product.photo} alt=""/>
            <p>{product.title}</p>
            <p>
                <RatingView ratingValue={product.reviews_score}/>
                <span className="ml-2 align-top">{product.reviews_count}</span>
            </p>
            <h4 className="text-left">{formatNumber(product.price)}</h4>
            <div className="text-right">
                <Link  to={detail_link} className="btn btn-link btn-sm mr-2">Details</Link>

                {(inCart(product.id)) ? (
                    <button
                    onClick={() => addItem(product)}
                    className="btn btn-outline-dark btn-sm">Add more</button>
                    ): (
                        <button
                    onClick={() => addItem(product)}
                    className="btn btn-dark btn-sm">Add to cart</button>
                )}


            </div>
        </div>
    );
}

export default ProductCard;
