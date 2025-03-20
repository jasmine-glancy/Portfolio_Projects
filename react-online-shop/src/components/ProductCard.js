import React from "react"
import { Link } from "react-router-dom"

function ProductCard ({ProductImg, ProductName, ProductPrice}) {
    return(
        <div id="product-card">
            <div id="product-img">
                <img src={ProductImg}/>
            </div>
            <div>
                <Link to={"/view"}><h3 id="product-name">{ProductName}</h3></Link>
                <h3 id="product-price">€{ProductPrice}</h3>
            </div>
        </div>
    );
}

export default ProductCard;