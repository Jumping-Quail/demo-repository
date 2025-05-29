@app.route('/test')
def test():
    """Test endpoint for quick verification"""
    return jsonify({
        "status": "success",
        "message": "API is working correctly",
        "test_data": {
            "repository": "demo-repository",
            "analysis_tools": ["mistral-ai", "openai", "code-quality", "security"],
            "features": ["interactive-dashboard", "rest-api", "automated-analysis", "rag-system", "comparative-analysis"]
        },
        "api_version": "1.1.0"
    })

@app.route('/metrics')
def metrics():
    """Metrics endpoint for monitoring"""
    # This would normally integrate with a proper monitoring system
    # For now, we'll just return some basic stats
    stats = {
        "uptime_seconds": 3600,  # Placeholder
        "requests": {
            "total": 1000,  # Placeholder
            "success": 950,  # Placeholder
            "error": 50,  # Placeholder
        },
        "endpoints": {
            "/analyze": 200,  # Placeholder
            "/openai-analyze": 150,  # Placeholder
            "/compare-analysis": 100,  # Placeholder
            "/rag-query": 300,  # Placeholder
            "/results": 250,  # Placeholder
        },
        "rate_limits": {
            "current": limiter.current_limit,
            "remaining": "N/A"  # Would require integration with limiter storage
        }
    }
    
    return jsonify({
        "status": "success",
        "metrics": stats
    })

if __name__ == '__main__':
    print("Starting AI Repository Analysis API Server...")
    print("Available endpoints:")
    print("  GET  /         - API information")
    print("  GET  /health   - Health check")
    print("  POST /analyze  - Run Mistral analysis")
    print("  POST /openai-analyze - Run OpenAI analysis")
    print("  POST /compare-analysis - Compare analyses")
    print("  POST /rag-query - Query the RAG system")
    print("  GET  /results  - Get results")
    print("  GET  /dashboard- Dashboard info")
    print("  GET  /test     - Test endpoint")
    print("\nServer starting on http://0.0.0.0:3000")
    
    app.run(host='0.0.0.0', port=3000, debug=False)
