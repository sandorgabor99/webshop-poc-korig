import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import type { UserWithOrders, OrderWithDetails, CustomerOrderSummary } from '../api/types';
import './CustomerManagement.css';

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

export default function CustomerManagement() {
	const { user } = useAuth();
	const [customers, setCustomers] = useState<UserWithOrders[]>([]);
	const [selectedCustomer, setSelectedCustomer] = useState<UserWithOrders | null>(null);
	const [customerOrders, setCustomerOrders] = useState<OrderWithDetails[]>([]);
	const [customerSummary, setCustomerSummary] = useState<CustomerOrderSummary | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [showCustomerDetails, setShowCustomerDetails] = useState(false);

	useEffect(() => {
		loadCustomers();
	}, []);

	const loadCustomers = async () => {
		try {
			setLoading(true);
			setError(null);
			const customersData = await api.listCustomers();
			setCustomers(customersData);
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load customers');
		} finally {
			setLoading(false);
		}
	};

	const loadCustomerDetails = async (customer: UserWithOrders) => {
		try {
			setSelectedCustomer(customer);
			const [ordersData, summaryData] = await Promise.all([
				api.getCustomerOrders(customer.id),
				api.getCustomerOrderSummary(customer.id)
			]);
			setCustomerOrders(ordersData);
			setCustomerSummary(summaryData);
			setShowCustomerDetails(true);
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load customer details');
		}
	};

	const closeCustomerDetails = () => {
		setShowCustomerDetails(false);
		setSelectedCustomer(null);
		setCustomerOrders([]);
		setCustomerSummary(null);
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
			<div className="customer-management">
				<div className="access-denied">
					<h2>Access Denied</h2>
					<p>You don't have permission to access this page.</p>
				</div>
			</div>
		);
	}

	if (loading) {
		return (
			<div className="customer-management">
				<div className="loading">Loading customers...</div>
			</div>
		);
	}

	if (error) {
		return (
			<div className="customer-management">
				<div className="error">
					<h2>Error</h2>
					<p>{error}</p>
					<button onClick={loadCustomers}>Try Again</button>
				</div>
			</div>
		);
	}

	return (
		<div className="customer-management">
			<div className="customer-management-header">
				<h1>Customer Management</h1>
				<p>Manage and view customer information</p>
			</div>

			{/* Customers List */}
			<div className="customers-section">
				<h2>Customers</h2>
				{customers.length === 0 ? (
					<div className="no-customers">
						<p>No customers found.</p>
					</div>
				) : (
					<div className="customers-grid">
						{customers.map((customer) => (
							<div key={customer.id} className="customer-card">
								<div className="customer-info">
									<h3>{customer.username}</h3>
									<p className="customer-email">{customer.email}</p>
									<p className="customer-date">Joined: {formatDate(customer.created_at)}</p>
									<div className="customer-stats">
										<span className="stat">
											Orders: {customer.order_count}
										</span>
										<span className="stat">
											Total: {formatCurrency(customer.total_spent)}
										</span>
									</div>
								</div>
								<button
									className="btn-primary"
									onClick={() => loadCustomerDetails(customer)}
								>
									View Details
								</button>
							</div>
						))}
					</div>
				)}
			</div>

			{/* Customer Details Modal */}
			{showCustomerDetails && selectedCustomer && (
				<div className="customer-details-modal">
					<div className="modal-content">
						<div className="modal-header">
							<h2>Customer Details</h2>
							<button className="close-btn" onClick={closeCustomerDetails}>×</button>
						</div>
						
						<div className="customer-detail-info">
							<h3>{selectedCustomer.email}</h3>
							<p>Customer ID: {selectedCustomer.id}</p>
							<p>Joined: {formatDate(selectedCustomer.created_at)}</p>
						</div>

						{/* Customer Summary */}
						{customerSummary && (
							<div className="customer-summary">
								<h3>Order Summary</h3>
								<div className="summary-grid">
									<div className="summary-item">
										<span className="label">Total Orders:</span>
										<span className="value">{customerSummary.total_orders}</span>
									</div>
									<div className="summary-item">
										<span className="label">Total Spent:</span>
										<span className="value">{formatCurrency(customerSummary.total_spent)}</span>
									</div>
									<div className="summary-item">
										<span className="label">Average Order:</span>
										<span className="value">{formatCurrency(customerSummary.average_order_value)}</span>
									</div>
									{customerSummary.last_order_date && (
										<div className="summary-item">
											<span className="label">Last Order:</span>
											<span className="value">{formatDate(customerSummary.last_order_date)}</span>
										</div>
									)}
								</div>
							</div>
						)}

						{/* Customer Orders */}
						<div className="customer-orders">
							<h3>Order History</h3>
							{customerOrders.length === 0 ? (
								<p className="no-orders">No orders found for this customer.</p>
							) : (
								<div className="orders-list">
									{customerOrders.map((order) => (
										<div key={order.id} className="order-item">
											<div className="order-header">
												<h4>Order #{order.id}</h4>
												<span className="order-date">{formatDate(order.created_at)}</span>
											</div>
											<div className="order-info">
												<p>Total: {formatCurrency(order.total_amount)}</p>
												<p>Items: {order.items.length}</p>
											</div>
											<div className="order-items">
												<h5>Items:</h5>
												<div className="items-grid">
													{order.items.map((item) => (
														<div key={item.id} className="item">
															<div className="item-info">
																<span className="item-name">{(item as any).product?.name || `Product ${item.product_id}`}</span>
																<span className="item-price">
																	{formatCurrency(item.unit_price)} × {item.quantity}
																</span>
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
										</div>
									))}
								</div>
							)}
						</div>
					</div>
				</div>
			)}
		</div>
	);
}
