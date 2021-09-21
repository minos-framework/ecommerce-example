import React, {useEffect, useState} from 'react';
import TicketService from "../../services/ticket";
import {formatNumber} from "../../helpers/utils";

function TicketDetail(params) {
    const [ticket, setTicket] = useState(undefined);


    function GetTicket() {
        TicketService.get(params.uuid).then(
            (response) => {
                setTicket(response.data)
            },
            error => {
                console.log(error)
            }
        );
    }

    useEffect(() => {
        GetTicket()
    }, [ticket]);


    if (ticket === undefined) {
        return (
            <div>
                <div>Loading ...</div>
            </div>
        );
    } else {
        return (
            <div className="mt-4">
                <span className="badge rounded-pill bg-info">Order details</span>
                <ul className="list-group mt-4">
                    {ticket.entries.map((item) => (
                        <li className="list-group-item d-flex justify-content-between align-items-center">
                            <h5><a href={"/product/" + item.product_uuid}>{item.title}</a></h5>
                            <h5><span className="badge bg-primary rounded-pill">x{item.quantity}</span></h5>
                            <h5>{formatNumber(item.quantity * item.unit_price)}</h5>
                        </li>
                    ))}

                    <li className="list-group-item d-flex justify-content-between align-items-center bg-light">
                        Subtotal
                        <span>{formatNumber(params.total_amount)}</span>
                    </li>

                    <li className="list-group-item d-flex justify-content-between align-items-center bg-light">
                        Discount
                        <span>{formatNumber(0)}</span>
                    </li>

                    <li className="list-group-item d-flex justify-content-between align-items-center bg-light">
                        Shipping
                        <span>{formatNumber(0)}</span>
                    </li>
                    <li className="list-group-item d-flex justify-content-between align-items-center bg-light">
                        <h4>Total</h4>
                        <h4 className="text-success">{formatNumber(params.total_amount)}</h4>
                    </li>
                </ul>
            </div>
        );
    }


}

export default TicketDetail;