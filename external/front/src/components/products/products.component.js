import React from 'react';
import axios from "axios";

class Products extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            products: null,
            name: null
        }
    }

    componentDidMount() {

    }

    getProducts() {
        axios.get(`http://localhost:8084/products`, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Accept': 'application/json',
            },
        })
            .then(response => {
                console.log(response.data)
            })
            .then(data => {
                this.setState({products: data})
            })
            .catch(error => {

            })
    }
    render() {
        /*
        let participations = []
        if(this.state.participations !== null && this.state.participations.length > 0) {
            let ptc = JSON.parse(this.state.participations)

            for (let i = 0; i < ptc.length; i++) {
                participations.push(<span><Product participant={ptc[i]}/></span>)
            }
        }
        */
        return (
            <span>
                {this.products}
            </span>
        );
    }
}

export default Products;