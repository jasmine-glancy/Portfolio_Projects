import Logo from '../assets/Logo.png'

function NavBar () {

    // Returns the navigation bar HTML
    return(
        <nav>
            <div>
                <img src={Logo} alt="Fable" />
            </div>
            <div id="page-links">
                <a href="/">COLLECTIONS</a>
                <a href="/">CUSTOMIZER</a>
                <a href="/">SALE</a>
            </div>
            <div id="view-cart">
                <a href="/">ITEMS</a>
            </div>
        </nav>
    )

}


export default NavBar;