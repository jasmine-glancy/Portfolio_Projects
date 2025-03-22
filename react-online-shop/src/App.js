import './App.css';
import React from 'react';
import Landing from './pages/Landing';
import ViewProduct from './pages/ViewProduct';
import CartView from './pages/CartView';
import OrderPage from './pages/OrderPage';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import { Provider } from 'react-redux';
import store from './app/store';

function App() {
  return (
    <div>
      <Provider store={store}>
        <Router>
          <NavBar />

          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/view" element={<ViewProduct />}/>
            <Route path="/cart" element={<CartView />} />
            <Route path="/order" element={<OrderPage />}/>
          </Routes>
        </Router>
      </Provider>
    </div>
  );
}

export default App;
