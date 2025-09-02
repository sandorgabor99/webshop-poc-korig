import React from "react";
import { useSearchParams, Link } from "react-router-dom";
import { api } from "../api/client";
import { getErrorMessage } from "../utils/errorHandler";
import type { Order, Product } from "../api/types";

export default function Checkout() {
	const [searchParams] = useSearchParams();
	const [products, setProducts] = React.useState<Product[]>([]);
	const [selectedProduct, setSelectedProduct] = React.useState<Product | null>(null);
	const [quantity, setQuantity] = React.useState<number>(1);
	const [order, setOrder] = React.useState<Order | null>(null);
	const [error, setError] = React.useState<string | null>(null);
	const [loading, setLoading] = React.useState(false);
	const [productsLoading, setProductsLoading] = React.useState(true);

	// Load products on component mount
	React.useEffect(() => {
		const loadProducts = async () => {
			try {
				const productList = await api.listProducts();
				setProducts(productList);
				
				// If there's a product ID in URL, select it
				const productId = searchParams.get('product');
				if (productId) {
					const product = productList.find(p => p.id === parseInt(productId));
					if (product) {
						setSelectedProduct(product);
					}
				}
			} catch (err) {
				setError(getErrorMessage(err));
			} finally {
				setProductsLoading(false);
			}
		};
		
		loadProducts();
	}, [searchParams]);

	const handleProductSelect = (product: Product) => {
		setSelectedProduct(product);
		setQuantity(1); // Reset quantity when product changes
		setError(null);
		setOrder(null);
	};

	const handleQuantityChange = (newQuantity: number) => {
		if (newQuantity < 1) return;
		if (selectedProduct && newQuantity > selectedProduct.stock) {
			setError(`Sorry, only ${selectedProduct.stock} items available in stock.`);
			return;
		}
		setQuantity(newQuantity);
		setError(null);
	};

	const submit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!selectedProduct) {
			setError('Please select a product first.');
			return;
		}
		
		setError(null);
		setLoading(true);
		
		try {
			const newOrder = await api.createOrder([{ 
				id: 0, // Temporary ID for creation
				product_id: selectedProduct.id, 
				quantity,
				unit_price: selectedProduct.price
			}]);
			setOrder(newOrder);
		} catch (err) {
			setError(getErrorMessage(err));
		} finally {
			setLoading(false);
		}
	};

	if (productsLoading) {
		return (
			<div style={{
				display: "flex",
				justifyContent: "center",
				alignItems: "center",
				minHeight: "40vh"
			}}>
				<div style={{
					textAlign: "center",
					color: "var(--text-muted)"
				}}>
					<div style={{
						width: "40px",
						height: "40px",
						border: "3px solid var(--border)",
						borderTop: "3px solid var(--primary)",
						borderRadius: "50%",
						animation: "spin 1s linear infinite",
						margin: "0 auto 1rem"
					}}></div>
					<p>Loading products...</p>
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
						Checkout
					</h1>
					<p style={{ color: "var(--text-muted)" }}>
						Select a product and quantity to complete your purchase
					</p>
				</div>
				<Link to="/" className="btn btn-secondary">
					← Back to Products
				</Link>
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

			{order && (
				<div style={{
					padding: "1.5rem",
					background: "rgb(16 185 129 / 0.1)",
					border: "1px solid var(--success)",
					borderRadius: "0.5rem",
					marginBottom: "2rem"
				}}>
					<h3 style={{
						color: "var(--success)",
						marginBottom: "1rem"
					}}>
						✅ Order Successful!
					</h3>
					<div style={{
						background: "white",
						padding: "1rem",
						borderRadius: "0.5rem",
						fontFamily: "monospace",
						fontSize: "0.875rem"
					}}>
						<strong>Order ID:</strong> {order.id}<br />
						<strong>Total Amount:</strong> ${order.total_amount.toFixed(2)}<br />
						<strong>Created:</strong> {new Date(order.created_at).toLocaleString()}
					</div>
				</div>
			)}

			<div style={{
				display: "grid",
				gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
				gap: "2rem",
				alignItems: "start"
			}}>
				{/* Product Selection */}
				<div>
					<h2 style={{
						fontSize: "1.5rem",
						fontWeight: "600",
						marginBottom: "1rem",
						color: "var(--text)"
					}}>
						Select Product
					</h2>
					
					{products.length === 0 ? (
						<div style={{
							textAlign: "center",
							padding: "2rem",
							color: "var(--text-muted)"
						}}>
							<p>No products available</p>
						</div>
					) : (
						<div style={{
							display: "flex",
							flexDirection: "column",
							gap: "1rem",
							maxHeight: "400px",
							overflowY: "auto"
						}}>
							{products.map((product) => (
								<div
									key={product.id}
									className="card"
									style={{
										cursor: "pointer",
										border: selectedProduct?.id === product.id 
											? "2px solid var(--primary)" 
											: "1px solid var(--border)",
										opacity: product.stock === 0 ? 0.6 : 1
									}}
									onClick={() => product.stock > 0 && handleProductSelect(product)}
								>
									<div style={{
										display: "flex",
										alignItems: "center",
										gap: "1rem"
									}}>
										<div style={{
											width: "50px",
											height: "50px",
											background: "var(--primary)",
											borderRadius: "0.5rem",
											display: "flex",
											alignItems: "center",
											justifyContent: "center",
											fontSize: "1.5rem"
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
												{product.name}
											</h3>
											<p style={{
												color: "var(--text-muted)",
												fontSize: "0.875rem",
												marginBottom: "0.5rem"
											}}>
												{product.description || "No description"}
											</p>
											<div style={{
												display: "flex",
												justifyContent: "space-between",
												alignItems: "center"
											}}>
												<span style={{
													fontSize: "1.25rem",
													fontWeight: "bold",
													color: "var(--primary)"
												}}>
													${product.price.toFixed(2)}
												</span>
												<span style={{
													padding: "0.25rem 0.5rem",
													background: product.stock > 0 
														? "rgb(16 185 129 / 0.1)" 
														: "rgb(239 68 68 / 0.1)",
													color: product.stock > 0 
														? "var(--success)" 
														: "var(--danger)",
													borderRadius: "0.25rem",
													fontSize: "0.75rem",
													fontWeight: "500"
												}}>
													{product.stock > 0 ? `${product.stock} in stock` : "Out of stock"}
												</span>
											</div>
										</div>
									</div>
								</div>
							))}
						</div>
					)}
				</div>

				{/* Order Form */}
				<div>
					<h2 style={{
						fontSize: "1.5rem",
						fontWeight: "600",
						marginBottom: "1rem",
						color: "var(--text)"
					}}>
						Order Details
					</h2>
					
					{selectedProduct ? (
						<div className="card" style={{ padding: "1.5rem" }}>
							<div style={{
								display: "flex",
								alignItems: "center",
								gap: "1rem",
								marginBottom: "1.5rem"
							}}>
								<div style={{
									width: "60px",
									height: "60px",
									background: "var(--primary)",
									borderRadius: "0.5rem",
									display: "flex",
									alignItems: "center",
									justifyContent: "center",
									fontSize: "2rem"
								}}>
									🛍️
								</div>
								<div>
									<h3 style={{
										fontSize: "1.25rem",
										fontWeight: "600",
										marginBottom: "0.25rem"
									}}>
										{selectedProduct.name}
									</h3>
									<p style={{
										color: "var(--text-muted)",
										fontSize: "0.875rem"
									}}>
										{selectedProduct.description || "No description"}
									</p>
								</div>
							</div>

							<form onSubmit={submit}>
								<div style={{ marginBottom: "1.5rem" }}>
									<label style={{
										display: "block",
										marginBottom: "0.5rem",
										fontWeight: "500",
										color: "var(--text)"
									}}>
										Quantity
									</label>
									<div style={{
										display: "flex",
										alignItems: "center",
										gap: "0.5rem"
									}}>
										<button
											type="button"
											onClick={() => handleQuantityChange(quantity - 1)}
											disabled={quantity <= 1}
											style={{
												width: "40px",
												height: "40px",
												border: "1px solid var(--border)",
												background: "white",
												borderRadius: "0.5rem",
												cursor: quantity > 1 ? "pointer" : "not-allowed",
												opacity: quantity > 1 ? 1 : 0.5
											}}
										>
											-
										</button>
										<input
											type="number"
											value={quantity}
											onChange={(e) => handleQuantityChange(parseInt(e.target.value) || 1)}
											min="1"
											max={selectedProduct.stock}
											style={{
												width: "80px",
												textAlign: "center",
												padding: "0.5rem",
												border: "1px solid var(--border)",
												borderRadius: "0.5rem"
											}}
										/>
										<button
											type="button"
											onClick={() => handleQuantityChange(quantity + 1)}
											disabled={quantity >= selectedProduct.stock}
											style={{
												width: "40px",
												height: "40px",
												border: "1px solid var(--border)",
												background: "white",
												borderRadius: "0.5rem",
												cursor: quantity < selectedProduct.stock ? "pointer" : "not-allowed",
												opacity: quantity < selectedProduct.stock ? 1 : 0.5
											}}
										>
											+
										</button>
									</div>
									<p style={{
										fontSize: "0.875rem",
										color: "var(--text-muted)",
										marginTop: "0.5rem"
									}}>
										{selectedProduct.stock} items available
									</p>
								</div>

								<div style={{
									padding: "1rem",
									background: "var(--surface)",
									borderRadius: "0.5rem",
									marginBottom: "1.5rem"
								}}>
									<div style={{
										display: "flex",
										justifyContent: "space-between",
										marginBottom: "0.5rem"
									}}>
										<span>Unit Price:</span>
										<span>${selectedProduct.price.toFixed(2)}</span>
									</div>
									<div style={{
										display: "flex",
										justifyContent: "space-between",
										marginBottom: "0.5rem"
									}}>
										<span>Quantity:</span>
										<span>{quantity}</span>
									</div>
									<hr style={{
										border: "none",
										borderTop: "1px solid var(--border)",
										margin: "0.5rem 0"
									}} />
									<div style={{
										display: "flex",
										justifyContent: "space-between",
										fontWeight: "bold",
										fontSize: "1.125rem"
									}}>
										<span>Total:</span>
										<span>${(selectedProduct.price * quantity).toFixed(2)}</span>
									</div>
								</div>

								<button
									type="submit"
									disabled={loading}
									className="btn btn-primary"
									style={{
										width: "100%",
										padding: "1rem",
										fontSize: "1.125rem",
										opacity: loading ? 0.7 : 1
									}}
								>
									{loading ? "Processing..." : "Complete Purchase"}
								</button>
							</form>
						</div>
					) : (
						<div style={{
							textAlign: "center",
							padding: "3rem",
							color: "var(--text-muted)"
						}}>
							<div style={{
								fontSize: "3rem",
								marginBottom: "1rem"
							}}>
								🛒
							</div>
							<p>Select a product from the list to start your purchase</p>
						</div>
					)}
				</div>
			</div>
		</div>
	);
}
