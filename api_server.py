@app.route('/compare-analysis', methods=['POST', 'GET'])
@limiter.limit("10 per hour")
def compare_analysis():
    """Compare Mistral and OpenAI analyses"""
    try:
        logger.info("Starting analysis comparison")
        # Run the comparison script
        result = subprocess.run([
            sys.executable, 'compare_analysis.py'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            # Try to load the generated comparison report
            try:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'comparison_report.json'), 'r') as f:
                    comparison_data = json.load(f)
                logger.info("Analysis comparison completed successfully")
                return jsonify({
                    "status": "success",
                    "message": "Analysis comparison completed successfully",
                    "data": comparison_data,
                    "visualizations": {
                        "score_comparison": "/visualizations/score_comparison.html",
                        "agreement_comparison": "/visualizations/agreement_comparison.html"
                    }
                })
            except FileNotFoundError:
                logger.warning("Analysis comparison completed but report file not found")
                return jsonify({
                    "status": "success",
                    "message": "Analysis comparison completed but report file not found",
                    "output": result.stdout
                })
        else:
            logger.error(f"Analysis comparison failed: {result.stderr}")
            return jsonify({
                "status": "error",
                "message": "Analysis comparison failed",
                "error": result.stderr,
                "output": result.stdout
            }), 500
            
    except Exception as e:
        logger.exception("Failed to run analysis comparison")
        return jsonify({
            "status": "error",
            "message": f"Failed to run analysis comparison: {str(e)}"
        }), 500
