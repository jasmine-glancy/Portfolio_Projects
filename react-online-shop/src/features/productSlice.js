import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

import { getProducts } from "../api/productApi";
import { getProductsById } from "../api/productApi";

// createAsyncThunk receives the API

export const fetchProductsAsync = createAsyncThunk(
    'products/getProduct',
    async () => {
        const response = await getProducts()
        return response
    }
)

export const fetchProductsByIdAsync = createAsyncThunk(
    // Defines the route
    'products/getProduct/id',
    async (payload) => {

        const {id} = payload
        const response = await getProductsById()

        return response
    }
)



// Slice holds states 

const productSlice = createSlice({
    name: 'products',
    initialState:{
        items: [],
        status: 'idle',
        error: null
    },
    reducers: {

    },
    extraReducers: (builder) => {

        builder
            .addCase(fetchProductsAsync.pending, (state) =>{
                state.status = 'loading'
            })
            .addCase(fetchProductsAsync.fulfilled, (state, action) =>{
                state.status = 'succeeded'
                state.items = action.payload
            })
            .addCase(fetchProductsAsync.rejected, (state) =>{
                state.status = 'failed'
                state.error = 'something went wrong'
            })
            .addCase(fetchProductsByIdAsync.pending, (state) =>{
                state.status = 'loading'
            })
            .addCase(fetchProductsByIdAsync.fulfilled, (state, action) =>{
                state.status = 'succeeded'
                state.items = action.payload
            })
            .addCase(fetchProductsByIdAsync.rejected, (state) =>{
                state.status = 'failed'
                state.error = 'something went wrong'
            })

    }
})

export default productSlice.reducer;