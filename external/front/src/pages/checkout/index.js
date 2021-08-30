import React, {useState} from 'react';

import Products from './Products';
import {formatNumber} from '../../helpers/utils';
import {useCart} from "react-use-cart";
import PaymentService from '../../services/payment'
import {PaymentInputsWrapper, usePaymentInputs} from 'react-payment-inputs';
import images from 'react-payment-inputs/images';

function Checkout() {
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
        if (cardNumber) {
            PaymentService.create(cardNumber, cartTotal).then(
            response => {
                console.log(response.uuid)
            },
            error => {
                console.log(error)
            })
        }

        console.log(cardNumber)
        console.log(cardExpiryDate)
        console.log(cardCVC)
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
                            <div className="card card-body">
                                <PaymentInputsWrapper {...wrapperProps}>
                                    <svg {...getCardImageProps({images})} />
                                    <input {...getCardNumberProps({onChange: handleCardNumber})} />
                                    <input {...getExpiryDateProps({onChange: handleExpiryDate})} />
                                    <input {...getCVCProps({onChange: handleCVC})} />
                                </PaymentInputsWrapper>

                                <hr className="my-4"/>
                                <div className="text-center">
                                    <button type="button"
                                            className="btn btn-primary mb-2"
                                            onClick={() => Pay()}>PAY {formatNumber(cartTotal)}</button>
                                </div>

                            </div>
                        </div>
                    }

                </div>
            </div>
        </div>
    );
}

export default Checkout;