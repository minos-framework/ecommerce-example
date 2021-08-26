import axios from "axios";

const API_URL = "http://localhost:5566/";

class AuthService {
    login(username, password) {
        const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64')
        return axios
            .get(API_URL + "login", {
                headers: {
                    'Authorization': `Basic ${token}`
                }
            })
            .then(response => {

                if (response.data.length > 100) {
                    localStorage.setItem("username", username);
                    localStorage.setItem("user_token", response.data);
                }

                return response.data;
            });
    }

    logout() {
        localStorage.removeItem("user_uuid");
        localStorage.removeItem("username");
        localStorage.removeItem("user_token");
    }

    register(username, password, street, number) {
        return axios.post(API_URL + "users", {
            username: username,
            password: password,
            status: "created",
            address: {
                street: "Green Dolphin Street",
                street_no: "42"
            }
        }, {
            headers: {
                // Overwrite Axios's automatically set Content-Type
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.data.uuid) {
                localStorage.setItem("user_uuid", response.data.uuid);
                localStorage.setItem("username", response.data.username);
            }

            return this.createLogin(username, password);
        });
    }

    createLogin(username, password) {
        return axios.post(API_URL + "login", {
            username: username,
            password: password,
        }, {
            headers: {
                // Overwrite Axios's automatically set Content-Type
                'Content-Type': 'application/json'
            }
        }).then(response => {
            return response.data;
        });
    }

    getCurrentUser() {
        if (localStorage.getItem('user_token')) {
            return {
                uuid: localStorage.getItem('user_uuid'),
                username: localStorage.getItem('username'),
                token: localStorage.getItem('user_token'),
                roles: ['ROLE_USER']
            }
        }
        return undefined
    }

}

export default new AuthService();