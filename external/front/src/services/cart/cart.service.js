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
            user: localStorage.getItem("user_uuid"),
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
    add(product, quantity) {
        const cart_uuid = localStorage.getItem("cart_uuid")
        return axios.post(API_URL + "carts/" + cart_uuid + "/items", {
            product_uuid: product,
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
    remove() {

    }

    /*
    * Update Cart Item.
    * */
    update() {

    }

    /*
    * Delete Whole Cart.
    * */
    delete() {

    }
}

export default new CartService();