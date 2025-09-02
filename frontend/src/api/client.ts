import type { Product, ProductCreate, ProductUpdate, Token, User, Order, OrderItem, OrderWithDetails, CustomerOrderSummary, UserWithOrders, Review, ReviewCreate, ReviewUpdate, ProductWithReviews } from "./types";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

function getToken(): string | null {
	return localStorage.getItem("token");
}

function setToken(token: string | null) {
	if (token) localStorage.setItem("token", token);
	else localStorage.removeItem("token");
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
	const headers = new Headers(options.headers || {});
	if (!headers.has("Content-Type")) headers.set("Content-Type", "application/json");
	const token = getToken();
	if (token) headers.set("Authorization", `Bearer ${token}`);
	const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
	if (!res.ok) {
		const text = await res.text();
		throw new Error(text || res.statusText);
	}
	if (res.status === 204) return undefined as unknown as T;
	return (await res.json()) as T;
}

export const api = {
	setToken,
	getToken,
	async login(username: string, password: string): Promise<Token> {
		const body = new URLSearchParams();
		body.set("username", username);
		body.set("password", password);
		body.set("grant_type", "password");
		body.set("scope", "");
		body.set("client_id", "");
		body.set("client_secret", "");
		const res = await fetch(`${API_BASE}/auth/login`, {
			method: "POST",
			headers: { "Content-Type": "application/x-www-form-urlencoded" },
			body,
		});
		if (!res.ok) throw new Error(await res.text());
		const token = (await res.json()) as Token;
		api.setToken(token.access_token);
		return token;
	},
	async register(email: string, username: string, password: string): Promise<User> {
		return request<User>(`/auth/register`, { method: "POST", body: JSON.stringify({ email, username, password }) });
	},
	async me(): Promise<User> {
		return request<User>(`/auth/me`);
	},
	async listProducts(): Promise<Product[]> {
		return request<Product[]>(`/products/`);
	},
	async getProduct(id: number): Promise<Product> {
		return request<Product>(`/products/${id}`);
	},
	async createProduct(p: ProductCreate): Promise<Product> {
		return request<Product>(`/products/`, { method: "POST", body: JSON.stringify(p) });
	},
	async updateProduct(id: number, p: ProductUpdate): Promise<Product> {
		return request<Product>(`/products/${id}`, { method: "PATCH", body: JSON.stringify(p) });
	},
	async deleteProduct(id: number): Promise<void> {
		await request<void>(`/products/${id}`, { method: "DELETE" });
	},
	async uploadImage(file: File): Promise<{ filename: string; url: string }> {
		const formData = new FormData();
		formData.append("file", file);
		
		const headers = new Headers();
		const token = getToken();
		if (token) headers.set("Authorization", `Bearer ${token}`);
		
		const res = await fetch(`${API_BASE}/upload/image`, {
			method: "POST",
			headers,
			body: formData,
		});
		
		if (!res.ok) {
			const text = await res.text();
			throw new Error(text || res.statusText);
		}
		
		return (await res.json()) as { filename: string; url: string };
	},
	async createOrder(items: OrderItem[]): Promise<Order> {
		return request<Order>(`/orders/`, { method: "POST", body: JSON.stringify({ items }) });
	},
	async myOrders(): Promise<Order[]> {
		return request<Order[]>(`/orders/`);
	},
	// Enhanced order history endpoints
	async myOrdersDetailed(): Promise<OrderWithDetails[]> {
		return request<OrderWithDetails[]>(`/orders/detailed`);
	},
	async getOrderDetails(orderId: number): Promise<OrderWithDetails> {
		return request<OrderWithDetails>(`/orders/${orderId}`);
	},
	async getMyOrderSummary(): Promise<CustomerOrderSummary> {
		return request<CustomerOrderSummary>(`/orders/summary`);
	},
	// Admin endpoints for order management
	async getAllOrders(skip: number = 0, limit: number = 100, search?: string): Promise<OrderWithDetails[]> {
		const searchParam = search ? `&search=${encodeURIComponent(search)}` : '';
		return request<OrderWithDetails[]>(`/orders/admin/all?skip=${skip}&limit=${limit}${searchParam}`);
	},
	async searchOrderById(orderId: string): Promise<OrderWithDetails> {
		return request<OrderWithDetails>(`/orders/admin/search/${orderId}`);
	},
	async getCustomerOrders(userId: number): Promise<OrderWithDetails[]> {
		return request<OrderWithDetails[]>(`/orders/admin/customer/${userId}`);
	},
	// Customer management endpoints
	async listCustomers(skip: number = 0, limit: number = 100): Promise<UserWithOrders[]> {
		return request<UserWithOrders[]>(`/customers/?skip=${skip}&limit=${limit}`);
	},
	async getCustomer(userId: number): Promise<User> {
		return request<User>(`/customers/${userId}`);
	},
	async getCustomerOrderSummary(userId: number): Promise<CustomerOrderSummary> {
		return request<CustomerOrderSummary>(`/customers/${userId}/summary`);
	},
	// Review endpoints
	async getProductReviews(productId: number): Promise<Review[]> {
		return request<Review[]>(`/reviews/product/${productId}`);
	},
	async getProductWithReviews(productId: number): Promise<ProductWithReviews> {
		return request<ProductWithReviews>(`/reviews/product/${productId}/with-reviews`);
	},
	async createReview(review: ReviewCreate): Promise<Review> {
		return request<Review>(`/reviews/`, { method: "POST", body: JSON.stringify(review) });
	},
	async updateReview(reviewId: number, review: ReviewUpdate): Promise<Review> {
		return request<Review>(`/reviews/${reviewId}`, { method: "PATCH", body: JSON.stringify(review) });
	},
	async deleteReview(reviewId: number): Promise<void> {
		await request<void>(`/reviews/${reviewId}`, { method: "DELETE" });
	},
	async getMyReviews(): Promise<Review[]> {
		return request<Review[]>(`/reviews/user/me`);
	},
};
