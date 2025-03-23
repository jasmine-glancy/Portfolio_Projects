import React from "react"
import ProductA from "../assets/Foto2.png";
import ProductB from "../assets/Cart-Foto.png";
import ProductC from "../assets/Cart-Foto-2.png";
import Button from "../components/Button";
import CartItem from "../components/CartItem";
import Input from "../components/Input";
import SummaryCont from "../components/SummaryCont";

function CartView () {
    
    let inputStyle = {
        width: "700px",
        padding: "3% 10%",
        margin: "3% 0%"
    };

    let cityInputStyle = {
        width: "50%",
        padding: "3% 15%",
        margin: "3% 0"
    }

    let labelStyle = {
        padding: "3% 10%",
        marginTop: "15px"
    };
    

    let btnStyle1 = {
        padding: "3% 7%",
        width: "470%",
        color: "#000",
        background: "#fff",
        border: "0.5px solid #000",
        fontWeight: "100",
        fontSize: "1.5rem",
        margin: "5% 3%",
        cursor: "pointer"
    };

    let btnStyle2 = {
        padding: "2% 7%",
        border: "none",
        width: "120%",
        color: "#fff",
        background: "rgb(156, 156, 156)",
        fontWeight: "100",
        fontSize: "1.5rem",
        margin: "2% 3%",
        cursor: "pointer"
    };

    return (
        <div>
            <div id="cart-cont"> 
                <div id="cart-view">
                   <form id="cart-form-cont">
                        <div id="cart-form-a">
                            <Input labelName={"City"} placeholder={"Enter City"} labelStyle={labelStyle} inputStyle={cityInputStyle} />
                            <Input labelName={"Address"} placeholder={"Enter Address"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                            <Input labelName={"Recipient Details"} placeholder={"Enter Recipient Details"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                            <Input labelName={"Phone"} placeholder={"Enter Phone"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                            <Input labelName={"Email"} placeholder={"Enter Email"}  labelStyle={labelStyle} inputStyle={inputStyle} />

                            <div>
                                <h2> Payment Method </h2>
                                
                                <div id="payment-buttons">
                                    <Button buttonStyle={btnStyle1} buttonName={"Payment Card"} />
                                    <Button buttonStyle={btnStyle1} buttonName={"Cash on Delivery"} />
                                </div>
                            </div>

                            <div id="agree">
                                <input type="checkbox" />
                                <p>I agree to the terms of the offer and the loyalty policy</p>
                            </div>
                            <Button buttonStyle={btnStyle2} buttonName={"Place an Order"} />
                        </div>
                        <div id="cart-form-b">
                            <div>
                                <CartItem ProductImg={ProductA} ProductName={"Jacket KLS"} ProductCollection={"KLASSIK OF FABLE"} ProductArticle={"H0522001"} ProductSize={"M"} ProductColor={"Black"} ProductQuantity={"1"} ProductPrice={"€105"} alt="Person wearing a black blazer and cap, with a white T-shirt, standing against a gray background."/>
                                <CartItem ProductImg={ProductB} ProductName={"Shirt KLS"} ProductCollection={"KLASSIK OF FABLE"} ProductArticle={"M0592001"} ProductSize={"M"} ProductColor={"White"} ProductQuantity={"1"} ProductPrice={"€125"} alt="Person wearing a white shirt with a black peace symbol."/>
                                <CartItem ProductImg={ProductC} ProductName={"Trouser KLS"} ProductCollection={"KLASSIK OF FABLE"} ProductArticle={"A0521005"} ProductSize={"M"} ProductColor={"Black"} ProductQuantity={"1"} ProductPrice={"€110"} alt="Person wearing black pants and black shoes standing against a light gray background."/>
                            </div>

                            <SummaryCont />
                        </div>
                   </form>
                </div>

            </div>

        </div>
    );
}

export default CartView;