import React, {useEffect, useState} from 'react';
import OrderService from "../../services/order";
import {useParams} from 'react-router-dom';
import TicketDetail from "../../components/tickets/detail"
import {buildDate} from "../../helpers/utils";

function OrderDetail() {
    const [order, setOrder] = useState(undefined);
    const {id} = useParams()

    function GetOrder() {
        OrderService.get_order(id).then(
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


    if (order === undefined) {
        return (
            <div>
                <div>Loading ...</div>
            </div>
        );
    } else {
        return (
            <div>
                <div className="text-center mt-5 mb-4">
                    <h1>Order detail</h1>
                </div>
                <div className="row ml-1">
                    <div className="col-md-8 card card-body">
                        <div className="row bg-light-blue pb-4 pt-4">
                            <div className="col-md-6">
                                <h4>REFERENCE</h4>
                                {order.uuid}
                            </div>
                            <div className="col-md-3">
                                <h4>PLACED</h4>
                                {buildDate(order.created_at).toDateString()}
                            </div>
                            <div className="col-md-2 ml-auto float-right">
                                <h4>STATUS</h4>
                                <span className="badge rounded-pill bg-success">{order.status}</span>
                            </div>
                        </div>

                        <TicketDetail uuid={order.ticket_uuid} total_amount={order.total_amount}/>
                    </div>
                    <div className="col-md-4">
                        <div className="row card card-body m-1">
                            <div className="col-md-12">
                                <h6><span className="badge rounded-pill bg-info">Customer</span></h6>
                                <p>#{order.customer_uuid}</p>
                            </div>
                        </div>
                        <div className="row card card-body m-1 mt-3">
                            <div className="col-md-12">
                                <h6><span className="badge rounded-pill bg-info">PAYMENT</span></h6>
                                <p>#{order.payment_uuid}</p>
                                <p>Card: {order.payment_detail.card_number}</p>
                                <p>Holder: {order.payment_detail.card_holder}</p>
                                <p>Expire: {order.payment_detail.card_expire}</p>
                            </div>
                        </div>
                        <div className="row card card-body m-1 mt-3">
                            <div className="col-md-12">
                                <h6><span className="badge rounded-pill bg-info">SHIPPING ADDRESS</span></h6>
                                <p>Address: {order.shipment_detail.address}</p>
                                <p>City: {order.shipment_detail.city}</p>
                                <p>Province: {order.shipment_detail.province}</p>
                                <p>Zip: {order.shipment_detail.zip}</p>
                                <p>Country: {order.shipment_detail.country}</p>
                                <p>Name: {order.shipment_detail.name} {order.shipment_detail.last_name}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }


}

export default OrderDetail;