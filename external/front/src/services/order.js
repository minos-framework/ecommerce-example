import axios from "axios";
import {API_URL} from "../config";


/*
* Payment Micro-service calls.
* */
class OrderService {
    /*
    * Create Cart.
    * */
    create(data) {
        return axios.post(API_URL + "orders", data, {
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            return response.data;
        });
    }

    get_by_user(user) {
        user = "05693c6d-6a41-4bae-a8f5-68b4b15bfd9d"
        return axios.get(`${API_URL}orders/user/${user}`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(response => {
            return response
        });
    }

    get_order(uuid) {
        return axios.get(`${API_URL}orders/${uuid}`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(response => {
            return response
        });
    }
}

export default new OrderService();