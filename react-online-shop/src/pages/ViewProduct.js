import React from "react"
import Product from "../assets/Product-Foto.png";
import Button from "../components/Button";

function ViewProduct() {
    
    let btnStyle = {
        padding: "1% 7%",
        border: "none",
        color: "#fff",
        background: "#b4b0b0",
        fontWeight: 500,
        fontSize: "1.5rem"
    };

    return (
        <div>
            <div id="view-product-cont"> 
                <div id="product-img-cont">
                    <img src={Product} alt="Person wearing a beige blazer over a white shirt." />
                </div>
                <div id="product-view-info">
                    <h1 id="product-heading">JAСKET KLS</h1>
                    <h3 id="price">€105</h3>
                

                <Button buttonName={"Add to Cart"} buttonStyle={btnStyle} linkTo={"cart"} />
                
                <div id="name-and-description">
                    <h5 id="info">Product Info</h5>
                    <h5 id="description">
                        Jacket made of a loose fit makes the 
                        product a universal element of the 
                        upper layer. Two patch pockets and 
                        one hidden pocket. Branded lining with FABLE 
                        pattern. Shoulder pads of medium rigidity for shaping.
                    </h5>
                </div>
                </div>
            </div>
        </div>

    );
}

export default ViewProduct;