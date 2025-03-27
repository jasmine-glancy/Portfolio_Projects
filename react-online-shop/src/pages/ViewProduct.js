import React, { useEffect } from "react"
import Button from "../components/Button";
import { addToCartAsync } from "../features/cartSlice";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import { fetchProductsByIdAsync } from "../features/productSlice";

function ViewProduct() {

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const {items: products, status, error} = useSelector((state)=> { return state.products; });

    
    const id = localStorage.getItem('productId')


    useEffect(()=>{
        if (id) {
            dispatch(fetchProductsByIdAsync(id))
        }
    }, [dispatch]);

    const addToCartFunc = () => {
        dispatch(addToCartAsync({ userId: 4, productId: id, quantity: 1 }))
        navigate("/cart")
    }

    
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
                    <img src={products?.image} />
                </div>
                <div id="product-view-info">
                    <h1 id="product-heading">{products?.name} </h1>
                    <h3 id="price">€{products?.amount} </h3>
                

                <Button func={addToCartFunc} buttonName={"Add to Cart"} buttonStyle={btnStyle} linkTo={"cart"} />
                
                <div id="name-and-description">
                    <h5 id="info">Product Info</h5>
                    <h5 id="description">
                        {products?.description}
                    </h5>
                </div>
                </div>
            </div>
        </div>

    );
}

export default ViewProduct;