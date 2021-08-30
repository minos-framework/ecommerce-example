import axios from "axios";
import {API_URL} from "../config";


/*
* Payment Micro-service calls.
* */
class PaymentService {
    /*
    * Create Cart.
    * */
    create(credit_number, amount) {
        return axios.post(API_URL + "payments", {
            credit_number: credit_number,
            amount: amount
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            return response.data;
        });
    }
}

export default new PaymentService();