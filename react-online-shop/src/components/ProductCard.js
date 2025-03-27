import React from "react"
import { Link } from "react-router-dom"
import { useNavigate } from "react-router-dom"

function ProductCard ({ProductImg, ProductName, ProductPrice, ProductDesc, ProductID}) {

    const navigate = useNavigate()

    const navAndStore = () => {
        const productID = ProductID

        // Holds item in the local storage
        localStorage.setItem("productID", productID)

        // Navigate the user to the view page
        navigate('/view')

    }

    return(
        <div id="product-card">
            <div id="product-img">
                <img src={ProductImg}/>
            </div>
            <div>
                <h3 onClick={navAndStore} id="product-name">{ProductName}</h3>
                <h3 id="product-price">€{ProductPrice}</h3>
            </div>
        </div>
    );
}

export default ProductCard;