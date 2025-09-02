import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import type { OrderWithDetails } from '../api/types';
import './AllOrders.css';

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

export default function AllOrders() {
	const { user } = useAuth();
	const [orders, setOrders] = useState<OrderWithDetails[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [selectedOrder, setSelectedOrder] = useState<OrderWithDetails | null>(null);
	const [searchTerm, setSearchTerm] = useState('');

	useEffect(() => {
		loadOrders();
	}, []);

	const loadOrders = async (search?: string) => {
		try {
			setLoading(true);
			setError(null);
			const ordersData = await api.getAllOrders(0, 100, search);
			setOrders(ordersData);
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load orders');
		} finally {
			setLoading(false);
		}
	};

	const handleSearch = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!searchTerm.trim()) return;
		loadOrders(searchTerm.trim());
	};

	const handleClearSearch = () => {
		setSearchTerm('');
		loadOrders();
	};

	const formatDate = (dateString: string) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	};

	const formatCurrency = (amount: number) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	};

	if (!user?.is_admin) {
		return (
			<div className="all-orders">
				<div className="access-denied">
					<h2>Access Denied</h2>
					<p>You don't have permission to access this page.</p>
				</div>
			</div>
		);
	}

	if (loading) {
		return (
			<div className="all-orders">
				<div className="loading">Loading all orders...</div>
			</div>
		);
	}

	if (error) {
		return (
			<div className="all-orders">
				<div className="error">
					<h2>Error</h2>
					<p>{error}</p>
					<button onClick={() => loadOrders()}>Try Again</button>
				</div>
			</div>
		);
	}

	return (
		<div className="all-orders">
			<div className="all-orders-header">
				<h1>All Orders</h1>
				<p>View and manage all customer orders</p>
				
				{/* Search Form */}
				<form onSubmit={handleSearch} className="search-form">
					<div className="search-input-group">
						<input
							type="text"
							value={searchTerm}
							onChange={(e) => setSearchTerm(e.target.value)}
							placeholder="Search by Order ID (e.g., ORD-12345678)"
							className="search-input"
						/>
						<button type="submit" className="btn-primary">
							Search
						</button>
						{searchTerm && (
							<button type="button" onClick={handleClearSearch} className="btn-secondary">
								Clear
							</button>
						)}
					</div>
				</form>
			</div>

			{/* Orders List */}
			<div className="orders-section">
				<h2>Orders ({orders.length})</h2>
				{orders.length === 0 ? (
					<div className="no-orders">
						<p>No orders found.</p>
					</div>
				) : (
					<div className="orders-grid">
						{orders.map((order) => (
							<div key={order.id} className="order-card">
								<div className="order-header">
									<h3>Order {order.order_id}</h3>
									<span className="order-date">{formatDate(order.created_at)}</span>
								</div>
								<div className="order-customer">
									<p><strong>Customer:</strong> {order.user.username}</p>
									<p><strong>Email:</strong> {order.user.email}</p>
								</div>
								<div className="order-details">
									<p className="order-total">Total: {formatCurrency(order.total_amount)}</p>
									<p className="order-items">{order.items.length} item{order.items.length !== 1 ? 's' : ''}</p>
								</div>
								<button
									className="btn-secondary"
									onClick={() => setSelectedOrder(selectedOrder?.id === order.id ? null : order)}
								>
									{selectedOrder?.id === order.id ? 'Hide Details' : 'View Details'}
								</button>
								
								{selectedOrder?.id === order.id && (
									<div className="order-items-detail">
										<h4>Order Items:</h4>
										<div className="items-list">
											{order.items.map((item) => (
												<div key={item.id} className="item-detail">
													<div className="item-info">
														<h5>{(item as any).product?.name || `Product ${item.product_id}`}</h5>
														<p className="item-description">{(item as any).product?.description || 'No description available'}</p>
														<p className="item-price">
															{formatCurrency(item.unit_price)} × {item.quantity} = {formatCurrency(item.unit_price * item.quantity)}
														</p>
													</div>
													{(item as any).product?.image_url && (
														<img 
															src={(item as any).product.image_url.startsWith('http') ? (item as any).product.image_url : `${API_BASE}${(item as any).product.image_url}`} 
															alt={(item as any).product.name}
															className="item-image"
														/>
													)}
												</div>
											))}
										</div>
									</div>
								)}
							</div>
						))}
					</div>
				)}
			</div>
		</div>
	);
}
