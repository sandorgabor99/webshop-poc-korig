import React from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import { getErrorMessage } from "../utils/errorHandler";

export default function Login() {
	const { login } = useAuth();
	const nav = useNavigate();
	const [email, setEmail] = React.useState("");
	const [password, setPassword] = React.useState("");
	const [error, setError] = React.useState<string | null>(null);
	const [loading, setLoading] = React.useState(false);
	const [fieldErrors, setFieldErrors] = React.useState<{
		email?: string;
		password?: string;
	}>({});

	const validateForm = () => {
		const errors: { email?: string; password?: string } = {};
		
		if (!email.trim()) {
			errors.email = "Email is required";
		} else if (!/\S+@\S+\.\S+/.test(email)) {
			errors.email = "Please enter a valid email address";
		}
		
		if (!password) {
			errors.password = "Password is required";
		} else if (password.length < 6) {
			errors.password = "Password must be at least 6 characters";
		}
		
		setFieldErrors(errors);
		return Object.keys(errors).length === 0;
	};

	const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setEmail(e.target.value);
		if (fieldErrors.email) {
			setFieldErrors(prev => ({ ...prev, email: undefined }));
		}
		setError(null);
	};

	const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setPassword(e.target.value);
		if (fieldErrors.password) {
			setFieldErrors(prev => ({ ...prev, password: undefined }));
		}
		setError(null);
	};

	const onSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError(null);
		setFieldErrors({});
		
		if (!validateForm()) {
			return;
		}
		
		setLoading(true);
		try {
			await login(email, password);
			nav("/");
		} catch (err: any) {
			setError(getErrorMessage(err));
			// Clear password field on login failure for security
			setPassword("");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="auth-container">
			<div className="auth-card">
				<div className="auth-header">
					<h1 className="auth-title">Welcome back</h1>
					<p className="auth-subtitle">Sign in to your account</p>
				</div>

				<form onSubmit={onSubmit} className="auth-form">
					<div className="form-group">
						<label htmlFor="email" className="form-label">Email</label>
						<input
							id="email"
							type="email"
							value={email}
							onChange={handleEmailChange}
							required
							className={`form-input ${fieldErrors.email ? 'form-input-error' : ''}`}
							placeholder="Enter your email"
						/>
						{fieldErrors.email && (
							<div className="form-error">
								{fieldErrors.email}
							</div>
						)}
					</div>

					<div className="form-group">
						<label htmlFor="password" className="form-label">Password</label>
						<input
							id="password"
							type="password"
							value={password}
							onChange={handlePasswordChange}
							required
							className={`form-input ${fieldErrors.password ? 'form-input-error' : ''}`}
							placeholder="Enter your password"
						/>
						{fieldErrors.password && (
							<div className="form-error">
								{fieldErrors.password}
							</div>
						)}
						<div className="text-right mt-2">
							<Link to="/forgot-password" className="auth-link text-sm">
								Forgot password?
							</Link>
						</div>
					</div>

					{error && (
						<div className="alert alert-error" id="login-error" role="alert" aria-live="polite">
							{error}
						</div>
					)}

					<button
						type="submit"
						disabled={loading}
						className={`btn btn-primary w-full mt-4 ${loading ? 'btn-loading' : ''}`}
						aria-describedby={error ? "login-error" : undefined}
					>
						{loading ? "Signing in..." : "Sign in"}
					</button>
				</form>

				<div className="auth-footer">
					<p className="text-sm text-muted">
						Don't have an account?{" "}
						<Link to="/register" className="auth-link font-medium">
							Sign up
						</Link>
					</p>
				</div>
			</div>
		</div>
	);
}
