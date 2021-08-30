import React from 'react';

import {formatNumber} from '../../helpers/utils';
import {PlusCircleIcon, MinusCircleIcon, TrashIcon} from '../../components/icons';
import {useCart} from "react-use-cart";
import CartService from "../../services/cart/cart.service";

const Item = ({product}) => {

    const {removeItem, updateItemQuantity} = useCart();

    return (
        <div className="row no-gutters py-2">
            <div className="col-sm-2 p-2">
                <img
                    alt={product.title}
                    style={{margin: "0 auto", maxHeight: "50px"}}
                    src={product.photo} className="img-fluid d-block"/>
            </div>
            <div className="col-sm-3 p-2">
                <h5 className="mb-1">{product.title}</h5>
                <p className="mb-1">Price: {formatNumber(product.price)} </p>

            </div>
            <div className="col-sm-2 p-2 text-center ">
                <p className="mb-0">Qty: {product.quantity}</p>
            </div>

        </div>
    );
}

export default Item;