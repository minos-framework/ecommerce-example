import React, {useState} from 'react';

import Products from './Products';
import {formatNumber} from '../../helpers/utils';
import {useCart} from "react-use-cart";
import PaymentService from '../../services/order'
import {PaymentInputsWrapper, usePaymentInputs} from 'react-payment-inputs';
import images from 'react-payment-inputs/images';

function Checkout(props) {
    const [shipmentName, setShipmentName] = useState(undefined);
    const [shipmentLastName, setShipmentLastName] = useState(undefined);
    const [shipmentEmail, setShipmentEmail] = useState(undefined);
    const [shipmentAddress, setShipmentAddress] = useState(undefined);
    const [shipmentCountry, setShipmentCountry] = useState(undefined);
    const [shipmentCity, setShipmentCity] = useState(undefined);
    const [shipmentProvince, setShipmentProvince] = useState(undefined);
    const [shipmentZip, setShipmentZip] = useState(undefined);
    const [cardHolder, setCardHolder] = useState(undefined);
    const [cardNumber, setCardNumber] = useState(undefined);
    const [cardExpiryDate, setCardExpiryDate] = useState(undefined);
    const [cardCVC, setCardCVC] = useState(undefined);

    const {
        wrapperProps,
        getCardImageProps,
        getCardNumberProps,
        getExpiryDateProps,
        getCVCProps
    } = usePaymentInputs();

    const {
        cartTotal,
        totalItems,
    } = useCart();

    function Pay() {

        let data = {
            cart: "5b1a5558-0006-43cc-8476-85fe91a12e86",
            customer: "05693c6d-6a41-4bae-a8f5-68b4b15bfd9d",
            payment_detail: {
                card_holder: cardHolder,
                card_number: cardNumber,
                card_expire: cardExpiryDate,
                card_cvc: cardCVC
            },
            shipment_detail: {
                name: shipmentName,
                last_name: shipmentLastName,
                email: shipmentEmail,
                address: shipmentAddress,
                country: shipmentCountry,
                city: shipmentCity,
                province: shipmentProvince,
                zip: shipmentZip,
            }
        }

        if (cardNumber) {
            PaymentService.create(data).then(
            response => {
                props.history.push('/orders')
            },
            error => {
                console.log(error)
            })
        }
    }

    function handleCardNumber(event) {
        let num = event.target.value
        const card_number = num.replace(/ /g, '')
        setCardNumber(card_number)
    }

    function handleExpiryDate(event) {
        setCardExpiryDate(event.target.value)
    }

    function handleCVC(event) {
        setCardCVC(event.target.value)
    }

    function handleCardHolder(event) {
        setCardHolder(event.target.value)
    }

    function handleShipmentName(event) {
        setShipmentName(event.target.value)
    }

    function handleShipmentLastName(event) {
        setShipmentLastName(event.target.value)
    }

    function handleShipmentEmail(event) {
        setShipmentEmail(event.target.value)
    }

    function handleShipmentCountry(event) {
        setShipmentCountry(event.target.value)
    }

    function handleShipmentAddress(event) {
        setShipmentAddress(event.target.value)
    }

    function handleShipmentCity(event) {
        setShipmentCity(event.target.value)
    }

    function handleShipmentProvince(event) {
        setShipmentProvince(event.target.value)
    }

    function handleShipmentZip(event) {
        setShipmentZip(event.target.value)
    }

    return (
        <div>
            <div>
                <div className="text-center mt-5">
                    <h1>Checkout</h1>
                    <p>This is the Checkout Page.</p>
                </div>

                <div className="row no-gutters justify-content-center">
                    <div className="col-sm-6 p-3 border-right border-dark">
                        <Products/>
                        <hr className="my-4"/>
                        <div className="row no-gutters py-2">
                            <div className="col-sm-2 p-2">

                            </div>
                            <div className="col-sm-3 p-2">
                                <p className="mb-1">Total Payment</p>
                                <h3 className="m-0 txt-right">{formatNumber(cartTotal)}</h3>

                            </div>
                            <div className="col-sm-2 p-2 text-center ">
                                <p className="mb-1">Total Items</p>
                                <h4 className=" mb-3 txt-right">{totalItems}</h4>
                            </div>
                        </div>
                    </div>
                    {
                        totalItems > 0 &&
                        <div className="col-sm-6 p-3">
                            <h3>Shipment info</h3>
                            <div className="card card-body mb-3">
                                <div className="form-row">
                                    <div className="form-group col-md-6">
                                        <label htmlFor="inputEmail4">Name</label>
                                        <input type="email" className="form-control" id="inputEmail4"
                                               onChange={(e) => {handleShipmentName(e)}}
                                               placeholder="Name"/>
                                    </div>
                                    <div className="form-group col-md-6">
                                        <label htmlFor="inputPassword4">Last name</label>
                                        <input type="text" className="form-control" id="inputPassword4"
                                               onChange={(e) => {handleShipmentLastName(e)}}
                                               placeholder="Last name"/>
                                    </div>
                                </div>
                                <div className="form-row">
                                    <div className="form-group col-md-6">
                                        <label htmlFor="inputEmail4">Email</label>
                                        <input type="email" className="form-control" id="inputEmail4"
                                               onChange={(e) => {handleShipmentEmail(e)}}
                                               placeholder="Email"/>
                                    </div>
                                    <div className="form-group col-md-6">
                                        <label htmlFor="inputPassword4">Country</label>
                                        <select id="inputState" className="form-control"
                                                onChange={(e) => {handleShipmentCountry(e)}}
                                        >
                                            <option selected>Choose...</option>
                                            <option value="Spain">Spain</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="inputAddress">Address</label>
                                    <input type="text" className="form-control" id="inputAddress"
                                           onChange={(e) => {handleShipmentAddress(e)}}
                                           placeholder="1234 Main St"/>
                                </div>
                                <div className="form-row">
                                    <div className="form-group col-md-6">
                                        <label htmlFor="inputCity">City</label>
                                        <input type="text" className="form-control" id="inputCity"
                                               onChange={(e) => {handleShipmentCity(e)}}
                                        />
                                    </div>
                                    <div className="form-group col-md-4">
                                        <label htmlFor="inputState">Province</label>
                                        <select id="inputState" className="form-control"
                                                onChange={(e) => {handleShipmentProvince(e)}}
                                        >
                                            <option selected>Choose...</option>
                                            <option value="Madrid">Madrid</option>
                                        </select>
                                    </div>
                                    <div className="form-group col-md-2">
                                        <label htmlFor="inputZip">Zip</label>
                                        <input type="text" className="form-control" id="inputZip"
                                               onChange={(e) => {handleShipmentZip(e)}}
                                        />
                                    </div>
                                </div>
                            </div>
                            <h3>Credit card info</h3>
                            <div className="card card-body">
                                <div className="form-group">
                                    <label htmlFor="exampleInputEmail1">Card Holder</label>
                                    <input type="email" className="form-control" id="exampleInputEmail1"
                                           onChange={(e) => {handleCardHolder(e)}}
                                           aria-describedby="emailHelp" placeholder="Name and surname"/>
                                </div>
                                <PaymentInputsWrapper {...wrapperProps}>
                                    <svg {...getCardImageProps({images})} />
                                    <input {...getCardNumberProps({onChange: handleCardNumber})} />
                                    <input {...getExpiryDateProps({onChange: handleExpiryDate})} />
                                    <input {...getCVCProps({onChange: handleCVC})} />
                                </PaymentInputsWrapper>
                            </div>
                            <div className="text-center mt-3">
                                    <button type="button"
                                            className="btn btn-primary mb-2"
                                            onClick={() => Pay()}>PAY {formatNumber(cartTotal)}</button>
                                </div>
                        </div>
                    }

                </div>
            </div>
        </div>
    );
}

export default Checkout;