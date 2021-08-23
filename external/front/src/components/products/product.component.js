import React from 'react';

class Participant extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            participant: null,
        }
    }

    componentDidMount() {

    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            product: nextProps.product,
        });
    }

    componentDidUpdate(prevProps, prevState, snapshot) {

    }

    render() {
        let rows = []
        if(this.state.participant !== null) {
            console.log(this.state.participant)
            rows.push(<Role role_id={this.state.participant.role}/>)
        }

        return (
            <div>
                {rows}
            </div>
        );
    }
}

export default Participant;
