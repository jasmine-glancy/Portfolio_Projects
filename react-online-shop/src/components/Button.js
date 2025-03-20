import React from "react"
import { Link } from "react-router-dom";

function Button ({buttonName, buttonStyle, linkTo}) {
    return(
        // If there is a link in linkTo, take the user to it. Otherwise, don't do anything
        <Link to={linkTo ? `/${linkTo}` : '' }>
            <button style={buttonStyle}>{buttonName}</button>
        </Link>
    );
}

export default Button;