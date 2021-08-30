import React from 'react';

import Item from './Item';
import {useCart} from "react-use-cart";

const Products = () => {

    const { items } = useCart();

    return (
        <div>
            <div className="card card-body border-0">

                {
                    items.map(product =>  <Item key={product.id} product={product}/>)
                }

            </div>
        </div>

     );
}

export default Products;
