import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock localStorage with actual storage functionality
const store: Record<string, string> = {}

const localStorageMock = {
  getItem: vi.fn((key: string) => store[key] || null),
  setItem: vi.fn((key: string, value: string) => {
    store[key] = value
  }),
  removeItem: vi.fn((key: string) => {
    delete store[key]
  }),
  clear: vi.fn(() => {
    Object.keys(store).forEach(key => delete store[key])
  }),
}

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
})

// Mock fetch
Object.defineProperty(window, 'fetch', {
  value: vi.fn(),
  writable: true
})

// Mock environment variables
import.meta.env.VITE_API_BASE = 'http://test-api.com'
