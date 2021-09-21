import React, {useEffect, useState} from 'react';
import OrderService from "../../services/order";
import {useHistory} from "react-router-dom";

function Orders() {
    const [orders, setOrders] = useState([]);
    const history = useHistory();

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

    function handleRowClick(uuid) {
        history.push(`/order/${uuid}`);
    }

    useEffect(() => {
        GetOrders()
    }, [orders]);

    return (
        <div>
            <div className="text-center mt-5">
                <h1>Order</h1>
            </div>
            <table className="table table-hover">
                <tbody>
                <tr>
                    <th>Status</th>
                    <th>ID</th>
                    <th>Ticket ID</th>
                    <th>Payment</th>
                    <th>Total</th>
                    <th>Date</th>
                </tr>
                {orders.map((item) => (
                    <tr key={item.uuid} onClick={() => handleRowClick(item.uuid)}>
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