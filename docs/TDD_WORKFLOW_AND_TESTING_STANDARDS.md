> **Documentation Priorities**
> 1. Maximize LLM understanding
> 2. Maximize LLM strengths (pattern recognition, consistency, exhaustive reasoning)
> 3. Minimize LLM weaknesses (ambiguity, hidden context, state drift)
> 4. Optimize for LLM context efficiency
> 5. Human readability is secondary

# TDD Workflow and Testing Standards

## Core Principles

1. **Test-Driven Development (TDD) Cycle**
   - Red: Write a failing test
   - Green: Implement minimal code to pass
   - Refactor: Improve code quality
   - Verify: Ensure all tests pass
   - Handoff: Pass to next developer

2. **Test Isolation**
   - No test depends on another test's state
   - Tests can run in any order
   - Parallel execution by default
   - Clean up all resources post-execution

## Test Categories

### 1. Unit Tests (`@unit`)
- **Purpose**: Test individual components in isolation
- **Execution**: Parallel
- **Dependencies**: Mock all external services
- **Speed**: <100ms per test
- **Example**:
  ```python
  def test_calculate_total():
      cart = ShoppingCart()
      cart.add_item("item1", price=10, quantity=2)
      assert cart.total() == 20
  ```

### 2. Integration Tests (`@integration`)
- **Purpose**: Test component interactions
- **Execution**: Sequential by default
- **Dependencies**: Real services with test instances
- **Cleanup**: Required after each test
- **Example**:
  ```python
  @pytest.mark.integration
  def test_order_processing():
      with test_database() as db:
          order = process_order(test_order_data)
          assert db.order_exists(order.id)
  ```

### 3. E2E Tests (`@e2e`)
- **Purpose**: Test complete user flows
- **Execution**: Sequential, isolated environments
- **Dependencies**: Full stack deployment
- **Example**:
  ```python
  @pytest.mark.e2e
  def test_checkout_flow():
      with TestBrowser() as browser:
          browser.login()
          browser.add_to_cart()
          assert "Order Complete" in browser.checkout()
  ```

### 4. Serial Tests (`@serial`)
- **Purpose**: Tests requiring exclusive resource access
- **Execution**: One at a time
- **Use Case**: Global configuration changes
- **Example**:
  ```python
  @pytest.mark.serial
  def test_config_update():
      original = get_config()
      try:
          set_config("mode", "test")
          assert get_config("mode") == "test"
      finally:
          set_config("mode", original)
  ```

## Implementation Guidelines

### Test Structure
```python
# test_module.py
"""
Test Module: Description of test scope

Category: @unit | @integration | @e2e | @serial
Timeout: 2.0s (default) | <custom>
"""


def test_feature():
    # Arrange
    # Act
    # Assert
    pass
```

### Mocking Strategy
```python
# Good: Mock all external dependencies
def test_external_service():
    mock_service = Mock()
    mock_service.fetch_data.return_value = test_data
    
    result = process_with_service(mock_service)
    assert result == expected


# Bad: Real network calls
def test_bad_example():
    # Don't do this in unit tests
    data = requests.get("https://api.example.com/data").json()
    process(data)
```

### Fixture Usage
```python
@pytest.fixture
def test_user():
    user = create_test_user()
    try:
        yield user
    finally:
        user.delete()  # Ensure cleanup
```

## Execution Control

### Running Tests
```bash
# Run all tests with appropriate concurrency
pytest \
  -n auto \
  -m "not serial" \
  --dist=loadscope


# Run only serial tests
pytest -n 0 -m serial


# Run specific category
pytest -m "integration"
```

### Timeout Handling
- Default: 2.0 seconds per test
- Override with `@pytest.mark.timeout(X)`
- Global timeout in `pytest.ini`

## Best Practices

1. **Test Independence**
   - No test depends on another's execution
   - Reset all state between tests

2. **Deterministic Behavior**
   - Same input → Same output
   - No race conditions
   - No timing dependencies

3. **Resource Management**
   - Use context managers for resources
   - Clean up even on test failure
   - Never leave test artifacts

4. **Performance**
   - Unit tests: <100ms
   - Integration tests: <1s
   - E2E tests: Document expected duration

## Example Workflow

1. **Developer A** writes first failing test
   ```python
   # test_calculator.py
   def test_addition():
       assert add(2, 3) == 5  # Fails
   ```

2. **Developer B** implements minimal solution
   ```python
   # calculator.py
   def add(a, b):
       return a + b
   ```

3. **Developer C** writes next test
   ```python
   def test_negative_numbers():
       assert add(-1, 1) == 0  # Fails
   ```

4. **Developer D** updates implementation
   ```python
   def add(a, b):
       return a + b  # Already handles this case
   ```

## Error Handling

### Test Failure Modes
1. **Assertion Failure**: Expected vs Actual mismatch
2. **Timeout**: Test took too long
3. **Error**: Unhandled exception
4. **Setup/Teardown Failure**: Resource issues

### Debugging Tips
- Run single test: `pytest path/to/test.py::test_name`
- Show output: `pytest -v -s`
- Debug on failure: `pytest --pdb`

## Documentation Requirements

### Test Documentation
- Module-level docstring with category
- Test purpose in docstring
- Complex logic should include comments

### Reporting
- Clear error messages
- Helpful assertion messages
- Context in failure reports

## Maintenance

### Test Review
- Regular test audits
- Remove redundant tests
- Update tests with requirements

### Performance Monitoring
- Track test duration
- Identify slow tests
- Optimize where possible
