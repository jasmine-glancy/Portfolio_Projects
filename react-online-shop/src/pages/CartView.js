import NavBar from "../components/NavBar";
import Product1 from "../assets/Foto.png";
import Button from "../components/Button";
import Input from "../components/Input";

function CartView () {
    
    let inputStyle = {
        width: "100%",
        padding: "3% 10%",
        margin: "3% 0 10%"
    };

    let labelStyle = {

    };

    let btnStyle1 = {

    };

    let btnStyle2 = {

    };

    return (
        <div>
            <NavBar />
            <div id="cart-cont"> 
                <div id="cart-view">
                   <form id="cart-form">
                        <Input labelName={"City"} placeholder={"Enter City"} labelStyle={labelStyle} inputStyle={inputStyle} />
                        <Input labelName={"Address"} placeholder={"Enter Address"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                        <Input labelName={"Recipient Details"} placeholder={"Enter Recipient Details"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                        <Input labelName={"Phone"} placeholder={"Enter Phone"}  labelStyle={labelStyle} inputStyle={inputStyle} />
                        <Input labelName={"Email"} placeholder={"Enter Email"}  labelStyle={labelStyle} inputStyle={inputStyle} />

                        <div>
                            <h2> Payment Method </h2>
                            
                            <Button buttonStyle={btnStyle1} buttonName={"Payment Card"} />
                            <Button buttonStyle={btnStyle2} buttonName={"Cash on Delivery"} />
                        </div>
                   </form>
                </div>

            </div>

        </div>
    );
}

export default CartView;