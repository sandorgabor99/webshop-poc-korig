import React, { useState } from 'react';
import StarRating from './StarRating';
import { api } from '../api/client';
import type { ReviewCreate } from '../api/types';

interface ReviewFormProps {
	productId: number;
	onReviewSubmitted: () => void;
	onCancel: () => void;
}

export default function ReviewForm({ productId, onReviewSubmitted, onCancel }: ReviewFormProps) {
	const [rating, setRating] = useState(0);
	const [feedback, setFeedback] = useState('');
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [error, setError] = useState('');

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		
		if (rating === 0) {
			setError('Please select a rating');
			return;
		}

		setIsSubmitting(true);
		setError('');

		try {
			const reviewData: ReviewCreate = {
				product_id: productId,
				rating,
				feedback: feedback.trim() || undefined
			};

			await api.createReview(reviewData);
			onReviewSubmitted();
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to submit review');
		} finally {
			setIsSubmitting(false);
		}
	};

	return (
		<div style={{
			background: 'white',
			padding: '1.5rem',
			borderRadius: '0.5rem',
			border: '1px solid var(--border)',
			boxShadow: 'var(--shadow)'
		}}>
			<h3 style={{
				fontSize: '1.125rem',
				fontWeight: '600',
				marginBottom: '1rem',
				color: 'var(--text)'
			}}>
				Write a Review
			</h3>
			
			<form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
				<div>
					<label style={{
						display: 'block',
						fontSize: '0.875rem',
						fontWeight: '500',
						color: 'var(--text)',
						marginBottom: '0.5rem'
					}}>
						Rating *
					</label>
					<StarRating 
						rating={rating} 
						onRatingChange={setRating}
						size="large"
						showValue={true}
					/>
				</div>

				<div>
					<label htmlFor="feedback" style={{
						display: 'block',
						fontSize: '0.875rem',
						fontWeight: '500',
						color: 'var(--text)',
						marginBottom: '0.5rem'
					}}>
						Feedback (optional)
					</label>
					<textarea
						id="feedback"
						value={feedback}
						onChange={(e) => setFeedback(e.target.value)}
						rows={4}
						maxLength={1000}
						placeholder="Share your thoughts about this product..."
						style={{
							width: '100%',
							padding: '0.75rem',
							border: '1px solid var(--border)',
							borderRadius: '0.5rem',
							fontSize: '1rem',
							fontFamily: 'inherit',
							resize: 'vertical'
						}}
					/>
					<div style={{
						fontSize: '0.75rem',
						color: 'var(--text-muted)',
						marginTop: '0.25rem'
					}}>
						{feedback.length}/1000 characters
					</div>
				</div>

				{error && (
					<div style={{
						color: 'var(--danger)',
						fontSize: '0.875rem',
						background: 'rgb(239 68 68 / 0.1)',
						padding: '0.75rem',
						borderRadius: '0.5rem',
						border: '1px solid var(--danger)'
					}}>
						{error}
					</div>
				)}

				<div style={{ display: 'flex', gap: '0.75rem' }}>
					<button
						type="submit"
						disabled={isSubmitting || rating === 0}
						style={{
							flex: 1,
							background: rating === 0 || isSubmitting ? 'var(--text-muted)' : 'var(--primary)',
							color: 'white',
							padding: '0.75rem 1rem',
							borderRadius: '0.5rem',
							border: 'none',
							fontSize: '1rem',
							fontWeight: '500',
							cursor: rating === 0 || isSubmitting ? 'not-allowed' : 'pointer',
							opacity: rating === 0 || isSubmitting ? 0.5 : 1,
							transition: 'all 0.2s'
						}}
					>
						{isSubmitting ? 'Submitting...' : 'Submit Review'}
					</button>
					<button
						type="button"
						onClick={onCancel}
						disabled={isSubmitting}
						style={{
							flex: 1,
							background: 'white',
							color: 'var(--text)',
							padding: '0.75rem 1rem',
							borderRadius: '0.5rem',
							border: '1px solid var(--border)',
							fontSize: '1rem',
							fontWeight: '500',
							cursor: isSubmitting ? 'not-allowed' : 'pointer',
							opacity: isSubmitting ? 0.5 : 1,
							transition: 'all 0.2s'
						}}
					>
						Cancel
					</button>
				</div>
			</form>
		</div>
	);
}
