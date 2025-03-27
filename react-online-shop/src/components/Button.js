import React from "react"
import { Link } from "react-router-dom";

function Button ({buttonName, buttonStyle, linkTo, func}) {
    // If there is a link in linkTo, take the user to it. Otherwise, don't do anything
    if (linkTo) {
        return (
        <Link to={linkTo}>
            <button onClick={func} style={buttonStyle}>{buttonName}</button>
        </Link>
        );
    } else {
        return (
            <Link to={linkTo}>
            <button onClick={func} style={buttonStyle}>{buttonName}</button>
        </Link>
        )

    }
}

export default Button;