import NavBar from "../components/NavBar";
import Product1 from "../assets/Foto.png";
import Button from "../components/Button";
import Input from "../components/Input";

function CartView () {
    
    let inputStyle = {
        width: "700px",
        padding: "3% 10%",
        margin: "3% 0%"
    };

    let cityInputStyle = {
        width: "50%",
        padding: "3% 15%",
        margin: "3% 0 10%"
    }

    let labelStyle = {
        padding: "3% 10%",
        marginTop: "15px"
    };
    

    let btnStyle1 = {
        padding: "3% 7%",
        width: "460%",
        color: "#000",
        background: "#fff",
        border: "0.5px solid #000",
        fontWeight: "100",
        fontSize: "1.5rem",
        margin: "5% 3%",
        cursor: "pointer",
    };

    let btnStyle2 = {
        padding: "2% 7%",
        border: "none",
        width: "142%",
        color: "#fff",
        background: "rgb(156, 156, 156)",
        fontWeight: "100",
        fontSize: "1.5rem",
        margin: "2% 3%",
        cursor: "pointer",
    };

    return (
        <div>
            <NavBar />
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
                            <div>product box</div>

                            <table id="line-item-prices">
                                <td>
                                    <tr>Summary:</tr>
                                    <tr>Delivery:</tr>
                                    <tr>Discounts:</tr>
                                </td>
                                <td>
                                    <tr>€340</tr>
                                    <tr>€0</tr>
                                    <tr>€0</tr>
                                </td>
                                <tfoot>
                                    <td>
                                        <tr>Total: </tr>
                                    </td>
                                    <td>
                                        <tr>€340</tr>
                                    </td>
                                </tfoot>
                            </table>
                        </div>
                   </form>
                </div>

            </div>

        </div>
    );
}

export default CartView;