import React from 'react';
import { Link } from 'react-router-dom';

import CartProducts from './CartProducts';
import { formatNumber } from '../../helpers/utils';
import {useCart} from "react-use-cart";

function Cart() {

    const {
    isEmpty,
    totalUniqueItems,
    items,
        cartTotal,
    updateItemQuantity,
    removeItem,
        emptyCart,
        totalItems,
  } = useCart();

    return (
        <div>
            <div >
                <div className="text-center mt-5">
                    <h1>Cart</h1>
                    <p>This is the Cart Page.</p>
                </div>

                <div className="row no-gutters justify-content-center">
                    <div className="col-sm-9 p-3">
                        {
                            totalItems > 0 ?
                            <CartProducts/> :
                            <div className="p-3 text-center text-muted">
                                Your cart is empty
                            </div>
                        }
                    </div>
                    {
                        totalItems > 0 &&
                        <div className="col-sm-3 p-3">
                            <div className="card card-body">
                                <p className="mb-1">Total Items</p>
                                <h4 className=" mb-3 txt-right">{totalUniqueItems}</h4>
                                <p className="mb-1">Total Payment</p>
                                <h3 className="m-0 txt-right">{formatNumber(cartTotal)}</h3>
                                <hr className="my-4"/>
                                <div className="text-center">
                                    <button type="button" className="btn btn-primary mb-2">CHECKOUT</button>
                                    <button type="button" className="btn btn-outlineprimary btn-sm" onClick={() => emptyCart()}>CLEAR</button>
                                </div>

                            </div>
                        </div>
                    }

                </div>
            </div>
        </div>
     );
}

export default Cart;