#!/usr/bin/env python3
"""
API Server for Mistral AI Repository Analysis
Provides REST endpoints for testing the analysis functionality
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import subprocess
import sys

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        "service": "Mistral AI Repository Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/": "This help message",
            "/health": "Health check",
            "/analyze": "Run repository analysis",
            "/results": "Get latest analysis results",
            "/dashboard": "Redirect to analysis dashboard"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "mistral-ai-analysis",
        "timestamp": "2025-05-29T13:54:11Z"
    })

@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    """Run repository analysis"""
    try:
        # Run the analysis script
        result = subprocess.run([
            sys.executable, 'analyze_repo.py'
        ], capture_output=True, text=True, cwd='/workspace/demo-repository')
        
        if result.returncode == 0:
            # Try to load the generated report
            try:
                with open('/workspace/demo-repository/analysis_report.json', 'r') as f:
                    analysis_data = json.load(f)
                return jsonify({
                    "status": "success",
                    "message": "Analysis completed successfully",
                    "data": analysis_data
                })
            except FileNotFoundError:
                return jsonify({
                    "status": "success",
                    "message": "Analysis completed but report file not found",
                    "output": result.stdout
                })
        else:
            return jsonify({
                "status": "error",
                "message": "Analysis failed",
                "error": result.stderr,
                "output": result.stdout
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to run analysis: {str(e)}"
        }), 500

@app.route('/results')
def results():
    """Get latest analysis results"""
    try:
        # Try to load both report files
        reports = {}
        
        if os.path.exists('/workspace/demo-repository/analysis_report.json'):
            with open('/workspace/demo-repository/analysis_report.json', 'r') as f:
                reports['basic_analysis'] = json.load(f)
        
        if os.path.exists('/workspace/demo-repository/mistral_analysis_report.json'):
            with open('/workspace/demo-repository/mistral_analysis_report.json', 'r') as f:
                reports['mistral_analysis'] = json.load(f)
        
        if reports:
            return jsonify({
                "status": "success",
                "data": reports
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No analysis results found. Run /analyze first."
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to load results: {str(e)}"
        }), 500

@app.route('/dashboard')
def dashboard():
    """Redirect to analysis dashboard"""
    return jsonify({
        "status": "success",
        "message": "Dashboard available",
        "dashboard_url": "http://localhost:3000",
        "note": "Make sure the dashboard server is running with: python serve_dashboard.py"
    })

@app.route('/test')
def test():
    """Test endpoint for quick verification"""
    return jsonify({
        "status": "success",
        "message": "API is working correctly",
        "test_data": {
            "repository": "demo-repository",
            "analysis_tools": ["mistral-ai", "code-quality", "security"],
            "features": ["interactive-dashboard", "rest-api", "automated-analysis"]
        }
    })

if __name__ == '__main__':
    print("Starting Mistral AI Analysis API Server...")
    print("Available endpoints:")
    print("  GET  /         - API information")
    print("  GET  /health   - Health check")
    print("  POST /analyze  - Run analysis")
    print("  GET  /results  - Get results")
    print("  GET  /dashboard- Dashboard info")
    print("  GET  /test     - Test endpoint")
    print("\nServer starting on http://0.0.0.0:3001")
    
    app.run(host='0.0.0.0', port=3001, debug=False)