import React from "react"

function CartItem ({ProductImg, ProductName,
                    ProductCollection, ProductArticle,
                    ProductSize, ProductColor,
                    ProductQuantity, ProductPrice}) {
    return(
        <div>
            <div id="cart-item-details">
                <div id="cart-item-image">
                    <img src={ProductImg} alt="A person wearing a light beige suit jacket and trousers with a white top, standing in profile against a white background."/>
                </div>
                <div id="cart-item-info">
                    <h2 id="item-name">{ProductName}</h2>

                    <h4 id="collection-name">Collection: {ProductCollection}</h4>
                    <h4 id="article-name">Article: {ProductArticle}</h4>
                    
                    <div id="cart-item-details">
                        <h3 id="item-size">Size: {ProductSize}</h3>

                        <h3 id="item-color">Color: {ProductColor}</h3>

                        <h3 id="item-quantity">
                            Quantity: <span>-</span> {ProductQuantity} <span>+</span>
                        </h3>
                    </div>
                    <div id="price-and-control">
                        <h3 id="item-price">Price: {ProductPrice}</h3>

                        <h3 id="delete-item">Delete</h3>
                    </div>
                </div>
            </div>
        </div>
    );                    
}

export default CartItem;