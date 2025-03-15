import NavBar from "../components/NavBar"
import Product1 from "../assets/Foto.png"
import Product2 from "../assets/Foto2.png"
import Product3 from "../assets/Foto3.png"
import ProductCard from "../components/ProductCard"
import ViewProduct from "./ViewProduct"
import CartView from "./CartView"

function Landing () {
    return(
        <div>
            <CartView />
            {/* <ViewProduct /> */}
            
            {/* <NavBar />

            <div id="heading">
                <h1>FABLE OF KLASSIK</h1>
                <h4>
                    Jackets KLS
                </h4>
            </div>

            <div id="products">
                <ProductCard ProductImg={Product1} ProductName={"Jacket KLS Beige"} ProductPrice={105} alt="a woman in a long-sleeved beige jacket"/>
                <ProductCard ProductImg={Product2} ProductName={"Jacket KLS Black"} ProductPrice={105} alt="a man in a long-sleeved black jacket and baseball cap"/>
                <ProductCard ProductImg={Product3} ProductName={"Jacket KLS Graphite"} ProductPrice={105} alt="a woman in a long-sleeved gray jacket holding a cactus"/>
            </div> */}

        </div>
    )
}

export default Landing;