import React from 'react';

import CartItem from './CartItem';
import {useCart} from "react-use-cart";

const CartProducts = () => {

    const { items } = useCart();

    return (
        <div>
            <div className="card card-body border-0">

                {
                    items.map(product =>  <CartItem key={product.id} product={product}/>)
                }

            </div>
        </div>

     );
}

export default CartProducts;
