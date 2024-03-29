import React from 'react';

import {formatNumber} from '../../helpers/utils';
import {PlusCircleIcon, MinusCircleIcon, TrashIcon} from '../../components/icons';
import {useCart} from "react-use-cart";
import CartService from "../../services/cart/cart.service";

const CartItem = ({product}) => {

    const {removeItem, updateItemQuantity} = useCart();

    function Update(product, quantity) {
        CartService.update(product.id, quantity).then(
            () => {
                updateItemQuantity(product.id, quantity)
            },
            error => {
                console.log(error)
            }
        );
    }

    function Remove(uuid) {
        CartService.remove(uuid).then(
            () => {
                removeItem(uuid)
            },
            error => {
                console.log(error)
            }
        );
    }

    return (
        <div className="row no-gutters py-2">
            <div className="col-sm-2 p-2">
                <img
                    alt={product.title}
                    style={{margin: "0 auto", maxHeight: "50px"}}
                    src={product.photo} className="img-fluid d-block"/>
            </div>
            <div className="col-sm-4 p-2">
                <h5 className="mb-1">{product.title}</h5>
                <p className="mb-1">Price: {formatNumber(product.price)} </p>

            </div>
            <div className="col-sm-2 p-2 text-center ">
                <p className="mb-0">Qty: {product.quantity}</p>
            </div>
            <div className="col-sm-4 p-2 text-right">
                <button
                    onClick={() => Update(product, product.quantity + 1)}
                    className="btn btn-primary btn-sm mr-2 mb-1">
                    <PlusCircleIcon width={"20px"}/>
                </button>

                {
                    product.quantity > 1 &&
                    <button
                        onClick={() => Update(product, product.quantity - 1)}
                        className="btn btn-danger btn-sm mr-2 mb-1">
                        <MinusCircleIcon width={"20px"}/>
                    </button>
                }

                <button
                    onClick={() => Remove(product.id)}
                    className="btn btn-danger btn-sm mb-1">
                    <TrashIcon width={"20px"}/>
                </button>

            </div>
        </div>
    );
}

export default CartItem;