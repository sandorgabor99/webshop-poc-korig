import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import { api } from "../api/client";
import { getErrorMessage } from "../utils/errorHandler";

export default function Cart() {
	const { items, removeFromCart, updateQuantity, clearCart, getTotalPrice } = useCart();
	const { user } = useAuth();
	const navigate = useNavigate();
	const [loading, setLoading] = React.useState(false);
	const [error, setError] = React.useState<string | null>(null);

	const handleQuantityChange = (productId: number, newQuantity: number) => {
		try {
			updateQuantity(productId, newQuantity);
			setError(null);
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	const handleCheckout = async () => {
		if (!user) {
			setError("Please log in to complete your purchase.");
			return;
		}

		if (items.length === 0) {
			setError("Your cart is empty.");
			return;
		}

		setLoading(true);
		setError(null);

		try {
			const orderItems = items.map(item => ({
				id: 0, // Temporary ID for creation
				product_id: item.product.id,
				quantity: item.quantity,
				unit_price: item.product.price
			}));

			await api.createOrder(orderItems);
			clearCart();
			navigate("/");
		} catch (err) {
			setError(getErrorMessage(err));
		} finally {
			setLoading(false);
		}
	};

	if (items.length === 0) {
		return (
			<div>
				<div style={{
					display: "flex",
					justifyContent: "space-between",
					alignItems: "center",
					marginBottom: "2rem",
					flexWrap: "wrap",
					gap: "1rem"
				}}>
					<div>
						<h1 style={{
							fontSize: "2rem",
							fontWeight: "bold",
							color: "var(--text)",
							marginBottom: "0.5rem"
						}}>
							Shopping Cart
						</h1>
						<p style={{ color: "var(--text-muted)" }}>
							Your cart is empty
						</p>
					</div>
					<Link to="/" className="btn btn-primary">
						Continue Shopping
					</Link>
				</div>

				<div style={{
					textAlign: "center",
					padding: "4rem 2rem",
					color: "var(--text-muted)"
				}}>
					<div style={{
						fontSize: "4rem",
						marginBottom: "1rem"
					}}>
						🛒
					</div>
					<h2 style={{
						fontSize: "1.5rem",
						marginBottom: "1rem",
						color: "var(--text)"
					}}>
						Your cart is empty
					</h2>
					<p style={{ marginBottom: "2rem" }}>
						Looks like you haven't added any items to your cart yet.
					</p>
					<Link to="/" className="btn btn-primary">
						Start Shopping
					</Link>
				</div>
			</div>
		);
	}

	return (
		<div>
			<div style={{
				display: "flex",
				justifyContent: "space-between",
				alignItems: "center",
				marginBottom: "2rem",
				flexWrap: "wrap",
				gap: "1rem"
			}}>
				<div>
					<h1 style={{
						fontSize: "2rem",
						fontWeight: "bold",
						color: "var(--text)",
						marginBottom: "0.5rem"
					}}>
						Shopping Cart
					</h1>
					<p style={{ color: "var(--text-muted)" }}>
						{items.length} item{items.length !== 1 ? 's' : ''} in your cart
					</p>
				</div>
				<div style={{ display: "flex", gap: "1rem" }}>
					<button
						onClick={clearCart}
						className="btn btn-secondary"
						style={{ fontSize: "0.875rem" }}
					>
						Clear Cart
					</button>
					<Link to="/" className="btn btn-secondary">
						Continue Shopping
					</Link>
				</div>
			</div>

			{error && (
				<div style={{
					padding: "1rem",
					background: "rgb(239 68 68 / 0.1)",
					border: "1px solid var(--danger)",
					borderRadius: "0.5rem",
					color: "var(--danger)",
					marginBottom: "2rem"
				}}>
					{error}
				</div>
			)}

			<div style={{
				display: "grid",
				gridTemplateColumns: "2fr 1fr",
				gap: "2rem",
				alignItems: "start"
			}}>
				{/* Cart Items */}
				<div>
					<h2 style={{
						fontSize: "1.5rem",
						fontWeight: "600",
						marginBottom: "1rem",
						color: "var(--text)"
					}}>
						Cart Items
					</h2>
					
					<div style={{
						display: "flex",
						flexDirection: "column",
						gap: "1rem"
					}}>
						{items.map((item) => (
							<div key={item.product.id} className="card" style={{
								display: "flex",
								alignItems: "center",
								gap: "1rem",
								padding: "1.5rem"
							}}>
								<div style={{
									width: "80px",
									height: "80px",
									background: "var(--primary)",
									borderRadius: "0.5rem",
									display: "flex",
									alignItems: "center",
									justifyContent: "center",
									fontSize: "2rem"
								}}>
									🛍️
								</div>
								
								<div style={{ flex: 1 }}>
									<h3 style={{
										fontSize: "1.125rem",
										fontWeight: "600",
										marginBottom: "0.25rem",
										color: "var(--text)"
									}}>
										{item.product.name}
									</h3>
									<p style={{
										color: "var(--text-muted)",
										fontSize: "0.875rem",
										marginBottom: "0.5rem"
									}}>
										{item.product.description || "No description"}
									</p>
									<div style={{
										display: "flex",
										alignItems: "center",
										gap: "1rem"
									}}>
										<span style={{
											fontSize: "1.25rem",
											fontWeight: "bold",
											color: "var(--primary)"
										}}>
											${item.product.price.toFixed(2)}
										</span>
										<span style={{
											padding: "0.25rem 0.5rem",
											background: item.product.stock > 0 
												? "rgb(16 185 129 / 0.1)" 
												: "rgb(239 68 68 / 0.1)",
											color: item.product.stock > 0 
												? "var(--success)" 
												: "var(--danger)",
											borderRadius: "0.25rem",
											fontSize: "0.75rem",
											fontWeight: "500"
										}}>
											{item.product.stock} in stock
										</span>
									</div>
								</div>

								<div style={{
									display: "flex",
									flexDirection: "column",
									alignItems: "center",
									gap: "0.5rem"
								}}>
									<div style={{
										display: "flex",
										alignItems: "center",
										gap: "0.5rem"
									}}>
										<button
											onClick={() => handleQuantityChange(item.product.id, item.quantity - 1)}
											disabled={item.quantity <= 1}
											style={{
												width: "32px",
												height: "32px",
												border: "1px solid var(--border)",
												background: "white",
												borderRadius: "0.25rem",
												cursor: item.quantity > 1 ? "pointer" : "not-allowed",
												opacity: item.quantity > 1 ? 1 : 0.5
											}}
										>
											-
										</button>
										<span style={{
											minWidth: "40px",
											textAlign: "center",
											fontWeight: "500"
										}}>
											{item.quantity}
										</span>
										<button
											onClick={() => handleQuantityChange(item.product.id, item.quantity + 1)}
											disabled={item.quantity >= item.product.stock}
											style={{
												width: "32px",
												height: "32px",
												border: "1px solid var(--border)",
												background: "white",
												borderRadius: "0.25rem",
												cursor: item.quantity < item.product.stock ? "pointer" : "not-allowed",
												opacity: item.quantity < item.product.stock ? 1 : 0.5
											}}
										>
											+
										</button>
									</div>
									
									<button
										onClick={() => removeFromCart(item.product.id)}
										className="btn btn-danger"
										style={{ fontSize: "0.75rem", padding: "0.25rem 0.5rem" }}
									>
										Remove
									</button>
								</div>
							</div>
						))}
					</div>
				</div>

				{/* Order Summary */}
				<div>
					<div className="card" style={{ padding: "1.5rem" }}>
						<h2 style={{
							fontSize: "1.5rem",
							fontWeight: "600",
							marginBottom: "1rem",
							color: "var(--text)"
						}}>
							Order Summary
						</h2>

						<div style={{
							display: "flex",
							flexDirection: "column",
							gap: "0.75rem",
							marginBottom: "1.5rem"
						}}>
							{items.map((item) => (
								<div key={item.product.id} style={{
									display: "flex",
									justifyContent: "space-between",
									alignItems: "center"
								}}>
									<div>
										<span style={{ fontWeight: "500" }}>{item.product.name}</span>
										<span style={{ color: "var(--text-muted)", fontSize: "0.875rem" }}>
											{" "}× {item.quantity}
										</span>
									</div>
									<span>${(item.product.price * item.quantity).toFixed(2)}</span>
								</div>
							))}
						</div>

						<hr style={{
							border: "none",
							borderTop: "1px solid var(--border)",
							margin: "1rem 0"
						}} />

						<div style={{
							display: "flex",
							justifyContent: "space-between",
							alignItems: "center",
							fontWeight: "bold",
							fontSize: "1.25rem",
							marginBottom: "1.5rem"
						}}>
							<span>Total:</span>
							<span>${getTotalPrice().toFixed(2)}</span>
						</div>

						{!user && (
							<div style={{
								padding: "1rem",
								background: "rgb(245 158 11 / 0.1)",
								border: "1px solid var(--warning)",
								borderRadius: "0.5rem",
								color: "var(--warning)",
								marginBottom: "1rem",
								fontSize: "0.875rem"
							}}>
								Please log in to complete your purchase.
							</div>
						)}

						<button
							onClick={handleCheckout}
							disabled={loading || !user || items.length === 0}
							className="btn btn-primary"
							style={{
								width: "100%",
								padding: "1rem",
								fontSize: "1.125rem",
								opacity: (loading || !user || items.length === 0) ? 0.7 : 1
							}}
						>
							{loading ? "Processing..." : "Proceed to Checkout"}
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}
