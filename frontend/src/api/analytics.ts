import { api } from './client';

export interface ProductAnalytics {
  product_id: number;
  product_name: string;
  views: number;
  orders: number;
  revenue: number;
  average_rating: number;
  review_count: number;
}

export interface OrderAnalytics {
  total_orders: number;
  total_revenue: number;
  average_order_value: number;
  orders_today: number;
  revenue_today: number;
  top_products: ProductAnalytics[];
}

export interface UserAnalytics {
  total_users: number;
  new_users_today: number;
  active_users: number;
  admin_users: number;
  customer_users: number;
}

export interface SystemStatistics {
  total_products: number;
  total_orders: number;
  total_users: number;
  total_revenue: number;
  average_product_rating: number;
  top_selling_products: ProductAnalytics[];
  recent_orders: Array<{
    id: number;
    order_id: string;
    total_amount: number;
    created_at: string;
    user_email: string;
  }>;
  user_growth: {
    labels: string[];
    data: number[];
  };
}

export interface DashboardMetrics {
  overview: {
    total_products: number;
    total_orders: number;
    total_users: number;
    total_revenue: number;
    average_product_rating: number;
    top_selling_products: ProductAnalytics[];
    recent_orders: Array<{
      id: number;
      order_id: string;
      user_email: string;
      total_amount: number;
      created_at: string;
    }>;
    user_growth: {
      labels: string[];
      data: number[];
    };
  };
  orders: OrderAnalytics;
  users: UserAnalytics;
  products: ProductAnalytics[];
  revenue_chart: Array<{
    date: string;
    revenue: number;
  }>;
  orders_chart: Array<{
    date: string;
    orders: number;
  }>;
  sales_analytics: SalesAnalytics;
  rating_analytics: RatingAnalytics;
}

export interface SalesAnalytics {
  monthly_sales: Array<{
    month: string;
    orders: number;
    revenue: number;
  }>;
  day_of_week_sales: Array<{
    day: number;
    day_name: string;
    orders: number;
    revenue: number;
  }>;
  hourly_sales: Array<{
    hour: number;
    orders: number;
    revenue: number;
  }>;
  conversion_rate: number;
  total_customers: number;
  total_orders: number;
}

export interface RatingAnalytics {
  rating_distribution: Array<{
    rating: number;
    count: number;
    percentage: number;
  }>;
  top_rated_products: Array<{
    product_id: number;
    product_name: string;
    average_rating: number;
    review_count: number;
  }>;
  rating_trends: Array<{
    date: string;
    average_rating: number;
    review_count: number;
  }>;
  overall_stats: {
    total_reviews: number;
    average_rating: number;
    products_with_reviews: number;
    positive_reviews: number;
    neutral_reviews: number;
    negative_reviews: number;
    positive_percentage: number;
  };
}

// Helper function to make API requests using the existing api structure
async function apiRequest<T>(endpoint: string): Promise<T> {
  const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";
  const token = api.getToken();
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers,
  });
  
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  
  return response.json();
}

export const analyticsApi = {
  // Get comprehensive dashboard metrics
  getDashboardMetrics: async (): Promise<DashboardMetrics> => {
    return apiRequest<DashboardMetrics>('/analytics/dashboard');
  },

  // Get system overview statistics
  getSystemOverview: async (): Promise<SystemStatistics> => {
    return apiRequest<SystemStatistics>('/analytics/overview');
  },

  // Get order analytics
  getOrderAnalytics: async (): Promise<OrderAnalytics> => {
    return apiRequest<OrderAnalytics>('/analytics/orders');
  },

  // Get user analytics
  getUserAnalytics: async (): Promise<UserAnalytics> => {
    return apiRequest<UserAnalytics>('/analytics/users');
  },

  // Get product analytics
  getProductAnalytics: async (): Promise<ProductAnalytics[]> => {
    return apiRequest<ProductAnalytics[]>('/analytics/products');
  },
};
