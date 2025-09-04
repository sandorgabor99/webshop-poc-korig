# Testing Strategy Documentation

## Testing Philosophy

The testing strategy follows the **Testing Pyramid** approach, emphasizing unit tests as the foundation, with integration and end-to-end tests providing additional confidence layers.

```
        /\
       /  \     E2E Tests (Few, Critical Paths)
      /____\    
     /      \   Integration Tests (API, Database)
    /________\  
   /          \ Unit Tests (Many, Fast, Isolated)
  /____________\
```

## Testing Stack

### 1. Backend Testing
- **Pytest 7.4.3**: Primary testing framework
- **Pytest-asyncio**: Async test support
- **Pytest-cov**: Coverage reporting
- **HTTPX**: HTTP client for API testing
- **SQLAlchemy Testing**: Database testing utilities

### 2. Frontend Testing
- **Vitest**: Fast unit testing framework
- **React Testing Library**: Component testing utilities
- **Jest DOM**: DOM testing matchers
- **User Event**: User interaction simulation
- **Coverage V8**: Code coverage reporting

### 3. Integration Testing
- **Docker Compose**: Service integration testing
- **Health Checks**: Service availability verification
- **API Contract Testing**: Endpoint validation
- **Database Integration**: Real database testing

## Test Categories

### 1. Unit Tests

**Backend Unit Tests**
```python
def test_user_creation():
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.role == UserRole.CUSTOMER

def test_product_average_rating():
    product = Product(name="Test Product", price=10.0)
    product.reviews = [
        Review(rating=5),
        Review(rating=3),
        Review(rating=4)
    ]
    assert product.average_rating == 4.0
    assert product.review_count == 3
```

**Frontend Unit Tests**
```typescript
describe('useCart Hook', () => {
  it('should add items to cart', () => {
    const { result } = renderHook(() => useCart());
    const product = { id: 1, name: 'Test Product', price: 10 };
    
    act(() => {
      result.current.addItem(product, 2);
    });
    
    expect(result.current.items).toHaveLength(1);
    expect(result.current.getTotalItems()).toBe(2);
  });
});
```

### 2. Integration Tests

**API Integration Tests**
```python
def test_product_crud_operations(client, test_admin, auth_headers):
    # Create product
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 10
    }
    
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 200
    
    product_id = response.json()["id"]
    
    # Read product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    
    # Update product
    update_data = {"price": 39.99}
    response = client.put(f"/products/{product_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    # Delete product
    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 200
```

**Database Integration Tests**
```python
def test_order_creation_with_items(db_session, test_user, test_product):
    order = Order(
        user_id=test_user.id,
        total_amount=test_product.price * 2
    )
    db_session.add(order)
    db_session.commit()
    
    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=2,
        unit_price=test_product.price
    )
    db_session.add(order_item)
    db_session.commit()
    
    assert order.items[0].quantity == 2
    assert order.total_amount == test_product.price * 2
```

### 3. End-to-End Tests

**Container Integration Tests**
```yaml
test-docker-compose:
  run: |
    # Build images
    docker-compose build
    
    # Start services
    docker-compose up -d
    
    # Wait for services to be ready
    sleep 60
    
    # Test backend
    curl -f http://localhost:8000/health || exit 1
    
    # Test frontend
    curl -f http://localhost:80/health || exit 1
    
    # Stop services
    docker-compose down
```

**Health Check Tests**
```bash
# Backend health check
curl -f http://localhost:8000/health

# Frontend health check
curl -f http://localhost:80/health

# Database connectivity
python -c "from app.database import engine; print('DB OK' if engine.connect() else 'DB FAIL')"
```

## Test Configuration

### 1. Pytest Configuration (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### 2. Test Database Setup
```python
# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Override database dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
```

### 3. Test Fixtures
```python
@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=hash_password("testpass123"),
        role=UserRole.CUSTOMER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
```

## Coverage & Quality Metrics

### 1. Coverage Reporting
```yaml
# Backend coverage
- name: Run backend tests
  run: |
    pytest tests/ -v --cov=app --cov-report=xml --cov-report=html

# Frontend coverage
- name: Run frontend tests
  run: |
    npm test -- --coverage
```

**Coverage Metrics:**
- **Backend**: Line, branch, and function coverage
- **Frontend**: Statement, branch, and function coverage
- **Integration**: API endpoint coverage
- **Overall**: Combined coverage reporting

### 2. Quality Gates
- **Test Coverage**: Minimum 80% coverage required
- **Test Execution**: All tests must pass
- **Security Scan**: No critical vulnerabilities
- **Performance**: Response time thresholds

## Testing Best Practices

### 1. Test Organization
- **Test Structure**: Mirror application structure
- **Naming Convention**: Descriptive test names
- **Fixture Management**: Reusable test data
- **Test Isolation**: Independent test execution

### 2. Test Data Management
- **Factory Pattern**: Test data generation
- **Database Seeding**: Consistent test data
- **Cleanup Strategy**: Proper test cleanup
- **Data Isolation**: Test-specific data sets

### 3. Performance Testing
- **Response Time**: API endpoint performance
- **Load Testing**: Concurrent user simulation
- **Resource Usage**: Memory and CPU monitoring
- **Scalability**: Performance under load

## Security Testing

### 1. Vulnerability Scanning
```yaml
security-scan:
  steps:
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
```

### 2. Container Security
```yaml
container-security:
  steps:
    - name: Run Trivy on backend image
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'webshop-backend:latest'
        format: 'sarif'
        output: 'trivy-backend-results.sarif'
```

### 3. Authentication Testing
```python
def test_unauthorized_access(client):
    # Test protected endpoints without authentication
    response = client.get("/orders/")
    assert response.status_code == 401
    
    response = client.post("/products/", json={})
    assert response.status_code == 401

def test_admin_only_endpoints(client, test_user, auth_headers):
    # Test admin endpoints with regular user
    response = client.delete("/products/1", headers=auth_headers)
    assert response.status_code == 403
```

## Performance Testing

### 1. Load Testing
```python
def test_api_performance(client):
    import time
    
    start_time = time.time()
    response = client.get("/products/")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 0.5  # 500ms threshold
```

### 2. Database Performance
```python
def test_database_query_performance(db_session):
    import time
    
    start_time = time.time()
    products = db_session.query(Product).all()
    end_time = time.time()
    
    assert (end_time - start_time) < 0.1  # 100ms threshold
```

## Test Automation

### 1. CI/CD Integration
```yaml
test-backend:
  strategy:
    matrix:
      python-version: [3.11, 3.12]
  steps:
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: pip install -r requirements.ci.txt
    
    - name: Run tests
      run: pytest tests/ -v --cov=app
```

### 2. Test Execution
- **Automatic**: Tests run on every commit and PR
- **Parallel**: Matrix testing for multiple Python versions
- **Caching**: Dependency and build caching
- **Reporting**: Coverage and test results reporting

## Test Maintenance

### 1. Regular Tasks
- **Dependency Updates**: Keep testing libraries current
- **Test Data Refresh**: Update test data as needed
- **Coverage Monitoring**: Track coverage trends
- **Performance Monitoring**: Monitor test execution times

### 2. Test Refactoring
- **Code Changes**: Update tests when code changes
- **API Changes**: Update integration tests for API changes
- **Model Changes**: Update database tests for model changes
- **UI Changes**: Update frontend tests for UI changes

## Future Testing Enhancements

### 1. Advanced Testing
- **Property-Based Testing**: Hypothesis for Python
- **Mutation Testing**: Code quality validation
- **Visual Regression Testing**: UI consistency testing
- **Accessibility Testing**: WCAG compliance testing

### 2. Testing Tools
- **Test Data Generation**: Faker library integration
- **Mock Services**: Service virtualization
- **Performance Monitoring**: APM integration
- **Test Analytics**: Test execution analytics

## Conclusion

This comprehensive testing strategy ensures:

- **Code Quality**: High test coverage and quality gates
- **Reliability**: Comprehensive testing at all levels
- **Security**: Vulnerability scanning and security testing
- **Performance**: Performance testing and monitoring
- **Maintainability**: Well-organized and maintainable tests
- **Automation**: Fully automated testing in CI/CD pipeline

The testing approach provides confidence in code changes while maintaining high software quality standards.
