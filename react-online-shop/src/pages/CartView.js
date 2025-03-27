import React from "react"
import { useEffect, useState } from "react";
import Button from "../components/Button";
import CartItem from "../components/CartItem";
import Input from "../components/Input";
import SummaryCont from "../components/SummaryCont";
import { useSelector, useDispatch } from "react-redux";

import { fetchCartAsync } from "../features/cartSlice";

function CartView () {

    const dispatch = useDispatch();
    
    const [userdata, setUserData] = useState({});

    const {
        items: cart, 
        status, 
        error,
    } = useSelector((state)=> { 
        return state.cart; 
    });
    
    const [loading, setLoading] = useState(status);

    useEffect(() => {
        dispatch(fetchCartAsync());
    }, [dispatch]);

    const handleCity = (e) => {
        // Add info to user data
        setUserData({...userdata, city: e.target.value})
    }

    const handleAddress = (e) => {
        setUserData({...userdata, address: e.target.value})
    }

    const handleName = (e) => {
        setUserData({...userdata, name: e.target.value})
    }

    const handlePhone = (e) => {
        setUserData({...userdata, phone: e.target.value})
    }

    const handleEmail = (e) => {
        setUserData({...userdata, email: e.target.value})
        console.log(userdata)
    }

    if (status === "loading") return <div>loading</div>;
    
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
                            <Input func={handleCity} labelName={"City"} placeholder={"Enter City"} labelStyle={labelStyle} inputStyle={cityInputStyle} />
                            <Input func={handleAddress} labelName={"Address"} placeholder={"Enter Address"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                            <Input func={handleName} labelName={"Recipient Details"} placeholder={"Enter Recipient Details"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                            <Input func={handlePhone} labelName={"Phone"} placeholder={"Enter Phone"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                            <Input  func={handleEmail} labelName={"Email"} placeholder={"Enter Email"}  labelStyle={labelStyle} inputStyle={inputStyle} />

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
                                {
                                    cart?.items?.length > 0 
                                    ? cart.items.map((item, index) => {
                                        return <CartItem item={item}/>
                                    }) : "no data"
                                }
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