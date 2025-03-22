import React from "react"
import Button from "./Button";
import Input from "./Input"

function SummaryCont () {
    let promoCodeInputStyle = {
        width: "150%",
        padding: "12% 20%",
    };

    
    let btnStyle3 = {
        padding: "2% 7%",
        border: "none",
        width: "30%",
        color: "#fff",
        background: "#000",
        fontWeight: "100",
        fontSize: "1.5rem",
        cursor: "pointer"
    };

    return(
        <div id="summary-cont">
            <div id="first">
                <div>
                    <p>Summary:</p>
                    <p>€340</p>
                </div>
                <div>
                    <p>Delivery:</p>
                    <p>€0</p>
                </div>
                <div>
                    <p>Promocode:</p>
                    <p>€0</p>
                </div>
            </div>

            <div className="second">
                <h2>Total:</h2>
                <h2>€340</h2>
            </div>

            <div className="second">
                <Input inputStyle={promoCodeInputStyle} placeholder={"Enter Promocode"} />
                <Button buttonName={"Apply"} buttonStyle={btnStyle3} />
            </div>
        </div>
    );
}

export default SummaryCont;