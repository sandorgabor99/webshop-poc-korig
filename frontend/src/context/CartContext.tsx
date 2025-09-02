import React from "react";
import type { Product } from "../api/types";

export type CartItem = {
	product: Product;
	quantity: number;
};

export type CartState = {
	items: CartItem[];
	addToCart: (product: Product, quantity: number) => void;
	removeFromCart: (productId: number) => void;
	updateQuantity: (productId: number, quantity: number) => void;
	clearCart: () => void;
	getTotalItems: () => number;
	getTotalPrice: () => number;
};

const CartContext = React.createContext<CartState | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	const [items, setItems] = React.useState<CartItem[]>([]);

	const addToCart = (product: Product, quantity: number) => {
		setItems(currentItems => {
			const existingItem = currentItems.find(item => item.product.id === product.id);
			
			if (existingItem) {
				// Update existing item quantity
				const newQuantity = existingItem.quantity + quantity;
				if (newQuantity > product.stock) {
					throw new Error(`Sorry, only ${product.stock} items available in stock.`);
				}
				
				return currentItems.map(item =>
					item.product.id === product.id
						? { ...item, quantity: newQuantity }
						: item
				);
			} else {
				// Add new item
				if (quantity > product.stock) {
					throw new Error(`Sorry, only ${product.stock} items available in stock.`);
				}
				
				return [...currentItems, { product, quantity }];
			}
		});
	};

	const removeFromCart = (productId: number) => {
		setItems(currentItems => 
			currentItems.filter(item => item.product.id !== productId)
		);
	};

	const updateQuantity = (productId: number, quantity: number) => {
		setItems(currentItems => {
			const item = currentItems.find(item => item.product.id === productId);
			if (!item) return currentItems;
			
			if (quantity > item.product.stock) {
				throw new Error(`Sorry, only ${item.product.stock} items available in stock.`);
			}
			
			if (quantity <= 0) {
				return currentItems.filter(item => item.product.id !== productId);
			}
			
			return currentItems.map(item =>
				item.product.id === productId
					? { ...item, quantity }
					: item
			);
		});
	};

	const clearCart = () => {
		setItems([]);
	};

	const getTotalItems = () => {
		return items.reduce((total, item) => total + item.quantity, 0);
	};

	const getTotalPrice = () => {
		return items.reduce((total, item) => total + (item.product.price * item.quantity), 0);
	};

	return (
		<CartContext.Provider value={{
			items,
			addToCart,
			removeFromCart,
			updateQuantity,
			clearCart,
			getTotalItems,
			getTotalPrice
		}}>
			{children}
		</CartContext.Provider>
	);
};

export const useCart = () => {
	const ctx = React.useContext(CartContext);
	if (!ctx) throw new Error("useCart must be used within CartProvider");
	return ctx;
};
