import axios from "axios";

const API_URL = "http://localhost:5566/";

class AuthService {
    login(username, password) {
        return axios
            .post(API_URL + "login", {
                "username": username,
                "password": password
            })
            .then(response => {
                if (response.data.accessToken) {
                    localStorage.setItem("user", JSON.stringify(response.data));
                }

                return response.data;
            });
    }

    logout() {
        localStorage.removeItem("user");
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
                localStorage.setItem("user_uuid", response.data.username);
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
            console.log(response.data)

            return response.data;
        });
    }

    getCurrentUser() {
        return JSON.parse(localStorage.getItem('user'));
    }
}

export default new AuthService();