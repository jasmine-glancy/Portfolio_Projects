import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import React from "react";
import ProductCard from "../components/ProductCard";
import fetchProductAsync from "../features/productSlice";

function Landing () {

    const dispatch = useDispatch()

    const {items:products, status, error} = useSelector((state)=> state.products)

    useEffect(() => {
        dispatch(fetchProductAsync)
    })

    console.log(products, status, error)

    return(
        <div>
            <div id="heading">
                <h1>FABLE OF KLASSIK</h1>
                <h4>
                    Jackets KLS
                </h4>
            </div>

            <div id="products">
                {products.map((item, index) => {
                    return (
                        <ProductCard
                        ProductImg={item.img}
                        ProductName={item.name}
                        ProductPrice={item.price}
                        />
                    );
                    })}                
            </div>

        </div>
    )
}

export default Landing;