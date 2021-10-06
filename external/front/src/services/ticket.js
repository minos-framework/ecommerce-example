import axios from "axios";
import {API_URL} from "../config";


/*
* Ticket Micro-service calls.
* */
class TicketService {
    /*
    * Get Ticket.
    * */
    get(uuid) {
        return axios.get(`${API_URL}tickets/${uuid}`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(response => {
            return response
        });
    }
}

export default new TicketService();