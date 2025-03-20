import React from "react"
import Card from "../assets/Fable-Card.png"
import Table from "../components/Table";

function OrderPage () {
    return(
        <div>
            <div id="order-page-container">
                <div id="order-info">
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
                
                    <Table />
                </div>
            </div>
        </div>
    );
}

export default OrderPage;