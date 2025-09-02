import React from "react";
import { api } from "../api/client";
import { getErrorMessage } from "../utils/errorHandler";

interface ImageUploadProps {
	onImageUploaded: (imageUrl: string) => void;
	currentImageUrl?: string | null;
	className?: string;
}

export default function ImageUpload({ onImageUploaded, currentImageUrl, className }: ImageUploadProps) {
	const [uploading, setUploading] = React.useState(false);
	const [error, setError] = React.useState<string | null>(null);
	const fileInputRef = React.useRef<HTMLInputElement>(null);

	const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files?.[0];
		if (!file) return;

		// Validate file type
		const validTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"];
		if (!validTypes.includes(file.type)) {
			setError("Please select a valid image file (JPEG, PNG, GIF, or WebP)");
			return;
		}

		// Validate file size (5MB)
		if (file.size > 5 * 1024 * 1024) {
			setError("File size must be less than 5MB");
			return;
		}

		setError(null);
		setUploading(true);

		try {
			const result = await api.uploadImage(file);
			onImageUploaded(result.url);
		} catch (err) {
			setError(getErrorMessage(err));
		} finally {
			setUploading(false);
		}
	};

	const handleClick = () => {
		fileInputRef.current?.click();
	};

	const handleRemoveImage = () => {
		onImageUploaded("");
		if (fileInputRef.current) {
			fileInputRef.current.value = "";
		}
	};

	return (
		<div className={className}>
			<input
				ref={fileInputRef}
				type="file"
				accept="image/*"
				onChange={handleFileSelect}
				style={{ display: "none" }}
			/>

			{currentImageUrl ? (
				<div style={{ position: "relative", display: "inline-block" }}>
					<img
						src={currentImageUrl}
						alt="Product preview"
						style={{
							width: "150px",
							height: "150px",
							objectFit: "cover",
							borderRadius: "0.5rem",
							border: "2px solid var(--border)"
						}}
					/>
					<button
						type="button"
						onClick={handleRemoveImage}
						style={{
							position: "absolute",
							top: "-8px",
							right: "-8px",
							background: "var(--danger)",
							color: "white",
							border: "none",
							borderRadius: "50%",
							width: "24px",
							height: "24px",
							cursor: "pointer",
							display: "flex",
							alignItems: "center",
							justifyContent: "center",
							fontSize: "12px"
						}}
					>
						×
					</button>
				</div>
			) : (
				<div
					onClick={handleClick}
					style={{
						width: "150px",
						height: "150px",
						border: "2px dashed var(--border)",
						borderRadius: "0.5rem",
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
						justifyContent: "center",
						cursor: "pointer",
						transition: "border-color 0.2s",
						background: "var(--surface)"
					}}
					onMouseEnter={(e) => {
						e.currentTarget.style.borderColor = "var(--primary)";
					}}
					onMouseLeave={(e) => {
						e.currentTarget.style.borderColor = "var(--border)";
					}}
				>
					{uploading ? (
						<div style={{ textAlign: "center", color: "var(--text-muted)" }}>
							<div style={{
								width: "24px",
								height: "24px",
								border: "2px solid var(--border)",
								borderTop: "2px solid var(--primary)",
								borderRadius: "50%",
								animation: "spin 1s linear infinite",
								margin: "0 auto 0.5rem"
							}}></div>
							<p style={{ fontSize: "0.875rem" }}>Uploading...</p>
						</div>
					) : (
						<div style={{ textAlign: "center", color: "var(--text-muted)" }}>
							<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginBottom: "0.5rem" }}>
								<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
								<polyline points="7,10 12,15 17,10"/>
								<line x1="12" y1="15" x2="12" y2="3"/>
							</svg>
							<p style={{ fontSize: "0.875rem", margin: 0 }}>Click to upload</p>
							<p style={{ fontSize: "0.75rem", margin: "0.25rem 0 0 0" }}>JPG, PNG, GIF, WebP</p>
							<p style={{ fontSize: "0.75rem", margin: 0 }}>Max 5MB</p>
						</div>
					)}
				</div>
			)}

			{error && (
				<div style={{
					color: "var(--danger)",
					fontSize: "0.875rem",
					marginTop: "0.5rem"
				}}>
					{error}
				</div>
			)}
		</div>
	);
}
