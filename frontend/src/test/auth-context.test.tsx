import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from './test-utils'
import { AuthProvider, useAuth } from '../context/AuthContext'
import { api } from '../api/client'

// Mock the API
vi.mock('../api/client', () => ({
  api: {
    getToken: vi.fn(),
    me: vi.fn(),
    setToken: vi.fn(),
    login: vi.fn(),
    register: vi.fn()
  }
}))

const TestComponent = () => {
  const { user, loading, login, register, logout } = useAuth()
  
  return (
    <div>
      <div data-testid="loading">{loading.toString()}</div>
      <div data-testid="user">{user ? user.email : 'no-user'}</div>
      <button onClick={() => login('test@example.com', 'password')}>Login</button>
      <button onClick={() => register('test@example.com', 'testuser', 'password')}>Register</button>
      <button onClick={logout}>Logout</button>
    </div>
  )
}

describe('AuthContext', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should initialize and finish loading', async () => {
    vi.mocked(api.getToken).mockReturnValue(null)
    
    render(<TestComponent />)
    
    expect(api.getToken).toHaveBeenCalled()
    
    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('false')
    })
    
    expect(screen.getByTestId('user')).toHaveTextContent('no-user')
  })

  it('should load user if token exists', async () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      username: 'testuser',
      role: 'CUSTOMER' as const,
      is_admin: false,
      created_at: '2024-01-01T00:00:00Z'
    }
    
    vi.mocked(api.getToken).mockReturnValue('valid-token')
    vi.mocked(api.me).mockResolvedValue(mockUser)
    
    render(<TestComponent />)
    
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('false')
    })
    
    expect(screen.getByTestId('user')).toHaveTextContent('test@example.com')
  })

  it('should handle login', async () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      username: 'testuser',
      role: 'CUSTOMER' as const,
      is_admin: false,
      created_at: '2024-01-01T00:00:00Z'
    }
    
    vi.mocked(api.getToken).mockReturnValue(null)
    vi.mocked(api.login).mockResolvedValue({ access_token: 'token', token_type: 'bearer' })
    vi.mocked(api.me).mockResolvedValue(mockUser)
    
    render(<TestComponent />)
    
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('false')
    })
    
    const loginButton = screen.getByText('Login')
    loginButton.click()
    
    await waitFor(() => {
      expect(api.login).toHaveBeenCalledWith('test@example.com', 'password')
    })
  })

  it('should handle register', async () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      username: 'testuser',
      role: 'CUSTOMER' as const,
      is_admin: false,
      created_at: '2024-01-01T00:00:00Z'
    }
    
    vi.mocked(api.getToken).mockReturnValue(null)
    vi.mocked(api.register).mockResolvedValue(mockUser)
    vi.mocked(api.login).mockResolvedValue({ access_token: 'token', token_type: 'bearer' })
    vi.mocked(api.me).mockResolvedValue(mockUser)
    
    render(<TestComponent />)
    
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('false')
    })
    
    const registerButton = screen.getByText('Register')
    registerButton.click()
    
    await waitFor(() => {
      expect(api.register).toHaveBeenCalledWith('test@example.com', 'testuser', 'password')
    })
  })

  it('should handle logout', async () => {
    vi.mocked(api.getToken).mockReturnValue(null)
    
    render(<TestComponent />)
    
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('false')
    })
    
    const logoutButton = screen.getByText('Logout')
    logoutButton.click()
    
    expect(api.setToken).toHaveBeenCalledWith(null)
  })

  it('should handle API errors gracefully', async () => {
    vi.mocked(api.getToken).mockReturnValue('invalid-token')
    vi.mocked(api.me).mockRejectedValue(new Error('Invalid token'))
    
    render(<TestComponent />)
    
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('false')
    })
    
    expect(api.setToken).toHaveBeenCalledWith(null)
    expect(screen.getByTestId('user')).toHaveTextContent('no-user')
  })
})
