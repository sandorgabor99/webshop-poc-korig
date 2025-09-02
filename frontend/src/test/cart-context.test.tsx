import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from './test-utils'
import { CartProvider, useCart } from '../context/CartContext'

const TestComponent = () => {
  const { items, addToCart, removeFromCart, updateQuantity, clearCart, getTotalItems, getTotalPrice } = useCart()
  
  const mockProduct = {
    id: 1,
    name: 'Test Product',
    description: 'A test product',
    price: 29.99,
    stock: 10,
    created_at: '2024-01-01T00:00:00Z',
    average_rating: 4.5,
    review_count: 10
  }
  
  return (
    <div>
      <div data-testid="total-items">{getTotalItems()}</div>
      <div data-testid="total-price">{getTotalPrice().toFixed(2)}</div>
      <div data-testid="items-count">{items.length}</div>
      <button onClick={() => addToCart(mockProduct, 1)}>Add to Cart</button>
      <button onClick={() => addToCart(mockProduct, 2)}>Add 2 to Cart</button>
      <button onClick={() => removeFromCart(1)}>Remove from Cart</button>
      <button onClick={() => updateQuantity(1, 3)}>Update Quantity</button>
      <button onClick={clearCart}>Clear Cart</button>
      {items.map(item => (
        <div key={item.product.id} data-testid={`item-${item.product.id}`}>
          {item.product.name} - Qty: {item.quantity}
        </div>
      ))}
    </div>
  )
}

describe('CartContext', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should initialize with empty cart', () => {
    render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    )
    
    expect(screen.getByTestId('total-items')).toHaveTextContent('0')
    expect(screen.getByTestId('total-price')).toHaveTextContent('0.00')
    expect(screen.getByTestId('items-count')).toHaveTextContent('0')
  })

  it('should add item to cart', () => {
    render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    )
    
    fireEvent.click(screen.getByText('Add to Cart'))
    
    expect(screen.getByTestId('total-items')).toHaveTextContent('1')
    expect(screen.getByTestId('total-price')).toHaveTextContent('29.99')
    expect(screen.getByTestId('items-count')).toHaveTextContent('1')
    expect(screen.getByTestId('item-1')).toHaveTextContent('Test Product - Qty: 1')
  })

  it('should update quantity when adding same item', () => {
    render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    )
    
    fireEvent.click(screen.getByText('Add to Cart'))
    fireEvent.click(screen.getByText('Add to Cart'))
    
    expect(screen.getByTestId('total-items')).toHaveTextContent('2')
    expect(screen.getByTestId('total-price')).toHaveTextContent('59.98')
    expect(screen.getByTestId('items-count')).toHaveTextContent('1')
    expect(screen.getByTestId('item-1')).toHaveTextContent('Test Product - Qty: 2')
  })

  it('should remove item from cart', () => {
    render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    )
    
    fireEvent.click(screen.getByText('Add to Cart'))
    fireEvent.click(screen.getByText('Remove from Cart'))
    
    expect(screen.getByTestId('total-items')).toHaveTextContent('0')
    expect(screen.getByTestId('total-price')).toHaveTextContent('0.00')
    expect(screen.getByTestId('items-count')).toHaveTextContent('0')
    expect(screen.queryByTestId('item-1')).not.toBeInTheDocument()
  })

  it('should update quantity', () => {
    render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    )
    
    fireEvent.click(screen.getByText('Add to Cart'))
    fireEvent.click(screen.getByText('Update Quantity'))
    
    expect(screen.getByTestId('total-items')).toHaveTextContent('3')
    expect(screen.getByTestId('total-price')).toHaveTextContent('89.97')
    expect(screen.getByTestId('item-1')).toHaveTextContent('Test Product - Qty: 3')
  })

  it('should clear cart', () => {
    render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    )
    
    fireEvent.click(screen.getByText('Add to Cart'))
    fireEvent.click(screen.getByText('Clear Cart'))
    
    expect(screen.getByTestId('total-items')).toHaveTextContent('0')
    expect(screen.getByTestId('total-price')).toHaveTextContent('0.00')
    expect(screen.getByTestId('items-count')).toHaveTextContent('0')
    expect(screen.queryByTestId('item-1')).not.toBeInTheDocument()
  })
})
