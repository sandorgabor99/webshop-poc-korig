# Frontend Architecture Documentation

## Technology Stack

### Core Framework
- **React 18.2.0**: Modern React with concurrent features
- **TypeScript 5.2.2**: Type-safe JavaScript development
- **Vite 5.1.0**: Fast build tool and development server

### State Management
- **React Context API**: Global state management
- **Custom Hooks**: Reusable state logic
- **Local Storage**: Persistent client-side data

### Routing & Navigation
- **React Router DOM 6.22.0**: Client-side routing
- **Protected Routes**: Role-based access control
- **Dynamic Navigation**: Context-aware menu system

### UI Components & Styling
- **Custom CSS Framework**: Tailwind-inspired utility classes
- **Responsive Design**: Mobile-first approach
- **Component Library**: Reusable UI components

### Data Visualization
- **Chart.js 4.5.0**: Interactive charts and graphs
- **React Chart.js 2**: React wrapper for Chart.js
- **Google Charts**: Additional charting capabilities

### Development Tools
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **TypeScript ESLint**: TypeScript-specific linting rules

## Architecture Patterns

### 1. Component Architecture
```
App (Root Component)
├── Navigation (Header)
├── Routes
│   ├── Products (Public)
│   ├── ProductDetail (Public)
│   ├── Cart (Customer)
│   ├── Checkout (Customer)
│   ├── OrderHistory (Customer)
│   ├── Login/Register (Public)
│   └── Admin Routes
│       ├── ProductManagement
│       ├── OrderManagement
│       ├── CustomerManagement
│       └── Analytics
└── Context Providers
    ├── AuthContext
    └── CartContext
```

### 2. State Management Strategy
```typescript
// Auth Context
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Cart Context
interface CartContextType {
  items: CartItem[];
  addItem: (product: Product, quantity: number) => void;
  removeItem: (productId: number) => void;
  clearCart: () => void;
  getTotalItems: () => number;
  getTotalPrice: () => number;
}
```

### 3. Routing Strategy
- **Public Routes**: Products, product details, authentication
- **Protected Routes**: Customer-specific features (cart, orders)
- **Admin Routes**: Administrative functions (management, analytics)
- **Route Guards**: Authentication and role-based access control

## Core Components

### 1. Authentication System
```typescript
const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  
  const login = async (email: string, password: string) => {
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      setUser(data.user);
      localStorage.setItem('token', data.access_token);
    }
  };
  
  return { user, login, logout, isAuthenticated: !!user };
};
```

### 2. Product Management
- **Product Listing**: Grid layout with search and filtering
- **Product Details**: Rich product information with reviews
- **Admin Interface**: CRUD operations for products
- **Image Management**: Upload, preview, and deletion

### 3. Shopping Cart System
```typescript
const useCart = () => {
  const [items, setItems] = useState<CartItem[]>([]);
  
  const addItem = (product: Product, quantity: number) => {
    setItems(prev => {
      const existing = prev.find(item => item.product.id === product.id);
      if (existing) {
        return prev.map(item => 
          item.product.id === product.id 
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [...prev, { product, quantity }];
    });
  };
  
  return { items, addItem, removeItem, clearCart, getTotalItems, getTotalPrice };
};
```

### 4. Order Management
- **Order Creation**: Multi-step checkout process
- **Order History**: Customer order tracking
- **Admin Order Management**: Full order lifecycle management
- **Order Analytics**: Business intelligence and reporting

### 5. Analytics Dashboard
```typescript
const Statistics = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  
  useEffect(() => {
    fetchAnalytics();
  }, []);
  
  return (
    <div className="analytics-dashboard">
      <div className="stats-grid">
        <StatCard title="Total Sales" value={analytics?.totalSales} />
        <StatCard title="Orders" value={analytics?.totalOrders} />
        <StatCard title="Customers" value={analytics?.totalCustomers} />
        <StatCard title="Products" value={analytics?.totalProducts} />
      </div>
      <div className="charts-section">
        <SalesChart data={analytics?.salesData} />
        <OrderTrendsChart data={analytics?.orderTrends} />
      </div>
    </div>
  );
};
```

## Performance Optimizations

### 1. Code Splitting
- **Route-based Splitting**: Lazy loading of route components
- **Component Splitting**: On-demand component loading
- **Bundle Optimization**: Tree shaking and dead code elimination

### 2. State Optimization
- **Memoization**: React.memo for expensive components
- **Callback Optimization**: useCallback for stable references
- **State Batching**: Efficient state updates

### 3. Image Optimization
- **Lazy Loading**: Progressive image loading
- **Responsive Images**: Multiple resolution support
- **Compression**: Optimized image formats

## Component Library

### 1. UI Components
- **Button**: Primary, secondary, outline variants
- **Input**: Text, email, password, number inputs
- **Modal**: Overlay dialogs and forms
- **Table**: Data display with sorting and pagination
- **Card**: Content containers with headers and actions

### 2. Layout Components
- **Container**: Responsive content wrapper
- **Grid**: Flexible grid system
- **Flexbox**: Utility classes for flexbox layouts
- **Spacing**: Consistent margin and padding system

### 3. Form Components
- **Form**: Form wrapper with validation
- **Field**: Form field with label and error handling
- **Select**: Dropdown selection component
- **Checkbox**: Boolean input component
- **Radio**: Single choice selection

## Styling System

### 1. CSS Architecture
- **Utility-First**: Tailwind-inspired utility classes
- **Component-Based**: Scoped component styles
- **Responsive Design**: Mobile-first approach
- **Theme System**: Consistent color and spacing

### 2. Design Tokens
```css
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Typography */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
}
```

### 3. Responsive Breakpoints
```css
/* Mobile First */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

## Data Management

### 1. API Integration
- **Fetch API**: Modern HTTP client
- **Error Handling**: Consistent error management
- **Loading States**: User feedback during requests
- **Retry Logic**: Automatic retry on failures

### 2. State Persistence
- **Local Storage**: Persistent client-side data
- **Session Storage**: Temporary session data
- **Cookies**: Authentication tokens
- **IndexedDB**: Large data storage (future)

### 3. Caching Strategy
- **API Response Caching**: Cache frequently accessed data
- **Image Caching**: Browser image caching
- **Component Caching**: Memoized component rendering
- **Route Caching**: Cached route components

## Error Handling

### 1. Error Boundaries
```typescript
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### 2. Error Types
- **Network Errors**: API request failures
- **Validation Errors**: Form input validation
- **Authentication Errors**: Token expiration
- **Permission Errors**: Insufficient access rights

### 3. User Feedback
- **Toast Notifications**: Success and error messages
- **Inline Validation**: Real-time form validation
- **Loading Indicators**: Request progress feedback
- **Error Pages**: Graceful error handling

## Accessibility

### 1. ARIA Support
- **Semantic HTML**: Proper HTML structure
- **ARIA Labels**: Screen reader support
- **Keyboard Navigation**: Full keyboard accessibility
- **Focus Management**: Logical focus order

### 2. Screen Reader Support
- **Alt Text**: Descriptive image alternatives
- **Landmarks**: Page structure identification
- **Live Regions**: Dynamic content updates
- **Skip Links**: Navigation shortcuts

### 3. Color and Contrast
- **WCAG Compliance**: AA level accessibility
- **High Contrast**: Sufficient color contrast
- **Color Independence**: Non-color dependent information
- **Focus Indicators**: Clear focus visibility
