import React from "react";
import { api } from "../api/client";
import { getErrorMessage } from "../utils/errorHandler";
import type { Product, ProductCreate } from "../api/types";
import ImageUpload from "../components/ImageUpload";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

export default function AdminProducts() {
	const [products, setProducts] = React.useState<Product[]>([]);
	const [form, setForm] = React.useState<ProductCreate>({ name: "", description: "", price: 0, stock: 0, image_url: "" });
	const [loading, setLoading] = React.useState(true);
	const [error, setError] = React.useState<string | null>(null);

	const load = async () => {
		setLoading(true);
		try {
			setProducts(await api.listProducts());
		} catch (err) {
			setError(getErrorMessage(err));
		} finally {
			setLoading(false);
		}
	};

	React.useEffect(() => { load(); }, []);

	const create = async (e: React.FormEvent) => {
		e.preventDefault();
		setError(null);
		try {
			await api.createProduct(form);
			setForm({ name: "", description: "", price: 0, stock: 0, image_url: "" });
			await load();
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	const update = async (id: number, field: keyof Product, value: any) => {
		try {
			await api.updateProduct(id, { [field]: value } as any);
			await load();
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	const remove = async (id: number) => {
		try {
			await api.deleteProduct(id);
			await load();
		} catch (err) {
			setError(getErrorMessage(err));
		}
	};

	return (
		<div>
			<div className="flex justify-between items-center mb-6">
				<div>
					<h1 className="text-2xl font-bold mb-2">
						Product Management
					</h1>
					<p className="text-muted">
						Create, edit, and manage your products
					</p>
				</div>
			</div>

			{error && (
				<div className="alert alert-error mb-4">
					{error}
				</div>
			)}

			<div className="card mb-6">
				<div className="card-header">
					<h2 className="card-title">Create New Product</h2>
				</div>
				<form onSubmit={create} className="grid gap-4">
					<div className="form-group">
						<label className="form-label">Product Name</label>
						<input 
							className="form-input"
							placeholder="Enter product name" 
							value={form.name} 
							onChange={(e) => setForm({ ...form, name: e.target.value })} 
							required 
						/>
					</div>
					<div className="form-group">
						<label className="form-label">Description</label>
						<textarea 
							className="form-input form-textarea"
							placeholder="Enter product description" 
							value={form.description} 
							onChange={(e) => setForm({ ...form, description: e.target.value })}
						/>
					</div>
					<div className="grid grid-cols-2 gap-4">
						<div className="form-group">
							<label className="form-label">Price ($)</label>
							<input 
								className="form-input"
								type="number" 
								step="0.01" 
								min="0"
								placeholder="0.00" 
								value={form.price} 
								onChange={(e) => setForm({ ...form, price: parseFloat(e.target.value) || 0 })} 
								required 
							/>
						</div>
						<div className="form-group">
							<label className="form-label">Stock Quantity</label>
							<input 
								className="form-input"
								type="number" 
								min="0"
								placeholder="0" 
								value={form.stock} 
								onChange={(e) => setForm({ ...form, stock: parseInt(e.target.value) || 0 })} 
								required 
							/>
						</div>
					</div>
					<div className="form-group">
						<label className="form-label">Product Image</label>
						<ImageUpload
							onImageUploaded={(imageUrl) => setForm({ ...form, image_url: imageUrl })}
							currentImageUrl={form.image_url || null}
						/>
					</div>
					<button type="submit" className="btn btn-primary">
						Create Product
					</button>
				</form>
			</div>

			<div className="card">
				<div className="card-header">
					<h2 className="card-title">Manage Products</h2>
				</div>

				{loading ? (
					<div className="loading">
						<div className="spinner"></div>
						<p className="text-muted">Loading products...</p>
					</div>
				) : products.length === 0 ? (
					<div className="text-center p-6">
						<p className="text-muted">No products found. Create your first product above.</p>
					</div>
				) : (
					<div className="overflow-x-auto">
						<table className="admin-table">
							<thead>
								<tr>
									<th>Image</th>
									<th>Name</th>
									<th>Description</th>
									<th>Price</th>
									<th>Stock</th>
									<th>Actions</th>
								</tr>
							</thead>
							<tbody>
								{products.map((p) => (
									<tr key={p.id}>
										<td>
											{p.image_url ? (
												<img
													src={p.image_url.startsWith('http') ? p.image_url : `${API_BASE}${p.image_url}`}
													alt={p.name}
													className="product-thumb"
												/>
											) : (
												<div className="product-thumb-placeholder">
													No image
												</div>
											)}
										</td>
										<td className="font-medium">{p.name}</td>
										<td className="text-muted">
											{p.description || "No description"}
										</td>
										<td>
											<input 
												className="form-input w-20"
												type="number" 
												step="0.01" 
												min="0"
												defaultValue={p.price} 
												onBlur={(e) => update(p.id, "price", parseFloat(e.target.value) || 0)}
											/>
										</td>
										<td>
											<input 
												className="form-input w-20"
												type="number" 
												min="0"
												defaultValue={p.stock} 
												onBlur={(e) => update(p.id, "stock", parseInt(e.target.value) || 0)}
											/>
										</td>
										<td>
											<div className="flex gap-2">
												<button 
													onClick={() => {
														// TODO: Add image editing modal
														alert("Image editing feature coming soon!");
													}}
													className="btn btn-secondary btn-sm"
												>
													Edit Image
												</button>
												<button 
													onClick={() => remove(p.id)}
													className="btn btn-danger btn-sm"
												>
													Delete
												</button>
											</div>
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				)}
			</div>
		</div>
	);
}
