import { describe, it, expect, beforeEach, vi } from 'vitest'
import { api } from '../api/client'

// Mock localStorage directly in the test
const localStorageMock = {
  store: {} as Record<string, string>,
  getItem: vi.fn((key: string): string | null => localStorageMock.store[key] || null),
  setItem: vi.fn((key: string, value: string) => {
    localStorageMock.store[key] = value
  }),
  removeItem: vi.fn((key: string) => {
    delete localStorageMock.store[key]
  }),
  clear: vi.fn(() => {
    localStorageMock.store = {}
  }),
}

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
})

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorageMock.clear()
  })

  describe('Token Management', () => {
    it('should set and get token', () => {
      api.setToken('test-token')
      expect(api.getToken()).toBe('test-token')
    })

    it('should remove token when set to null', () => {
      api.setToken('test-token')
      api.setToken(null)
      expect(api.getToken()).toBeNull()
    })
  })

  describe('Login', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        access_token: 'test-token',
        token_type: 'bearer'
      }
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      } as Response)

      const result = await api.login('test@example.com', 'password')
      
      expect(result).toEqual(mockResponse)
      expect(api.getToken()).toBe('test-token')
      expect(fetch).toHaveBeenCalledWith(
        'http://test-api.com/auth/login',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })
      )
    })

    it('should handle login error', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: false,
        text: () => Promise.resolve('Invalid credentials')
      } as Response)

      await expect(api.login('test@example.com', 'wrong')).rejects.toThrow('Invalid credentials')
    })
  })

  describe('Register', () => {
    it('should register successfully', async () => {
      const mockUser = {
        id: 1,
        email: 'test@example.com',
        is_admin: false,
        created_at: '2024-01-01T00:00:00Z'
      }
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockUser)
      } as Response)

      const result = await api.register('test@example.com', 'testuser', 'password')
      
      expect(result).toEqual(mockUser)
      expect(fetch).toHaveBeenCalledWith(
        'http://test-api.com/auth/register',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ email: 'test@example.com', username: 'testuser', password: 'password' })
        })
      )
    })
  })

  describe('Products', () => {
    it('should list products', async () => {
      const mockProducts = [
        { id: 1, name: 'Product 1', price: 10.99, stock: 5 }
      ]
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockProducts)
      } as Response)

      const result = await api.listProducts()
      
      expect(result).toEqual(mockProducts)
      expect(fetch).toHaveBeenCalledWith(
        'http://test-api.com/products/',
        expect.objectContaining({
          headers: expect.any(Headers)
        })
      )
    })

    it('should create product with admin token', async () => {
      api.setToken('admin-token')
      const mockProduct = { id: 1, name: 'New Product', price: 29.99, stock: 10 }
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockProduct)
      } as Response)

      const result = await api.createProduct({
        name: 'New Product',
        price: 29.99,
        stock: 10
      })
      
      expect(result).toEqual(mockProduct)
      expect(fetch).toHaveBeenCalledWith(
        'http://test-api.com/products/',
        expect.objectContaining({
          method: 'POST',
          headers: expect.any(Headers),
          body: JSON.stringify({ name: 'New Product', price: 29.99, stock: 10 })
        })
      )
    })
  })

  describe('Orders', () => {
    it('should create order', async () => {
      api.setToken('user-token')
      const mockOrder = {
        id: 1,
        total_amount: 29.98,
        created_at: '2024-01-01T00:00:00Z',
        items: [{ product_id: 1, quantity: 2, unit_price: 14.99 }]
      }
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockOrder)
      } as Response)

      const result = await api.createOrder([
        { id: 0, product_id: 1, quantity: 2, unit_price: 14.99 }
      ])
      
      expect(result).toEqual(mockOrder)
      expect(fetch).toHaveBeenCalledWith(
        'http://test-api.com/orders/',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ 
            items: [{ id: 0, product_id: 1, quantity: 2, unit_price: 14.99 }] 
          })
        })
      )
    })
  })
})
