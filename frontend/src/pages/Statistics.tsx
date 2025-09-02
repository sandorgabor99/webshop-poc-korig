import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import { analyticsApi } from '../api/analytics';
import type { DashboardMetrics, ProductAnalytics } from '../api/analytics';
import './Statistics.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
);

const Statistics: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'orders' | 'users' | 'products' | 'sales' | 'ratings'>('overview');

  useEffect(() => {
    loadDashboardMetrics();
  }, []);

  const loadDashboardMetrics = async () => {
    try {
      setLoading(true);
      const data = await analyticsApi.getDashboardMetrics();
      setMetrics(data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard metrics');
      console.error('Error loading metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // Chart.js options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: '#6c757d',
          font: { size: 12 }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff'
      }
    },
    scales: {
      x: {
        grid: { color: '#f1f3f4' },
        ticks: { color: '#6c757d' }
      },
      y: {
        grid: { color: '#f1f3f4' },
        ticks: { color: '#6c757d' }
      }
    }
  };

  // Helper function to check if data exists and is valid
  const hasValidData = (data: any) => {
    return data && Array.isArray(data) && data.length > 0;
  };

  if (loading) {
    return (
      <div className="statistics-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading statistics...</p>
        </div>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div className="statistics-container">
        <div className="error-message">
          <h2>Error</h2>
          <p>{error || 'Failed to load statistics'}</p>
          <button onClick={loadDashboardMetrics} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-container">
      <div className="statistics-header">
        <h1>📊 Admin Statistics Dashboard</h1>
        <p>Comprehensive analytics and insights for your webshop</p>
      </div>

      {/* Navigation Tabs */}
      <div className="statistics-tabs">
        <button
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📈 Overview
        </button>
        <button
          className={`tab-button ${activeTab === 'orders' ? 'active' : ''}`}
          onClick={() => setActiveTab('orders')}
        >
          🛒 Orders
        </button>
        <button
          className={`tab-button ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          👥 Users
        </button>
        <button
          className={`tab-button ${activeTab === 'products' ? 'active' : ''}`}
          onClick={() => setActiveTab('products')}
        >
          🛍️ Products
        </button>
        <button
          className={`tab-button ${activeTab === 'sales' ? 'active' : ''}`}
          onClick={() => setActiveTab('sales')}
        >
          📈 Sales Analytics
        </button>
        <button
          className={`tab-button ${activeTab === 'ratings' ? 'active' : ''}`}
          onClick={() => setActiveTab('ratings')}
        >
          ⭐ Rating Analysis
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="tab-content">
          <div className="metrics-grid">
            <div className="metric-card primary">
              <div className="metric-icon">💰</div>
              <div className="metric-content">
                <h3>Total Revenue</h3>
                <div className="metric-value">{formatCurrency(metrics.overview?.total_revenue || 0)}</div>
              </div>
            </div>

            <div className="metric-card success">
              <div className="metric-icon">📦</div>
              <div className="metric-content">
                <h3>Total Orders</h3>
                <div className="metric-value">{metrics.overview?.total_orders || 0}</div>
              </div>
            </div>

            <div className="metric-card info">
              <div className="metric-icon">👥</div>
              <div className="metric-content">
                <h3>Total Users</h3>
                <div className="metric-value">{metrics.overview?.total_users || 0}</div>
              </div>
            </div>

            <div className="metric-card warning">
              <div className="metric-icon">🛍️</div>
              <div className="metric-content">
                <h3>Total Products</h3>
                <div className="metric-value">{metrics.overview?.total_products || 0}</div>
              </div>
            </div>
          </div>

          <div className="charts-section">
            <div className="chart-container">
              <h3>Revenue Trend</h3>
              <div className="chart">
                {hasValidData(metrics.revenue_chart) ? (
                  <Line
                    data={{
                      labels: metrics.revenue_chart.map(item => item.date),
                      datasets: [
                        {
                          label: 'Revenue',
                          data: metrics.revenue_chart.map(item => item.revenue),
                          borderColor: 'rgba(75, 192, 192, 1)',
                          backgroundColor: 'rgba(75, 192, 192, 0.2)',
                          borderWidth: 3,
                          fill: true,
                          tension: 0.4,
                        }
                      ]
                    }}
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: false
                        }
                      }
                    }}
                    height={300}
                  />
                ) : (
                  <p className="no-data">No revenue data available</p>
                )}
              </div>
            </div>

            <div className="chart-container">
              <h3>Orders Trend (Last 30 Days)</h3>
              <div className="chart">
                {hasValidData(metrics.orders_chart) ? (
                  <Line
                    data={{
                      labels: metrics.orders_chart.map(item => formatDate(item.date)),
                      datasets: [
                        {
                          label: 'Orders',
                          data: metrics.orders_chart.map(item => item.orders || 0),
                          borderColor: 'rgba(118, 75, 162, 1)',
                          backgroundColor: 'rgba(118, 75, 162, 0.1)',
                          borderWidth: 3,
                          pointRadius: 6,
                          pointBackgroundColor: 'rgba(118, 75, 162, 1)',
                          fill: true,
                          tension: 0.4
                        }
                      ]
                    }}
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: false
                        }
                      }
                    }}
                    height={300}
                  />
                ) : (
                  <p className="no-data">No order data available</p>
                )}
              </div>
            </div>
          </div>

          <div className="recent-orders">
            <h3>Recent Orders</h3>
            <div className="orders-table">
              <table>
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Customer</th>
                    <th>Amount</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {metrics.overview?.recent_orders?.map((order) => (
                    <tr key={order.id}>
                      <td>{order.order_id}</td>
                      <td>{order.user_email}</td>
                      <td>{formatCurrency(order.total_amount || 0)}</td>
                      <td>{formatDate(order.created_at)}</td>
                    </tr>
                  )) || (
                    <tr>
                      <td colSpan={4} className="no-data">No recent orders available</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Orders Tab */}
      {activeTab === 'orders' && (
        <div className="tab-content">
          <div className="metrics-grid">
            <div className="metric-card primary">
              <div className="metric-icon">📊</div>
              <div className="metric-content">
                <h3>Total Orders</h3>
                <div className="metric-value">{metrics.orders?.total_orders || 0}</div>
              </div>
            </div>

            <div className="metric-card success">
              <div className="metric-icon">💰</div>
              <div className="metric-content">
                <h3>Total Revenue</h3>
                <div className="metric-value">{formatCurrency(metrics.orders?.total_revenue || 0)}</div>
              </div>
            </div>

            <div className="metric-card info">
              <div className="metric-icon">📈</div>
              <div className="metric-content">
                <h3>Avg Order Value</h3>
                <div className="metric-value">{formatCurrency(metrics.orders?.average_order_value || 0)}</div>
              </div>
            </div>

            <div className="metric-card warning">
              <div className="metric-icon">📅</div>
              <div className="metric-content">
                <h3>Today's Orders</h3>
                <div className="metric-value">{metrics.orders?.orders_today || 0}</div>
              </div>
            </div>
          </div>

          <div className="top-products">
            <h3>Top Selling Products</h3>
            <div className="chart-container">
              {hasValidData(metrics.orders?.top_products) ? (
                <Bar
                  data={{
                    labels: metrics.orders.top_products.map(product => product.product_name || 'Unknown'),
                    datasets: [
                      {
                        label: 'Orders',
                        data: metrics.orders.top_products.map(product => product.orders || 0),
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                        yAxisID: 'y'
                      },
                      {
                        label: 'Revenue',
                        data: metrics.orders.top_products.map(product => product.revenue || 0),
                        backgroundColor: 'rgba(118, 75, 162, 0.8)',
                        borderColor: 'rgba(118, 75, 162, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                        yAxisID: 'y1'
                      }
                    ]
                  }}
                  options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      title: {
                        display: false
                      }
                    },
                    scales: {
                      x: {
                        ...chartOptions.scales.x,
                        title: {
                          display: true,
                          text: 'Product'
                        }
                      },
                      y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                          display: true,
                          text: 'Orders'
                        }
                      },
                      y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                          display: true,
                          text: 'Revenue ($)'
                        },
                        grid: {
                          drawOnChartArea: false,
                        },
                      }
                    }
                  }}
                  height={400}
                />
              ) : (
                <p className="no-data">No product data available</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className="tab-content">
          <div className="metrics-grid">
            <div className="metric-card primary">
              <div className="metric-icon">👥</div>
              <div className="metric-content">
                <h3>Total Users</h3>
                <div className="metric-value">{metrics.users?.total_users || 0}</div>
              </div>
            </div>

            <div className="metric-card success">
              <div className="metric-icon">🆕</div>
              <div className="metric-content">
                <h3>New Today</h3>
                <div className="metric-value">{metrics.users?.new_users_today || 0}</div>
              </div>
            </div>

            <div className="metric-card info">
              <div className="metric-icon">🔥</div>
              <div className="metric-content">
                <h3>Active Users</h3>
                <div className="metric-value">{metrics.users?.active_users || 0}</div>
              </div>
            </div>

            <div className="metric-card warning">
              <div className="metric-icon">👨‍💼</div>
              <div className="metric-content">
                <h3>Admin Users</h3>
                <div className="metric-value">{metrics.users?.admin_users || 0}</div>
              </div>
            </div>
          </div>

          <div className="user-growth">
            <h3>User Growth (Last 7 Days)</h3>
            <div className="chart-container">
              {hasValidData(metrics.overview?.user_growth?.labels) ? (
                <Line
                  data={{
                    labels: metrics.overview.user_growth.labels,
                    datasets: [
                      {
                        label: 'New Users',
                        data: metrics.overview.user_growth.data,
                        borderColor: 'rgba(102, 126, 234, 1)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 3,
                        pointRadius: 6,
                        pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                        fill: true,
                        tension: 0.4
                      }
                    ]
                  }}
                  options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      title: {
                        display: false
                      }
                    }
                  }}
                  height={300}
                />
              ) : (
                <p className="no-data">No user growth data available</p>
              )}
            </div>
          </div>

          <div className="user-roles">
            <h3>User Distribution by Role</h3>
            <div className="chart-container">
              <Doughnut
                data={{
                  labels: ['Admin', 'Customer'],
                  datasets: [
                    {
                      data: [
                        metrics.users?.admin_users || 0,
                        metrics.users?.customer_users || 0
                      ],
                      backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)'
                      ],
                      borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(118, 75, 162, 1)'
                      ],
                      borderWidth: 2,
                    }
                  ]
                }}
                options={{
                  ...chartOptions,
                  plugins: {
                    ...chartOptions.plugins,
                    title: {
                      display: false
                    }
                  }
                }}
                height={300}
              />
            </div>
          </div>
        </div>
      )}

      {/* Products Tab */}
      {activeTab === 'products' && (
        <div className="tab-content">
          <div className="products-analytics">
            <h3>Product Performance Analytics</h3>
            <div className="chart-container">
              {hasValidData(metrics.products) ? (
                <Bar
                  data={{
                    labels: metrics.products.slice(0, 10).map(product => product.product_name || 'Unknown'),
                    datasets: [
                      {
                        label: 'Orders',
                        data: metrics.products.slice(0, 10).map(product => product.orders || 0),
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                        yAxisID: 'y'
                      },
                      {
                        label: 'Revenue',
                        data: metrics.products.slice(0, 10).map(product => product.revenue || 0),
                        backgroundColor: 'rgba(118, 75, 162, 0.8)',
                        borderColor: 'rgba(118, 75, 162, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                        yAxisID: 'y1'
                      }
                    ]
                  }}
                  options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      title: {
                        display: false
                      }
                    },
                    scales: {
                      x: {
                        ...chartOptions.scales.x,
                        title: {
                          display: true,
                          text: 'Product'
                        }
                      },
                      y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                          display: true,
                          text: 'Orders'
                        }
                      },
                      y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                          display: true,
                          text: 'Revenue ($)'
                        },
                        grid: {
                          drawOnChartArea: false,
                        },
                      }
                    }
                  }}
                  height={400}
                />
              ) : (
                <p className="no-data">No product data available</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Sales Analytics Tab */}
      {activeTab === 'sales' && (
        <div className="tab-content">
          <div className="metrics-grid">
            <div className="metric-card primary">
              <div className="metric-icon">📊</div>
              <div className="metric-content">
                <h3>Conversion Rate</h3>
                <div className="metric-value">{metrics.sales_analytics?.conversion_rate || 0}%</div>
              </div>
            </div>

            <div className="metric-card success">
              <div className="metric-icon">👥</div>
              <div className="metric-content">
                <h3>Total Customers</h3>
                <div className="metric-value">{metrics.sales_analytics?.total_customers || 0}</div>
              </div>
            </div>

            <div className="metric-card info">
              <div className="metric-icon">📦</div>
              <div className="metric-content">
                <h3>Total Orders</h3>
                <div className="metric-value">{metrics.sales_analytics?.total_orders || 0}</div>
              </div>
            </div>

            <div className="metric-card warning">
              <div className="metric-icon">💰</div>
              <div className="metric-content">
                <h3>Monthly Revenue</h3>
                <div className="metric-value">
                  {(() => {
                    // Simple debug logging
                    console.log('=== MONTHLY REVENUE DEBUG ===');
                    console.log('Metrics:', metrics);
                    console.log('Sales analytics:', metrics?.sales_analytics);
                    
                    const monthlySales = metrics?.sales_analytics?.monthly_sales;
                    console.log('Monthly sales:', monthlySales);
                    
                    if (!monthlySales || !Array.isArray(monthlySales) || monthlySales.length === 0) {
                      console.log('No monthly sales data available');
                      return formatCurrency(0);
                    }
                    
                    // Get the latest month (last in array)
                    const latestMonth = monthlySales[monthlySales.length - 1];
                    console.log('Latest month:', latestMonth);
                    
                    if (!latestMonth || typeof latestMonth.revenue !== 'number') {
                      console.log('Invalid latest month data:', latestMonth);
                      return formatCurrency(0);
                    }
                    
                    console.log('Latest month revenue:', latestMonth.revenue);
                    return formatCurrency(latestMonth.revenue);
                  })()}
                </div>
              </div>
            </div>
          </div>

          <div className="sales-trends">
            <h3>Sales Trend (Last 12 Months)</h3>
            <div className="chart-container">
              {hasValidData(metrics.sales_analytics?.monthly_sales) ? (
                <Bar
                  data={{
                    labels: metrics.sales_analytics.monthly_sales.map(month => month.month),
                    datasets: [
                      {
                        label: 'Total Revenue',
                        data: metrics.sales_analytics.monthly_sales.map(month => month.revenue || 0),
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                        yAxisID: 'y'
                      }
                    ]
                  }}
                  options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      title: {
                        display: false
                      }
                    },
                    scales: {
                      x: {
                        ...chartOptions.scales.x,
                        title: {
                          display: true,
                          text: 'Month'
                        }
                      },
                      y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                          display: true,
                          text: 'Revenue ($)'
                        }
                      }
                    }
                  }}
                  height={400}
                />
              ) : (
                <p className="no-data">No sales data available</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Rating Analysis Tab */}
      {activeTab === 'ratings' && (
        <div className="tab-content">
          <div className="metrics-grid">
            <div className="metric-card primary">
              <div className="metric-icon">⭐</div>
              <div className="metric-content">
                <h3>Overall Rating</h3>
                <div className="metric-value">{metrics.rating_analytics?.overall_stats?.average_rating || 0}/5</div>
              </div>
            </div>

            <div className="metric-card success">
              <div className="metric-icon">📝</div>
              <div className="metric-content">
                <h3>Total Reviews</h3>
                <div className="metric-value">{metrics.rating_analytics?.overall_stats?.total_reviews || 0}</div>
              </div>
            </div>

            <div className="metric-card info">
              <div className="metric-icon">👍</div>
              <div className="metric-content">
                <h3>Positive Reviews</h3>
                <div className="metric-value">{metrics.rating_analytics?.overall_stats?.positive_percentage || 0}%</div>
              </div>
            </div>

            <div className="metric-card warning">
              <div className="metric-icon">🛍️</div>
              <div className="metric-content">
                <h3>Products with Reviews</h3>
                <div className="metric-value">{metrics.rating_analytics?.overall_stats?.products_with_reviews || 0}</div>
              </div>
            </div>
          </div>

          <div className="charts-section">
            <div className="chart-container">
              <h3>Rating Distribution</h3>
              <div className="chart">
                {hasValidData(metrics.rating_analytics?.rating_distribution) ? (
                  <Bar
                    data={{
                      labels: metrics.rating_analytics.rating_distribution.map(item => `${item.rating} Stars`),
                      datasets: [
                        {
                          label: 'Count',
                          data: metrics.rating_analytics.rating_distribution.map(item => item.count),
                          backgroundColor: [
                            'rgba(220, 53, 69, 0.8)',
                            'rgba(255, 193, 7, 0.8)',
                            'rgba(255, 193, 7, 0.8)',
                            'rgba(40, 167, 69, 0.8)',
                            'rgba(40, 167, 69, 0.8)'
                          ],
                          borderColor: [
                            'rgba(220, 53, 69, 1)',
                            'rgba(255, 193, 7, 1)',
                            'rgba(255, 193, 7, 1)',
                            'rgba(40, 167, 69, 1)',
                            'rgba(40, 167, 69, 1)'
                          ],
                          borderWidth: 2,
                          borderRadius: 8,
                        }
                      ]
                    }}
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: false
                        }
                      }
                    }}
                    height={300}
                  />
                ) : (
                  <p className="no-data">No rating distribution data available</p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="refresh-section">
        <button onClick={loadDashboardMetrics} className="refresh-button">
          🔄 Refresh Data
        </button>
        <p className="last-updated">
          Last updated: {new Date().toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export default Statistics;
