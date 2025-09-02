export type User = {
	id: number;
	email: string;
	username: string;
	role: "ADMINISTRATOR" | "CUSTOMER";
	is_admin: boolean;
	created_at: string;
};

export type UserWithOrders = User & {
	order_count: number;
	total_spent: number;
};

export type UserCreate = {
	email: string;
	username: string;
	password: string;
	role?: "ADMINISTRATOR" | "CUSTOMER";
};

export type UserUpdate = Partial<UserCreate>;

export type LoginCredentials = {
	username: string; // This will be the email for login
	password: string;
};

export type Token = {
	access_token: string;
	token_type: string;
};

export type Product = {
	id: number;
	name: string;
	description?: string | null;
	price: number;
	stock: number;
	image_url?: string | null;
	created_at: string;
	average_rating: number;
	review_count: number;
};

export type ProductCreate = {
	name: string;
	description?: string;
	price: number;
	stock: number;
	image_url?: string;
};

export type ProductUpdate = {
	name?: string;
	description?: string;
	price?: number;
	stock?: number;
	image_url?: string;
};

export type Review = {
	id: number;
	user_id: number;
	product_id: number;
	rating: number;
	feedback?: string | null;
	created_at: string;
	user: User;
};

export type ReviewCreate = {
	product_id: number;
	rating: number;
	feedback?: string;
};

export type ReviewUpdate = {
	rating?: number;
	feedback?: string;
};

export type ProductWithReviews = Product & {
	reviews: Review[];
};

export type OrderItem = {
	id: number;
	product_id: number;
	quantity: number;
	unit_price: number;
};

export type OrderItemWithProduct = OrderItem & {
	product: Product;
};

export type Order = {
	id: number;
	order_id: string;
	total_amount: number;
	created_at: string;
	items: OrderItem[];
};

export type OrderWithDetails = Order & {
	items: OrderItemWithProduct[];
	user: User;
};

export type CustomerOrderSummary = {
	total_orders: number;
	total_spent: number;
	average_order_value: number;
	last_order_date?: string | null;
};
