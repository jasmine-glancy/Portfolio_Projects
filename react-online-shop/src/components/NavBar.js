import React from 'react'
import Logo from '../assets/Logo.png'
import { Link } from 'react-router-dom'

function NavBar () {

    // Returns the navigation bar HTML
    return(
        <nav>
            <div>
                <Link to={"/"}><img src={Logo} alt="Fable" /></Link>
            </div>
            <div id="page-links">
                <Link to={"/"}><p>COLLECTIONS</p></Link>
                <Link to={"/cart"}><p>CART</p></Link>
                <Link to={"/"}><p>SALE</p></Link>
            </div>
            <div id="view-cart">
                <Link to={"/order"}><p>ORDERS</p></Link>
            </div>
        </nav>
    )

}


export default NavBar;