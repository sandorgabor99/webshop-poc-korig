import React from "react";
import { api } from "../api/client";
import { useCart } from "../context/CartContext";
import { getErrorMessage } from "../utils/errorHandler";
import type { Product } from "../api/types";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import StarRating from "../components/StarRating";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

export default function Products() {
	const [products, setProducts] = React.useState<Product[]>([]);
	const [loading, setLoading] = React.useState(true);
	const [error, setError] = React.useState<string | null>(null);
	const { addToCart } = useCart();
	const { user } = useAuth();

	React.useEffect(() => {
		api.listProducts()
			.then(setProducts)
			.catch(err => setError(getErrorMessage(err)))
			.finally(() => setLoading(false));
	}, []);

	const handleAddToCart = (product: Product, quantity: number = 1) => {
		try {
			addToCart(product, quantity);
			setError(null);
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	if (loading) {
		return (
			<div className="loading" data-testid="loading">
				<div className="spinner"></div>
			</div>
		);
	}

	if (error) {
		return (
			<div className="alert alert-error">
				{error}
			</div>
		);
	}

	return (
		<div>
			<h1 className="text-2xl font-bold mb-6">Products</h1>
			
			{products.length === 0 ? (
				<div className="text-center py-8">
					<p className="text-muted">No products available.</p>
				</div>
			) : (
				<div className="grid grid-cols-1 grid-cols-2 grid-cols-3 grid-cols-4">
					{products.map((product) => (
						<div key={product.id} className="product-card">
							{product.image_url ? (
								<img
									src={product.image_url.startsWith('http') ? product.image_url : `${API_BASE}${product.image_url}`}
									alt={product.name}
									className="product-image"
								/>
							) : (
								<div className="product-image bg-gray-100 flex items-center justify-center">
									<span className="text-muted">No image</span>
								</div>
							)}
							<div className="product-content">
								<h3 className="product-title">
									<Link to={`/product/${product.id}`}>
										{product.name}
									</Link>
								</h3>
								{product.description && (
									<p className="product-description">
										{product.description}
									</p>
								)}
								<div className="flex items-center gap-2 mb-2">
									<StarRating 
										rating={product.average_rating} 
										readonly 
										size="small"
									/>
									<span className="text-sm text-muted">
										({product.review_count})
									</span>
								</div>
								<div className="flex justify-between items-center mb-4">
									<span className="product-price">
										${product.price.toFixed(2)}
									</span>
									<span className={`badge ${product.stock > 0 ? 'badge-success' : 'badge-danger'}`}>
										{product.stock > 0 ? `${product.stock} in stock` : "Out of stock"}
									</span>
								</div>
								<div className="product-actions">
									{product.stock > 0 ? (
										<button
											onClick={() => handleAddToCart(product, 1)}
											className="btn btn-primary"
										>
											Add to Cart
										</button>
									) : (
										<button disabled className="btn btn-secondary">
											Out of Stock
										</button>
									)}
									<Link to={`/product/${product.id}`} className="btn btn-outline">
										View Details
									</Link>
								</div>
							</div>
						</div>
					))}
				</div>
			)}
		</div>
	);
}
