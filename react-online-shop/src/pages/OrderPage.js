import NavBar from "../components/NavBar"
import Card from "../assets/Fable-Card.png"

function OrderPage () {
    return(
        <div>
            <NavBar />
            <div id="order-page-container">
                <h2 id="customer-greeting">Hello, Darya!</h2>
            
                <div id="card-container">
                    <img src={Card} alt="Storefront window with the word 'FABLE' above, displaying winter clothing on racks and a small table with hats." />

                    <div id="card-info">
                        <h3 id="card-type">Bonus Card</h3>
                        <h3 id="points-earned">250 points</h3>
                    </div>

                    <div id="card-benefit-info">
                        <h5 id="card-benefits">Cashback</h5>
                        <h5 id="benefit-percentage">5%</h5>
                    </div>
                </div>
                
                <h2>Recent Orders</h2>
            
                <table>
                    <thead>
                    <td><tr>Number</tr></td>
                    <td><tr>Order</tr></td>
                    <td><tr>Date</tr></td>
                    <td><tr>Summary</tr></td>
                    </thead>
                </table>
            </div>
        </div>
    );
}

export default OrderPage;