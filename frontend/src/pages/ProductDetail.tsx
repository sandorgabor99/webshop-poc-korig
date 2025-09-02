import React from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import { getErrorMessage } from "../utils/errorHandler";
import type { ProductWithReviews, Review } from "../api/types";
import StarRating from "../components/StarRating";
import ReviewForm from "../components/ReviewForm";
import ReviewList from "../components/ReviewList";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

export default function ProductDetail() {
	const { productId } = useParams<{ productId: string }>();
	const [product, setProduct] = React.useState<ProductWithReviews | null>(null);
	const [loading, setLoading] = React.useState(true);
	const [error, setError] = React.useState<string | null>(null);
	const [showReviewForm, setShowReviewForm] = React.useState(false);
	const [userReview, setUserReview] = React.useState<Review | null>(null);
	
	const { addToCart } = useCart();
	const { user } = useAuth();

	React.useEffect(() => {
		if (!productId) return;
		
		api.getProductWithReviews(parseInt(productId))
			.then((productData) => {
				setProduct(productData);
				// Check if user has already reviewed this product
				const userReview = productData.reviews.find(review => review.user_id === user?.id);
				setUserReview(userReview || null);
			})
			.catch(err => setError(getErrorMessage(err)))
			.finally(() => setLoading(false));
	}, [productId, user?.id]);

	const handleAddToCart = (quantity: number = 1) => {
		if (!product) return;
		
		try {
			addToCart(product, quantity);
			setError(null);
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	const handleReviewSubmitted = async () => {
		if (!productId) return;
		
		try {
			const updatedProduct = await api.getProductWithReviews(parseInt(productId));
			setProduct(updatedProduct);
			const userReview = updatedProduct.reviews.find(review => review.user_id === user?.id);
			setUserReview(userReview || null);
			setShowReviewForm(false);
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	const handleReviewDeleted = async (reviewId: number) => {
		if (!productId) return;
		
		try {
			await api.deleteReview(reviewId);
			const updatedProduct = await api.getProductWithReviews(parseInt(productId));
			setProduct(updatedProduct);
			setUserReview(null);
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	if (loading) {
		return (
			<div className="loading">
				<div className="spinner"></div>
				<p className="text-muted">Loading product...</p>
			</div>
		);
	}

	if (!product) {
		return (
			<div className="text-center p-6">
				<p className="text-lg text-muted mb-4">
					Product not found
				</p>
				<Link to="/" className="btn btn-primary">
					← Back to Products
				</Link>
			</div>
		);
	}

	return (
		<div>
			<div className="flex items-center mb-4 gap-3">
				<Link to="/" className="btn btn-outline">
					← Back to Products
				</Link>
				<h1 className="text-2xl font-bold">
					{product.name}
				</h1>
			</div>

			{error && (
				<div className="alert alert-error mb-4">
					{error}
				</div>
			)}

			<div className="grid grid-cols-1 grid-cols-2 mb-6">
				{/* Product Image */}
				<div className="p-4">
					{product.image_url ? (
						<img
							src={product.image_url.startsWith('http') ? product.image_url : `${API_BASE}${product.image_url}`}
							alt={product.name}
							className="w-full h-96 object-cover rounded border"
						/>
					) : (
						<div className="w-full h-96 bg-gray-100 rounded flex items-center justify-center text-4xl text-muted">
							🛍️
						</div>
					)}
				</div>

				{/* Product Details */}
				<div className="p-4">
					<h2 className="text-xl font-semibold mb-3">
						{product.name}
					</h2>

					{product.description && (
						<p className="text-muted mb-4">
							{product.description}
						</p>
					)}

					{/* Rating Display */}
					<div className="flex items-center gap-3 mb-4">
						<StarRating 
							rating={product.average_rating} 
							readonly 
							size="large"
						/>
						<span className="text-sm text-muted">
							({product.review_count} reviews)
						</span>
					</div>

					{/* Price and Stock */}
					<div className="flex justify-between items-center mb-4">
						<span className="text-2xl font-bold text-primary">
							${product.price.toFixed(2)}
						</span>
						<span className={`badge ${product.stock > 0 ? 'badge-success' : 'badge-danger'}`}>
							{product.stock > 0 ? `${product.stock} in stock` : "Out of stock"}
						</span>
					</div>

					{/* Add to Cart */}
					{product.stock > 0 ? (
						<button
							onClick={() => handleAddToCart(1)}
							className="btn btn-primary w-full"
						>
							Add to Cart
						</button>
					) : (
						<button
							disabled
							className="btn btn-secondary w-full"
						>
							Out of Stock
						</button>
					)}
				</div>
			</div>

			{/* Reviews Section */}
			<div className="border-t pt-6">
				<div className="flex justify-between items-center mb-4">
					<h3 className="text-xl font-semibold">
						Customer Reviews
					</h3>
					
					{user && !user.is_admin && !userReview && (
						<button
							onClick={() => setShowReviewForm(true)}
							className="btn btn-primary"
						>
							Write a Review
						</button>
					)}
				</div>

				{showReviewForm && (
					<div className="mb-6">
						<ReviewForm
							productId={product.id}
							onReviewSubmitted={handleReviewSubmitted}
							onCancel={() => setShowReviewForm(false)}
						/>
					</div>
				)}

				<ReviewList
					reviews={product.reviews}
					onReviewDeleted={handleReviewDeleted}
					currentUserId={user?.id}
				/>
			</div>
		</div>
	);
}
