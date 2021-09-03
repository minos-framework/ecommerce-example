import React, {useCallback, useState} from "react";
import {Switch, Route, Link} from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootswatch/dist/lux/bootstrap.css'

import './App.scss';

import AuthService from "./services/auth.service";

import Login from "./components/auth/login.component";
import Register from "./components/auth/register.component";
import Home from "./components/home.component";
import Profile from "./components/auth/profile.component";
import BoardUser from "./components/board-user.component";
import BoardAdmin from "./components/board-admin.component";

import Products from "./components/products/products-list";
import ProductDetail from "./components/products/product-detail";
import {useCart} from "react-use-cart";
import {CartIcon} from "./components/icons";
import Cart from "./pages/cart";
import Checkout from "./pages/checkout";
import Orders from "./pages/orders";

function App() {
    const user = AuthService.getCurrentUser();
    const logOut = useCallback(
        () => {
            AuthService.logout();
        },
        [],
    );

    let roles = []

    if (user) {
        roles = user.roles
    }

    const [showModeratorBoard, updateShowModeratorBoard] = useState(roles.includes("ROLE_USER"));
    const [showAdminBoard, updateShowAdminBoard] = useState(roles.includes("ROLE_ADMIN"));
    const [currentUser, updateCurrentUser] = useState(user)

    const {totalUniqueItems} = useCart()

    return (
        <div>
            <nav className="header navbar navbar-expand navbar-dark bg-dark">
                <Link to={"/"} className="navbar-brand">
                    Minos Demo
                </Link>
                <div className="navbar-nav mr-auto">
                    <li className="nav-item">
                        <Link to={"/home"} className="nav-link">
                            Home
                        </Link>
                    </li>

                    <li className="nav-item">
                        <Link to={"/products"} className="nav-link">
                            Products
                        </Link>
                    </li>

                    {showAdminBoard && (
                        <li className="nav-item">
                            <Link to={"/admin"} className="nav-link">
                                Admin Board
                            </Link>
                        </li>
                    )}

                    {currentUser && (
                        <li className="nav-item">
                            <Link to={"/orders"} className="nav-link">
                                My Orders
                            </Link>
                        </li>
                    )}
                </div>

                {currentUser ? (
                    <div className="navbar-nav ml-auto">
                        <li className="nav-item cart-link mr-3">
                            <Link to='/cart'>
                                <CartIcon/>
                                <span className="badge badge-primary align-top">{totalUniqueItems}</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to={"/profile"} className="nav-link">
                                {currentUser.username}
                            </Link>
                        </li>
                        <li className="nav-item">
                            <a href="/login" className="nav-link" onClick={() => logOut()}>
                                LogOut
                            </a>
                        </li>
                    </div>
                ) : (
                    <div className="navbar-nav ml-auto">
                        <li className="nav-item cart-link mr-3">
                            <Link to='/cart'>
                                <CartIcon/>
                                <span className="badge badge-primary align-top">{totalUniqueItems}</span>
                            </Link>
                        </li>

                        <li className="nav-item">
                            <Link to={"/login"} className="nav-link">
                                Login
                            </Link>
                        </li>

                        <li className="nav-item">
                            <Link to={"/register"} className="nav-link">
                                Sign Up
                            </Link>
                        </li>
                    </div>
                )}

            </nav>

            <div className="container-fluid">
                <Switch>
                    <Route exact path={["/", "/home"]} component={Home}/>
                    <Route exact path="/login" component={Login}/>
                    <Route exact path="/register" component={Register}/>
                    <Route exact path="/profile" component={Profile}/>
                    <Route path="/product/:id" component={ProductDetail}/>
                    <Route exact path="/products" component={Products}/>
                    <Route path="/user" component={BoardUser}/>
                    <Route path="/admin" component={BoardAdmin}/>
                    <Route path="/cart" component={Cart}/>
                    <Route path="/checkout" component={Checkout}/>
                    <Route path="/orders" component={Orders}/>
                </Switch>
            </div>

        </div>
    )
}

export default App;
