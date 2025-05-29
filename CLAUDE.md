# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands

- `python analyze_repo.py` - Run basic repository analysis
- `python mistral_integration.py` - Run Mistral AI analysis
- `python serve_dashboard.py` - Start the dashboard server (available at http://localhost:12000/analysis_dashboard.html)
- `python api_server.py` - Start the API server (runs on port 3000)
- `python test_api.py` - Test the API endpoints
- `python test_mistral_api.py` - Test Mistral API integration
- `python test_openai_api.py` - Test OpenAI API integration
- `python compare_analysis.py` - Compare Mistral and OpenAI analyses
- `python run_mistral_analysis.py` - Run real Mistral analysis with API key
- `python -m pytest` - Run all tests

## Repository Architecture

### Core Components

1. **Analysis Engines**
   - `analyze_repo.py` - Basic repository analyzer
   - `mistral_integration.py` - Mistral AI-powered analyzer
   - `openai_config.py` - OpenAI configuration and integration

2. **API Server**
   - `api_server.py` - Flask-based API server
   - Endpoints for analysis, results, health checks, and dashboard access

3. **Dashboard & Visualization**
   - `serve_dashboard.py` - Simple HTTP server for dashboard
   - `analysis_dashboard.html` - Interactive web dashboard
   - Visualization components for analysis results

4. **Testing Framework**
   - `test_api.py` - API endpoint tests
   - `test_mistral_api.py` - Mistral integration tests
   - `test_openai_api.py` - OpenAI API tests
   - `test_real_mistral.py` - Tests with real Mistral API

5. **Comparison Tools**
   - `compare_analysis.py` - Compares Mistral and OpenAI analyses
   - Generates visualizations for comparative analysis

### Data Flow

1. Repository data is collected (file structure, content, git info)
2. Analysis is performed using Mistral AI or OpenAI (simulation or real API)
3. Results are stored in JSON format
4. Dashboard visualizes the analysis results
5. API server provides programmatic access to analysis functionality

## Environment Variables

- `MISTRAL_API_KEY` or `MISTRALAI_API_KEY` - Mistral AI API key
- `OPENAI_API_KEY` - OpenAI API key

## External Dependencies

The project uses these key dependencies:
- Flask and Flask-CORS for API server
- Mistral AI and OpenAI Python libraries
- Plotly for visualizations
- Requests for API testing

## Common Workflows

1. **Running Analysis**:
   - Set API keys in environment variables
   - Run `python analyze_repo.py` for basic analysis
   - Run `python mistral_integration.py` for AI-powered analysis

2. **Viewing Results**:
   - Start dashboard with `python serve_dashboard.py`
   - Open http://localhost:12000/analysis_dashboard.html

3. **API Integration**:
   - Start API server with `python api_server.py`
   - Test endpoints with `python test_api.py`

4. **Comparing AI Models**:
   - Run `python compare_analysis.py` to generate comparison report