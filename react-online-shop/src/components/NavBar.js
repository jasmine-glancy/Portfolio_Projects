import Logo from '../assets/Logo.png'

function NavBar () {

    // Returns the navigation bar HTML
    return(
        <nav>
            <div>
                <img src={Logo} alt="Fable" />
            </div>
            <div>
                <p>Collections</p>
                <p>Customizer</p>
                <p>Sale</p>
            </div>
            <div>
                <p>Items</p>
            </div>
        </nav>
    )

}


export default NavBar