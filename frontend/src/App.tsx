import React from "react";
import { Link, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import Products from "./pages/Products";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Checkout from "./pages/Checkout";
import Cart from "./pages/Cart";
import AdminProducts from "./pages/AdminProducts";
import OrderHistory from "./pages/OrderHistory";
import CustomerManagement from "./pages/CustomerManagement";
import AllOrders from "./pages/AllOrders";
import ProductDetail from "./pages/ProductDetail";
import Statistics from "./pages/Statistics";
import { useAuth } from "./context/AuthContext";
import { useCart } from "./context/CartContext";

export default function App() {
	const { user, logout } = useAuth();
	const { getTotalItems } = useCart();
	const nav = useNavigate();
	const location = useLocation();

	const handleLogout = () => {
		logout();
		nav("/");
	};

	return (
		<div>
			<nav className="navbar">
				<div className="container">
					<div className="navbar-content">
						<div className="flex items-center gap-4">
							<Link to="/" className="navbar-brand">
								TechShop
							</Link>
							<ul className="navbar-nav">
								<li>
									<Link to="/" className={location.pathname === "/" ? "active" : ""}>
										Products
									</Link>
								</li>
								{!user?.is_admin && (
									<li>
										<Link to="/cart">
											Cart ({getTotalItems()})
										</Link>
									</li>
								)}
								{user && !user?.is_admin && (
									<li>
										<Link to="/orders" className={location.pathname === "/orders" ? "active" : ""}>
											My Orders
										</Link>
									</li>
								)}
								{user?.is_admin && (
									<>
										<li>
											<Link to="/admin/products" className={location.pathname === "/admin/products" ? "active" : ""}>
												Manage Products
											</Link>
										</li>
										<li>
											<Link to="/admin/orders" className={location.pathname === "/admin/orders" ? "active" : ""}>
												All Orders
											</Link>
										</li>
										<li>
											<Link to="/admin/customers" className={location.pathname === "/admin/customers" ? "active" : ""}>
												Customers
											</Link>
										</li>
										<li>
											<Link to="/admin/statistics" className={location.pathname === "/admin/statistics" ? "active" : ""}>
												📊 Statistics
											</Link>
										</li>
									</>
								)}
							</ul>
						</div>
						<div className="navbar-user">
							{user ? (
								<div className="flex items-center gap-4">
									<div className="flex items-center gap-2">
										<span className="text-sm text-muted">Welcome,</span>
										<span className="text-sm font-medium">{user.username}</span>
										{user.is_admin && <span className="badge badge-primary">Admin</span>}
									</div>
									<button onClick={handleLogout} className="btn btn-outline btn-sm">
										Logout
									</button>
								</div>
							) : (
								<div className="flex items-center gap-2">
									<Link to="/login" className="btn btn-outline btn-sm">
										Login
									</Link>
									<Link to="/register" className="btn btn-primary btn-sm">
										Register
									</Link>
								</div>
							)}
						</div>
					</div>
				</div>
			</nav>

			<main className="container py-6">
				<Routes>
					<Route path="/" element={<Products />} />
					<Route path="/product/:productId" element={<ProductDetail />} />
					<Route path="/login" element={<Login />} />
					<Route path="/register" element={<Register />} />
					<Route path="/cart" element={<Cart />} />
					<Route path="/checkout" element={<Checkout />} />
					<Route path="/orders" element={<OrderHistory />} />
					<Route path="/admin/products" element={<AdminProducts />} />
					<Route path="/admin/orders" element={<AllOrders />} />
					<Route path="/admin/customers" element={<CustomerManagement />} />
					<Route path="/admin/statistics" element={<Statistics />} />
				</Routes>
			</main>
		</div>
	);
}
