import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

import { getProducts } from "../api/productApi";

// createAsyncThunk receives the API

export const fetchProductsAsync = createAsyncThunk(
    // Defines the route
    'products/getProduct',
    async () => {
        const response = await getProducts()

        return response
    }
)


// Slice holds states 

const productSlice = createSlice({
    name: 'products',
    initialState: {
        items: [],
        // Idle is the default state
        status: 'idle',
        error: null
    },

    // Reducers hold functions
    reducers: {},

    // Allows us to handle different cases
    extraRedcers: (builder) => {
        builder
            .addCase(fetchProductsAsync.pending, (state) => {
                // If the state status is pending, pass loading as the status
                state.status = 'loading'
            })

            .addCase(fetchProductsAsync.fulfilled, (state) => {
                // If the state status is completed, pass succeeded as the status
                state.status = 'succeeded'
            })

            .addCase(fetchProductsAsync.rejected, (state) => {
                // If the state status encounters an error, pass failed as the status
                state.status = 'failed'
            })
    }
})

export default productSlice.reducer;