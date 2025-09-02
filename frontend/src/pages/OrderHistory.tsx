import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import type { OrderWithDetails, CustomerOrderSummary } from '../api/types';
import './OrderHistory.css';

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

export default function OrderHistory() {
	const { user } = useAuth();
	const [orders, setOrders] = useState<OrderWithDetails[]>([]);
	const [summary, setSummary] = useState<CustomerOrderSummary | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [selectedOrder, setSelectedOrder] = useState<OrderWithDetails | null>(null);

	useEffect(() => {
		loadOrders();
	}, []);

	const loadOrders = async () => {
		try {
			setLoading(true);
			setError(null);
			const [ordersData, summaryData] = await Promise.all([
				api.myOrdersDetailed(),
				api.getMyOrderSummary()
			]);
			setOrders(ordersData);
			setSummary(summaryData);
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load orders');
		} finally {
			setLoading(false);
		}
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

	if (loading) {
		return (
			<div className="order-history">
				<div className="loading">Loading your order history...</div>
			</div>
		);
	}

	if (error) {
		return (
			<div className="order-history">
				<div className="error">
					<h2>Error</h2>
					<p>{error}</p>
					<button onClick={loadOrders}>Try Again</button>
				</div>
			</div>
		);
	}

	return (
		<div className="order-history">
			<div className="order-history-header">
				<h1>Order History</h1>
				<p>Welcome back, {user?.email}</p>
			</div>

			{/* Order Summary */}
			{summary && (
				<div className="order-summary">
					<div className="summary-card">
						<h3>Total Orders</h3>
						<p className="summary-number">{summary.total_orders}</p>
					</div>
					<div className="summary-card">
						<h3>Total Spent</h3>
						<p className="summary-number">{formatCurrency(summary.total_spent)}</p>
					</div>
					<div className="summary-card">
						<h3>Average Order</h3>
						<p className="summary-number">{formatCurrency(summary.average_order_value)}</p>
					</div>
					{summary.last_order_date && (
						<div className="summary-card">
							<h3>Last Order</h3>
							<p className="summary-date">{formatDate(summary.last_order_date)}</p>
						</div>
					)}
				</div>
			)}

			{/* Orders List */}
			<div className="orders-section">
				<h2>Your Orders</h2>
				{orders.length === 0 ? (
					<div className="no-orders">
						<p>You haven't placed any orders yet.</p>
						<a href="/products" className="btn-primary">Start Shopping</a>
					</div>
				) : (
					<div className="orders-grid">
						{orders.map((order) => (
							<div key={order.id} className="order-card">
								<div className="order-header">
									<h3>Order #{order.id}</h3>
									<span className="order-date">{formatDate(order.created_at)}</span>
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
