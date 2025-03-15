

function ProductCard ({ProductImg, ProductName, ProductPrice}) {
    return(
        <div id="product-card">
            <div id="product-img">
                <img src={ProductImg}/>
            </div>
            <div>
                <h3 id="product-name">{ProductName}</h3>
                <h3 id="product-price">€{ProductPrice}</h3>
            </div>
        </div>
    );
}

export default ProductCard;