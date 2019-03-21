import React from 'react';
import {connect} from "react-redux";
import {Link} from "react-router-dom";

class AccountPage extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="col-md-4 col-md-offset-4">
                <h2>Account Page</h2>
                <p>
                    <Link to="/">Home</Link>
                </p>
            </div>
        );
    }
}

function mapStateToProps(state) {
    const { authentication } = state;
    const { user } = authentication;
    return {
        user
    };
}

const connectedAccountPage = connect(mapStateToProps)(AccountPage);
export { connectedAccountPage as AccountPage };
