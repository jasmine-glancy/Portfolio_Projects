import React from "react"

function CartItem ({item}) {
    console.log(item, 'item')
    return(
        <div>
            <div id="cart-item-details">
                <div id="cart-item-image">
                    <img src={item.product.image} alt="A person wearing a light beige suit jacket and trousers with a white top, standing in profile against a white background."/>
                </div>
                <div id="cart-item-info">
                    <h2 id="item-name">{item.product.name}</h2>

                    <h4 id="collection-name">item: {item.product.name}</h4>
                    <h4 id="article-name">Article: {item.product._id}</h4>
                    
                    <div id="cart-item-details">
                        <h3 id="item-size">Size: S</h3>

                        <h3 id="item-color">Color: Black</h3>

                        <h3 id="item-quantity">
                            Quantity: <span>-</span> {item.product.quantity} <span>+</span>
                        </h3>
                    </div>
                    <div id="price-and-control">
                        <h3 id="item-price">Price: €{item.product.amount}</h3>

                        <h3 id="delete-item">Delete</h3>
                    </div>
                </div>
            </div>
        </div>
    );                    
}

export default CartItem;