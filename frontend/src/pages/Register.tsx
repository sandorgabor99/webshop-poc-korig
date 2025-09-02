import React from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import { getErrorMessage } from "../utils/errorHandler";

export default function Register() {
	const { register } = useAuth();
	const nav = useNavigate();
	const [email, setEmail] = React.useState("");
	const [username, setUsername] = React.useState("");
	const [password, setPassword] = React.useState("");
	const [error, setError] = React.useState<string | null>(null);
	const [loading, setLoading] = React.useState(false);

	const onSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError(null);
		setLoading(true);
		try {
			await register(email, username, password);
			nav("/");
		} catch (err: any) {
			setError(getErrorMessage(err));
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="auth-container">
			<div className="auth-card">
				<div className="auth-header">
					<h1 className="auth-title">Create account</h1>
					<p className="auth-subtitle">Join our webshop community</p>
				</div>

				<form onSubmit={onSubmit} className="auth-form">
					<div className="form-group">
						<label htmlFor="username" className="form-label">Username</label>
						<input
							id="username"
							type="text"
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							required
							minLength={3}
							maxLength={50}
							className="form-input"
							placeholder="Choose a username (3-50 characters)"
						/>
					</div>

					<div className="form-group">
						<label htmlFor="email" className="form-label">Email</label>
						<input
							id="email"
							type="email"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
							required
							className="form-input"
							placeholder="Enter your email"
						/>
					</div>

					<div className="form-group">
						<label htmlFor="password" className="form-label">Password</label>
						<input
							id="password"
							type="password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							required
							className="form-input"
							placeholder="Create a password"
						/>
					</div>

					{error && (
						<div className="alert alert-error">
							{error}
						</div>
					)}

					<button
						type="submit"
						disabled={loading}
						className={`btn btn-primary w-full mt-4 ${loading ? 'btn-loading' : ''}`}
					>
						{loading ? "Creating account..." : "Create account"}
					</button>
				</form>

				<div className="auth-footer">
					<p className="text-sm text-muted">
						Already have an account?{" "}
						<Link to="/login" className="auth-link font-medium">
							Sign in
						</Link>
					</p>
				</div>
			</div>
		</div>
	);
}
