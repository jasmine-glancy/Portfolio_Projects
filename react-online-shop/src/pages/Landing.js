import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import React from "react";
import ProductCard from "../components/ProductCard";
import { fetchProductsAsync } from "../features/productSlice";

function Landing () {

    const dispatch = useDispatch()

    const {items: products, status, error} = useSelector((state) => { return state.products; });

    const [loading, setLoading] = useState(status); 
    
    useEffect(() => {
        dispatch(fetchProductsAsync());
    }, [dispatch]);

    if (status === "loading") return <div>loading</div>;

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
                {/* products?.map only maps the items if they are found */}
                {products.length > 0 ? products.map((item, index) => {
                    return (
                        <ProductCard
                        ProductImg={item.image}
                        ProductName={item.name}
                        ProductPrice={item.amount}
                        ProductDesc={item.description}
                        ProductId={item.id}

                        key={index}
                        />
                    );
                    // If the condition is not met, return no data
                    }): 'no data'
                }       
                         
            </div>
        </div>
    );
}

export default Landing;