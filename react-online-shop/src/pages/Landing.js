import React from "react"
import Product1 from "../assets/Foto.png"
import Product2 from "../assets/Foto2.png"
import Product3 from "../assets/Foto3.png"
import ProductCard from "../components/ProductCard"

function Landing () {
    return(
        <div>
            <div id="heading">
                <h1>FABLE OF KLASSIK</h1>
                <h4>
                    Jackets KLS
                </h4>
            </div>

            <div id="products">
                <ProductCard ProductImg={Product1} ProductName={"Jacket KLS Beige"} ProductPrice={105} alt="Person wearing a beige suit, white shirt, and sunglasses, holding a black crossbody bag, standing against a plain white background."/>
                <ProductCard ProductImg={Product2} ProductName={"Jacket KLS Black"} ProductPrice={105} alt="Person wearing a black blazer and cap, with a white T-shirt, standing against a gray background."/>
                <ProductCard ProductImg={Product3} ProductName={"Jacket KLS Graphite"} ProductPrice={105} alt="Person wearing a gray blazer and blue cap, holding a gray pot with a cactus plant."/>
            </div>

        </div>
    )
}

export default Landing;