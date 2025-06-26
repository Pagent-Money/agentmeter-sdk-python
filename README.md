# AgentMeter Python SDK

A comprehensive Python SDK for integrating AgentMeter usage tracking and billing into your applications. **支持三种付费模式：API请求付费、Token付费、即时付费。**

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://pypi.org/project/agentmeter-sdk/)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🚀 Features

- **Three Payment Models** - Support for different billing scenarios
- **Easy Integration** - Simple decorators and context managers
- **Automatic Tracking** - Built-in usage measurement
- **User Meter Management** - Subscription limits and monitoring
- **Comprehensive API** - Full access to AgentMeter platform features
- **Error Handling** - Robust error handling and retry logic

## 💰 Payment Types

### 1. API Request Pay (按API次数付费)
Charge based on the number of API calls made.
- **Use Case**: API services, function calls, request-based features
- **Formula**: `# of API requests × unit price`
- **Example**: `1 × $0.3 = $0.3` per API call

### 2. Token-based Pay (按Token付费)
Charge based on input/output token consumption from AI models.
- **Use Case**: LLM calls, AI processing, content generation
- **Formula**: `(input tokens × input price) + (output tokens × output price)`
- **Example**: `1000 × $0.004 + 500 × $0.0001 = $4.05`

### 3. Instant Pay (即时付费)
Charge arbitrary amounts immediately for premium features.
- **Use Case**: Premium features, one-time payments, upgrades
- **Formula**: `1 × price`
- **Example**: `1 × $4.99 = $4.99` for premium feature

## 📦 Installation

```bash
pip install agentmeter-sdk
```

## 🔧 Quick Start

### Basic Setup

```python
from agentmeter import create_client

# Create client with your credentials
client = create_client(
    api_key="your_api_key",
    project_id="proj_123",
    agent_id="agent_456",
    user_id="user_789"
)
```

### 1. API Request Pay Examples

```python
from agentmeter import meter_api_request_pay, track_api_request_pay

# Method 1: Direct API call
response = client.record_api_request_pay(
    api_calls=1,
    unit_price=0.3,
    metadata={"endpoint": "/api/search"}
)

# Method 2: Decorator
@meter_api_request_pay(client, unit_price=0.3)
def search_api(query):
    return perform_search(query)

result = search_api("python tutorials")

# Method 3: Context manager
with track_api_request_pay(client, project_id, agent_id, unit_price=0.3) as usage:
    # Your API logic here
    usage["api_calls"] = 1
    usage["metadata"]["operation"] = "search"
```

### 2. Token-based Pay Examples

```python
from agentmeter import meter_token_based_pay, track_token_based_pay

# Method 1: Direct API call
response = client.record_token_based_pay(
    tokens_in=1000,
    tokens_out=500,
    input_token_price=0.004,
    output_token_price=0.0001,
    metadata={"model": "gpt-4"}
)

# Method 2: Decorator with token extraction
def extract_tokens(*args, result=None, **kwargs):
    # Extract token counts from your LLM response
    return input_tokens, output_tokens

@meter_token_based_pay(
    client, 
    input_token_price=0.004,
    output_token_price=0.0001,
    tokens_extractor=extract_tokens
)
def llm_call(prompt):
    return model.generate(prompt)

# Method 3: Context manager
with track_token_based_pay(client, project_id, agent_id) as usage:
    # Your LLM logic here
    usage["tokens_in"] = 1000
    usage["tokens_out"] = 500
    usage["metadata"]["model"] = "gpt-4"
```

### 3. Instant Pay Examples

```python
from agentmeter import meter_instant_pay, track_instant_pay

# Method 1: Direct API call
response = client.record_instant_pay(
    amount=4.99,
    description="Premium feature unlock",
    metadata={"feature": "advanced_search"}
)

# Method 2: Conditional decorator
def should_charge(*args, **kwargs):
    return kwargs.get('premium', False)

@meter_instant_pay(
    client,
    amount=4.99,
    description="Premium feature",
    condition_func=should_charge
)
def premium_feature(data, premium=False):
    if premium:
        return advanced_processing(data)
    return basic_processing(data)

# Method 3: Context manager
with track_instant_pay(client, project_id, agent_id) as usage:
    # Your premium feature logic here
    usage["amount"] = 9.99
    usage["metadata"]["feature"] = "ai_analysis"
```

## 🎯 Advanced Features

### User Meter Management

```python
# Set user subscription limits
user_meter = client.set_user_meter(
    threshold_amount=100.0,  # $100 monthly limit
    user_id="user_123"
)

# Check current usage
current_meter = client.get_user_meter(user_id="user_123")
print(f"Usage: ${current_meter.current_usage}/${current_meter.threshold_amount}")

# Manually increment usage
client.increment_user_meter(amount=15.50, user_id="user_123")

# Reset monthly usage
client.reset_user_meter(user_id="user_123")
```

### Project and Billing Management

```python
# Get usage statistics
stats = client.get_meter_stats(timeframe="30 days")
print(f"Total cost: ${stats.total_cost}")
print(f"API calls: {stats.total_api_calls}")
print(f"Tokens: {stats.total_tokens_in + stats.total_tokens_out}")

# List recent events
events = client.get_events(limit=10, user_id="user_123")

# Create billing records
billing_record = client.create_billing_record(
    project_id="proj_123",
    period_start="2024-03-01T00:00:00Z",
    period_end="2024-03-31T23:59:59Z",
    amount=150.00,
    status="pending"
)
```

### Batch Tracking

```python
from agentmeter import AgentMeterTracker

# Create tracker for batched events
tracker = AgentMeterTracker(
    client=client,
    project_id="proj_123",
    agent_id="agent_456",
    auto_flush=True,
    batch_size=10
)

# Track multiple events efficiently
tracker.track_api_request_pay(api_calls=1, unit_price=0.3)
tracker.track_token_based_pay(tokens_in=500, tokens_out=250)
tracker.track_instant_pay(amount=2.99, description="Feature unlock")

# Manually flush if needed
tracker.flush()
```

## 🛒 E-commerce Integration Example

```python
class EcommerceService:
    def __init__(self, client):
        self.client = client
    
    @meter_api_request_pay(client, unit_price=0.05)
    def search_products(self, query, user_id):
        """Product search - charged per search"""
        return perform_search(query)
    
    @meter_token_based_pay(client, tokens_extractor=extract_review_tokens)
    def analyze_review_sentiment(self, review_text, user_id):
        """AI review analysis - charged by tokens"""
        return ai_analyze_sentiment(review_text)
    
    @meter_instant_pay(client, amount=9.99, condition_func=is_premium_user)
    def get_premium_support(self, issue, user_id, premium=False):
        """Premium support - instant charge"""
        return provide_premium_support(issue)
```

## 🎨 Class-level Metering

```python
from agentmeter import meter_agent, PaymentType

@meter_agent(
    client, 
    PaymentType.API_REQUEST_PAY, 
    unit_price=0.1,
    methods_to_meter=['search', 'recommend']
)
class SearchAgent:
    def search(self, query):
        """This method will be automatically metered"""
        return perform_search(query)
    
    def recommend(self, user_id):
        """This method will be automatically metered"""
        return get_recommendations(user_id)
    
    def _internal_method(self):
        """Private methods won't be metered"""
        pass
```

## 🔧 Configuration

### Environment Variables

```bash
export AGENTMETER_API_KEY="your_api_key"
export AGENTMETER_PROJECT_ID="proj_123"
export AGENTMETER_AGENT_ID="agent_456"
```

### Configuration Object

```python
from agentmeter import AgentMeterConfig

config = AgentMeterConfig(
    project_id="proj_123",
    agent_id="agent_456",
    user_id="user_789",
    api_key="your_api_key",
    base_url="https://api.staging.agentmeter.money",
    # Default pricing
    api_request_unit_price=0.001,
    input_token_price=0.000004,
    output_token_price=0.000001
)

client = AgentMeterClient(**config.dict())
```

## 📊 Error Handling

```python
from agentmeter import AgentMeterError, AgentMeterAPIError

try:
    response = client.record_api_request_pay(api_calls=1, unit_price=0.3)
except AgentMeterAPIError as e:
    if e.status_code == 401:
        print("Authentication failed - check your API key")
    elif e.status_code == 429:
        print("Rate limited - retry later")
    else:
        print(f"API error: {e}")
except AgentMeterError as e:
    print(f"SDK error: {e}")
```

## 🔌 Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI
from agentmeter import meter_api_request_pay

app = FastAPI()
client = create_client(...)

@app.get("/search")
@meter_api_request_pay(client, unit_price=0.1)
async def search_endpoint(query: str, user_id: str):
    return {"results": perform_search(query)}
```

### Flask Integration

```python
from flask import Flask
from agentmeter import track_api_request_pay

app = Flask(__name__)
client = create_client(...)

@app.route('/api/recommend/<user_id>')
def recommend(user_id):
    with track_api_request_pay(client, project_id, agent_id, unit_price=0.2) as usage:
        recommendations = get_recommendations(user_id)
        usage["metadata"]["recommendation_count"] = len(recommendations)
        return {"recommendations": recommendations}
```

### LangChain Integration

```python
from agentmeter import LangChainAgentMeterCallback

callback = LangChainAgentMeterCallback(
    client=client,
    project_id="proj_123",
    agent_id="langchain_agent"
)

# Use with LangChain
llm = OpenAI(callbacks=[callback])
result = llm("What is machine learning?")
```

## 📈 Best Practices

### 1. Choose the Right Payment Model
- **API Request Pay**: For well-defined API endpoints
- **Token-based Pay**: For AI/ML services with variable token usage  
- **Instant Pay**: For premium features and one-time charges

### 2. Use Appropriate Tracking Methods
- **Decorators**: For function-level tracking
- **Context Managers**: For code block tracking
- **Direct Calls**: For explicit control
- **Batch Tracking**: For high-volume scenarios

### 3. Handle Errors Gracefully
```python
try:
    with track_api_request_pay(client, project_id, agent_id) as usage:
        result = your_api_call()
        usage["metadata"]["success"] = True
        return result
except Exception as e:
    # AgentMeter tracking won't interfere with your app
    print(f"API call failed: {e}")
    raise
```

### 4. Monitor Usage Limits
```python
def check_user_limit(user_id):
    meter = client.get_user_meter(user_id=user_id)
    usage_percent = (meter.current_usage / meter.threshold_amount) * 100
    
    if usage_percent > 90:
        return {"status": "limit_exceeded", "message": "Usage limit reached"}
    elif usage_percent > 75:
        return {"status": "warning", "message": "Approaching limit"}
    else:
        return {"status": "ok", "remaining": meter.threshold_amount - meter.current_usage}
```

## 🧪 Testing

Run the example scripts:

```bash
# Basic usage examples
python examples/basic_usage.py

# E-commerce integration example
python examples/ecommerce_integration.py

# LangChain integration example
python examples/langchain_integration.py
```

Run tests:

```bash
pytest tests/
```

## 📚 API Reference

### Core Classes
- `AgentMeterClient` - Main client for API interactions
- `AgentMeterTracker` - Batch tracking with auto-flush
- `AgentMeterConfig` - Configuration management

### Payment Models
- `APIRequestPayEvent` - API request payment events
- `TokenBasedPayEvent` - Token-based payment events  
- `InstantPayEvent` - Instant payment events

### Decorators
- `@meter_api_request_pay` - API request payment decorator
- `@meter_token_based_pay` - Token-based payment decorator
- `@meter_instant_pay` - Instant payment decorator
- `@meter_agent` - Class-level metering decorator

### Context Managers
- `track_api_request_pay()` - API request payment tracking
- `track_token_based_pay()` - Token-based payment tracking
- `track_instant_pay()` - Instant payment tracking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [AgentMeter Platform](https://agentmeter.money)
- [API Documentation](https://docs.agentmeter.money)
- [Support](mailto:support@agentmeter.com)
- [Status Page](https://status.agentmeter.com)

## 🆘 Support

For support or questions:
- 📧 Email: support@agentmeter.com
- 💬 Discord: [Join our community](https://discord.gg/agentmeter)
- 📖 Documentation: [docs.agentmeter.money](https://docs.agentmeter.money)

---

Made with ❤️ by the AgentMeter team