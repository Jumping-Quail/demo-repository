# Mistral AI Integration Guide

This guide explains how to use the Mistral AI integration in this repository for real repository analysis.

## 🚀 Quick Start

### 1. Start the API Server

```bash
python api_server.py
```

The server will start on `http://localhost:3000` (or 3000 if available).

### 2. Test the Integration

#### Option A: Using Environment Variable (Recommended)

```bash
# Set your Mistral API key
export MISTRAL_API_KEY='your-mistral-api-key-here'

# Run the comprehensive test
python test_real_mistral.py
```

#### Option B: Using API Endpoints Directly

```bash
# Test the integration
curl -X POST http://localhost:3001/mistral-test \
     -H "Content-Type: application/json" \
     -d '{"api_key": "your-mistral-api-key-here"}'

# Run full analysis
curl -X POST http://localhost:3001/mistral-analyze \
     -H "Content-Type: application/json" \
     -d '{"api_key": "your-mistral-api-key-here"}'
```

## 📋 Available Endpoints

### Core Endpoints

- `GET /` - API documentation and endpoint list
- `GET /health` - Health check
- `GET /test` - Basic functionality test

### Analysis Endpoints

- `GET /analyze` - Run repository analysis (simulation mode)
- `GET /results` - Get latest analysis results
- `GET /dashboard` - Interactive web dashboard

### Mistral AI Endpoints

- `POST /mistral-test` - Test Mistral AI integration
- `POST /mistral-analyze` - Full repository analysis with Mistral AI

## 🔑 API Key Configuration

### Method 1: Environment Variable

```bash
export MISTRAL_API_KEY='your-api-key-here'
```

### Method 2: API Parameter

Include the API key in your POST request:

```json
{
  "api_key": "your-api-key-here"
}
```

## 🧪 Testing

### Comprehensive Test Suite

```bash
# Test all functionality
python test_real_mistral.py
```

### Individual Tests

```bash
# Test API endpoints
python test_api.py

# Test Mistral integration specifically
python test_mistral_api.py
```

## 📊 Analysis Output

The Mistral AI analysis provides:

### Code Quality Analysis
- Overall quality score (0-10)
- Strengths and weaknesses
- Security assessment
- Improvement recommendations

### Technology Stack Analysis
- Languages and frameworks detected
- Package managers and tools
- Modernization suggestions

### Architecture Analysis
- Project structure assessment
- Design patterns identified
- Scalability recommendations

### Documentation Analysis
- Documentation quality score
- Missing documentation areas
- Improvement suggestions

## 🔄 Modes of Operation

### 1. Simulation Mode
- No API key required
- Uses pre-generated realistic responses
- Perfect for testing and development
- Instant results

### 2. Real API Mode
- Requires valid Mistral API key
- Uses actual Mistral AI models
- Real-time analysis
- More detailed and accurate results

### 3. Hybrid Mode
- Attempts real API first
- Falls back to simulation on error
- Best of both worlds
- Robust error handling

## 📈 Example Usage

### Python Script

```python
import requests

# Test the integration
response = requests.post(
    'http://localhost:3001/mistral-test',
    json={'api_key': 'your-api-key-here'}
)

result = response.json()
print(f"Status: {result['status']}")
print(f"Output: {result['output']}")
```

### Command Line

```bash
# Quick test
curl -s -X POST http://localhost:3001/mistral-test \
     -H "Content-Type: application/json" \
     -d '{"api_key": "your-key"}' | jq .

# Full analysis with clean JSON output
python run_mistral_analysis.py
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Server Not Running**
   ```bash
   python api_server.py
   ```

2. **Invalid API Key**
   - Check your Mistral API key
   - Verify it's correctly set in environment or request

3. **Port Already in Use**
   - The server will try port 3001 if 3000 is busy
   - Check the console output for the actual port

4. **Network Issues**
   - Check internet connection for real API calls
   - Simulation mode works offline

### Debug Mode

Enable debug logging:

```bash
export FLASK_DEBUG=1
python api_server.py
```

## 🔧 Configuration

### Environment Variables

- `MISTRAL_API_KEY` - Your Mistral AI API key
- `FLASK_DEBUG` - Enable debug mode (optional)
- `PORT` - Custom port for API server (optional)

### API Configuration

The integration uses:
- Model: `mistral-large-latest`
- Max tokens: 2000
- Temperature: 0.3 (focused, deterministic responses)

## 📚 Additional Resources

- [Mistral AI Documentation](https://docs.mistral.ai/)
- [API Reference](./API_TESTING_RESULTS.md)
- [Repository Analysis Results](./README.md#analysis-results)

## 🤝 Contributing

To extend the Mistral AI integration:

1. Modify `mistral_integration.py` for core functionality
2. Update `api_server.py` for new endpoints
3. Add tests to `test_mistral_api.py`
4. Update this documentation

## 📄 License

This integration follows the same license as the main repository.