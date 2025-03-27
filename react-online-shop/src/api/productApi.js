import axios from "axios";

const API_URL = "https://reactecomgdi.onrender.com/api"

// Async allows us to use "await", which takes time for us to retrieve info from the back end
export const getProducts = async () => {
    let result = await axios.get(`${API_URL}/products`)
    return result.data
}

export const getProductsById = async (id) => {
    let result = await axios.get(`${API_URL}/products/${id}`)
    return result.data
}