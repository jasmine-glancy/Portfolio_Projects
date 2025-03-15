import NavBar from "../components/NavBar"
import Product1 from "../assets/Foto.png"
import Product2 from "../assets/Foto2.png"
import Product3 from "../assets/Foto3.png"
import ProductCard from "../components/ProductCard"
import ViewProduct from "./ViewProduct"

function Landing () {
    return(
        <div>
            <ViewProduct />

            <div id="heading">
                <h1>FABLE OF KLASSIK</h1>
                <h4>
                    Jackets KLS
                </h4>
            </div>

            <div id="products">
                <ProductCard ProductImg={Product1} ProductName={"Jacket KLS Beige"} ProductPrice={105}/>
                <ProductCard ProductImg={Product2} ProductName={"Jacket KLS Black"} ProductPrice={105}/>
                <ProductCard ProductImg={Product3} ProductName={"Jacket KLS Graphite"} ProductPrice={105}/>
            </div>

        </div>
    )
}

export default Landing;