import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from './test-utils'
import Login from '../pages/Login'
import Register from '../pages/Register'
import Products from '../pages/Products'
import { api } from '../api/client'

// Mock the API
vi.mock('../api/client', () => ({
  api: {
    login: vi.fn(),
    register: vi.fn(),
    listProducts: vi.fn(),
    setToken: vi.fn(),
    getToken: vi.fn(),
    me: vi.fn()
  }
}))

// Mock react-router-dom
const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate
  }
})

// Mock AuthContext
const mockLogin = vi.fn()
const mockRegister = vi.fn()
const mockLogout = vi.fn()

vi.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    user: null,
    loading: false,
    login: mockLogin,
    register: mockRegister,
    logout: mockLogout
  }),
  AuthProvider: ({ children }: { children: React.ReactNode }) => children
}))

// Mock CartContext
const mockAddToCart = vi.fn()
vi.mock('../context/CartContext', () => ({
  useCart: () => ({
    items: [],
    addToCart: mockAddToCart,
    removeFromCart: vi.fn(),
    updateQuantity: vi.fn(),
    clearCart: vi.fn(),
    getTotalItems: () => 0,
    getTotalPrice: () => 0
  }),
  CartProvider: ({ children }: { children: React.ReactNode }) => children
}))

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render login form', () => {
    render(<Login />)
    
    expect(screen.getByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
    expect(screen.getByLabelText('Email')).toBeInTheDocument()
    expect(screen.getByLabelText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeInTheDocument()
  })

  it('should handle successful login', async () => {
    mockLogin.mockResolvedValue(undefined)
    
    render(<Login />)
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))
    
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123')
      expect(mockNavigate).toHaveBeenCalledWith('/')
    })
  })

  it('should handle login error', async () => {
    mockLogin.mockRejectedValue(new Error('Invalid credentials'))
    
    render(<Login />)
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'wrongpassword' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))
    
    await waitFor(() => {
      expect(screen.getByText('Invalid email or password. Please try again.')).toBeInTheDocument()
    })
  })

  it('should show field validation errors', async () => {
    render(<Login />)
    
    // Try to submit without filling required fields
    const form = screen.getByRole('button', { name: 'Sign in' }).closest('form')
    fireEvent.submit(form!)
    
    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument()
      expect(screen.getByText('Password is required')).toBeInTheDocument()
    })
  })

  it('should validate email format', async () => {
    render(<Login />)
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'invalid-email' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' }
    })
    
    const form = screen.getByRole('button', { name: 'Sign in' }).closest('form')
    fireEvent.submit(form!)
    
    await waitFor(() => {
      expect(screen.getByText('Please enter a valid email address')).toBeInTheDocument()
    })
  })

  it('should validate password length', async () => {
    render(<Login />)
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: '123' }
    })
    
    const form = screen.getByRole('button', { name: 'Sign in' }).closest('form')
    fireEvent.submit(form!)
    
    await waitFor(() => {
      expect(screen.getByText('Password must be at least 6 characters')).toBeInTheDocument()
    })
  })

  it('should clear password field on login failure', async () => {
    mockLogin.mockRejectedValue(new Error('Invalid credentials'))
    
    render(<Login />)
    
    const passwordInput = screen.getByLabelText('Password')
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(passwordInput, {
      target: { value: 'wrongpassword' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))
    
    await waitFor(() => {
      expect(passwordInput).toHaveValue('')
    })
  })

  it('should clear field errors when user starts typing', async () => {
    render(<Login />)
    
    // Trigger validation errors
    const form = screen.getByRole('button', { name: 'Sign in' }).closest('form')
    fireEvent.submit(form!)
    
    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument()
    })
    
    // Start typing in email field
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    
    await waitFor(() => {
      expect(screen.queryByText('Email is required')).not.toBeInTheDocument()
    })
  })

  it('should show loading state during login', async () => {
    mockLogin.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))
    
    render(<Login />)
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))
    
    expect(screen.getByText('Signing in...')).toBeInTheDocument()
  })
})

describe('Register Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render register form', () => {
    render(<Register />)
    
    expect(screen.getByRole('heading', { name: 'Create account' })).toBeInTheDocument()
    expect(screen.getByLabelText('Username')).toBeInTheDocument()
    expect(screen.getByLabelText('Email')).toBeInTheDocument()
    expect(screen.getByLabelText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Create account' })).toBeInTheDocument()
  })

  it('should handle successful registration', async () => {
    mockRegister.mockResolvedValue(undefined)
    
    render(<Register />)
    
    fireEvent.change(screen.getByLabelText('Username'), {
      target: { value: 'testuser' }
    })
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' }
    })
    
    fireEvent.click(screen.getByRole('button', { name: 'Create account' }))
    
    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith('test@example.com', 'testuser', 'password123')
      expect(mockNavigate).toHaveBeenCalledWith('/')
    })
  })
})

describe('Products Page', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should show loading state initially', () => {
    vi.mocked(api.listProducts).mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))
    
    render(<Products />)
    
    expect(screen.getByTestId('loading')).toBeInTheDocument()
  })

  it('should display products when loaded', async () => {
    const mockProducts = [
      {
        id: 1,
        name: 'Test Product',
        description: 'A test product',
        price: 29.99,
        stock: 10,
        created_at: '2024-01-01T00:00:00Z',
        average_rating: 4.5,
        review_count: 10
      }
    ]
    vi.mocked(api.listProducts).mockResolvedValue(mockProducts)
    
    render(<Products />)
    
    await waitFor(() => {
      expect(screen.getByText('Test Product')).toBeInTheDocument()
      expect(screen.getByText('$29.99')).toBeInTheDocument()
      expect(screen.getByText('10 in stock')).toBeInTheDocument()
    })
  })

  it('should show empty state when no products', async () => {
    vi.mocked(api.listProducts).mockResolvedValue([])
    
    render(<Products />)
    
    await waitFor(() => {
      expect(screen.getByText('No products available.')).toBeInTheDocument()
    })
  })
})
