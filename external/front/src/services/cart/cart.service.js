import axios from "axios";
import {API_URL} from "../../config";


/*
* Cart Micro-service calls.
* */
class CartService {
    /*
    * Get Cart.
    * */
    get() {
        const cart_uuid = localStorage.getItem("cart_uuid")
        return axios
            .get(API_URL + "carts/" + cart_uuid)
            .then(response => {
                return response.data;
            });
    }

    /*
    * Create Cart.
    * */
    create() {
        return axios.post(API_URL + "carts", {
            user: 1 //localStorage.getItem("user_uuid"),
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            return response.data;
        });
    }

    /*
    * Add Cart Item.
    * */
    add(uuid, quantity) {
        const cart_uuid = localStorage.getItem("cart_uuid")
        return axios.post(API_URL + "carts/" + cart_uuid + "/items", {
            product_uuid: uuid,
            quantity: quantity
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            return response.data;
        });
    }

    /*
    * Remove Cart Item.
    * */
    remove(uuid) {
        const cart_uuid = localStorage.getItem("cart_uuid")
        return axios.delete(API_URL + "carts/" + cart_uuid + "/items", {
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                product_uuid: uuid,
            }
        }).then(response => {
            return response.data;
        });
    }

    /*
    * Update Cart Item.
    * */
    update(uuid, quantity) {
        const cart_uuid = localStorage.getItem("cart_uuid")
        return axios.put(API_URL + "carts/" + cart_uuid + "/items", {
            product_uuid: uuid,
            quantity: quantity
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            return response.data;
        });
    }

    /*
    * Delete Whole Cart.
    * */
    delete() {
        const cart_uuid = localStorage.getItem("cart_uuid")
        return axios.delete(API_URL + "carts/" + cart_uuid, {
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(response => {
            return response.data;
        });
    }
}

export default new CartService();