import StarRating from './StarRating';
import type { Review } from '../api/types';

interface ReviewListProps {
	reviews: Review[];
	onReviewDeleted?: (reviewId: number) => void;
	currentUserId?: number;
}

export default function ReviewList({ reviews, onReviewDeleted, currentUserId }: ReviewListProps) {
	const handleDeleteReview = async (reviewId: number) => {
		if (onReviewDeleted) {
			onReviewDeleted(reviewId);
		}
	};

	if (reviews.length === 0) {
		return (
			<div style={{
				textAlign: 'center',
				padding: '2rem',
				color: 'var(--text-muted)'
			}}>
				<p>No reviews yet. Be the first to review this product!</p>
			</div>
		);
	}

	return (
		<div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
			{reviews.map((review) => (
				<div key={review.id} style={{
					background: 'white',
					padding: '1rem',
					borderRadius: '0.5rem',
					border: '1px solid var(--border)'
				}}>
					<div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
						<div style={{ flex: 1 }}>
							<div style={{
								display: 'flex',
								alignItems: 'center',
								gap: '0.75rem',
								marginBottom: '0.5rem'
							}}>
								<StarRating 
									rating={review.rating} 
									readonly 
									size="small"
								/>
								<span style={{
									fontSize: '0.875rem',
									color: 'var(--text-muted)'
								}}>
									by {review.user.username}
								</span>
								<span style={{
									fontSize: '0.75rem',
									color: 'var(--text-muted)'
								}}>
									{new Date(review.created_at).toLocaleDateString()}
								</span>
							</div>
							
							{review.feedback && (
								<p style={{
									color: 'var(--text)',
									fontSize: '0.875rem',
									lineHeight: '1.6'
								}}>
									{review.feedback}
								</p>
							)}
						</div>
						
						{currentUserId === review.user_id && onReviewDeleted && (
							<button
								onClick={() => handleDeleteReview(review.id)}
								style={{
									color: 'var(--danger)',
									fontSize: '0.875rem',
									fontWeight: '500',
									background: 'none',
									border: 'none',
									cursor: 'pointer',
									marginLeft: '1rem'
								}}
								onMouseEnter={(e) => {
									e.currentTarget.style.color = '#dc2626';
								}}
								onMouseLeave={(e) => {
									e.currentTarget.style.color = 'var(--danger)';
								}}
							>
								Delete
							</button>
						)}
					</div>
				</div>
			))}
		</div>
	);
}
