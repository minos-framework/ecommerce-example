import React, {useEffect, useState} from 'react';
import OrderService from "../../services/order";

function Orders() {
    const [orders, setOrders] = useState([]);

    function GetOrders() {
        OrderService.get_by_user("").then(
            (response) => {
                setOrders(response.data)
            },
            error => {
                console.log(error)
            }
        );
    }

    useEffect(() => {
        GetOrders()
    }, [orders]);

    return (
        <div>
            <div className="text-center mt-5">
                    <h1>Orders</h1>
                </div>
            <table className="table table-hover">
                <tbody>
                <tr>
                    <th>Status</th>
                    <th>ID</th>
                    <th>Ticket ID</th>
                    <th>Payment</th>
                    <th>Total</th>
                    <th>Creation Date</th>
                </tr>
                {orders.map((item) => (
                    <tr key={item.uuid}>
                        <td>{item.status}</td>
                        <td>{item.uuid.slice(3, -25)}...</td>
                        <td>{item.ticket_uuid.slice(3, -25)}...</td>
                        <td>{item.payment_uuid.slice(3, -25)}...</td>
                        <td>{item.total_amount} €</td>
                        <td>{item.created_at}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default Orders;