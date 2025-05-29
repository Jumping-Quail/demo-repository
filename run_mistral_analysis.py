#!/usr/bin/env python3
"""
Silent Mistral analysis runner for API endpoints
Outputs only JSON to stdout, logs to stderr
"""

import sys
import json
from mistral_integration import MistralRepositoryAnalyzer

def main():
    """Run Mistral analysis and output JSON only"""
    try:
        # Temporarily redirect stdout to stderr to suppress print statements
        import io
        import contextlib
        
        # Capture stdout during analysis
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            # Create analyzer
            analyzer = MistralRepositoryAnalyzer()
            
            # Generate report
            report = analyzer.generate_comprehensive_report()
        
        # Output clean JSON to stdout
        print(json.dumps(report, indent=2))
        
    except Exception as e:
        # Log error to stderr
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()