import React, {useEffect, useState} from 'react';
import OrderService from "../../services/order";

function OrderDetail() {
    const [order, setOrder] = useState([]);

    function GetOrder() {
        OrderService.get_order("").then(
            (response) => {
                setOrder(response.data)
            },
            error => {
                console.log(error)
            }
        );
    }

    useEffect(() => {
        GetOrder()
    }, [order]);

    return (
        <div>
            <div className="text-center mt-5">
                <h1>Order</h1>
            </div>
        </div>
    );
}

export default OrderDetail;