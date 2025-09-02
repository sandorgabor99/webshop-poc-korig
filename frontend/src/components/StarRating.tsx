import React from 'react';

interface StarRatingProps {
	rating: number;
	onRatingChange?: (rating: number) => void;
	readonly?: boolean;
	size?: 'small' | 'medium' | 'large';
	showValue?: boolean;
}

export default function StarRating({ 
	rating, 
	onRatingChange, 
	readonly = false, 
	size = 'medium',
	showValue = false 
}: StarRatingProps) {
	const stars = [1, 2, 3, 4, 5];
	
	const sizeStyles = {
		small: { fontSize: '0.875rem' },
		medium: { fontSize: '1rem' },
		large: { fontSize: '1.125rem' }
	};
	
	const starSizeStyles = {
		small: { width: '1rem', height: '1rem' },
		medium: { width: '1.25rem', height: '1.25rem' },
		large: { width: '1.5rem', height: '1.5rem' }
	};

	const handleStarClick = (starValue: number) => {
		if (!readonly && onRatingChange) {
			onRatingChange(starValue);
		}
	};

	return (
		<div style={{ 
			display: 'flex', 
			alignItems: 'center', 
			gap: '0.25rem',
			...sizeStyles[size]
		}}>
			<div style={{ display: 'flex', alignItems: 'center' }}>
				{stars.map((star) => (
					<button
						key={star}
						type="button"
						onClick={() => handleStarClick(star)}
						disabled={readonly}
						style={{
							...starSizeStyles[size],
							background: 'none',
							border: 'none',
							cursor: readonly ? 'default' : 'pointer',
							transition: 'all 0.2s',
							color: star <= rating ? '#fbbf24' : '#d1d5db',
							fontSize: 'inherit',
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center'
						}}
						onMouseEnter={(e) => {
							if (!readonly) {
								e.currentTarget.style.transform = 'scale(1.1)';
							}
						}}
						onMouseLeave={(e) => {
							if (!readonly) {
								e.currentTarget.style.transform = 'scale(1)';
							}
						}}
					>
						{star <= rating ? '★' : '☆'}
					</button>
				))}
			</div>
			{showValue && (
				<span style={{
					marginLeft: '0.5rem',
					color: 'var(--text-muted)',
					fontWeight: '500'
				}}>
					{rating.toFixed(1)}
				</span>
			)}
		</div>
	);
}
