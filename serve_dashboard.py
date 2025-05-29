#!/usr/bin/env python3
"""
Simple web server to serve the analysis dashboard
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def serve_dashboard(port=8000):
    """
    Serve the analysis dashboard on specified port
    
    Args:
        port: Port number to serve on
    """
    
    # Change to the repository directory
    os.chdir(Path(__file__).parent)
    
    # Create HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    
    # Enable CORS for iframe access
    class CORSRequestHandler(handler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            super().end_headers()
    
    with socketserver.TCPServer(("0.0.0.0", port), CORSRequestHandler) as httpd:
        print(f"🚀 Serving analysis dashboard at:")
        print(f"   Local: http://localhost:{port}/analysis_dashboard.html")
        print(f"   Network: http://0.0.0.0:{port}/analysis_dashboard.html")
        print(f"\n📊 Available files:")
        print(f"   • Analysis Dashboard: /analysis_dashboard.html")
        print(f"   • Original Demo: /index.html")
        print(f"   • Analysis Report: /analysis_report.json")
        print(f"   • Mistral Report: /mistral_analysis_report.json")
        print(f"\n🛑 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n✅ Server stopped")

if __name__ == "__main__":
    serve_dashboard(12000)  # Use the provided port