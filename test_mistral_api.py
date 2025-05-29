#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Mistral AI API integration
This script tests both simulation mode and real API mode
"""

import os
from mistral_integration import MistralRepositoryAnalyzer

def test_simulation_mode():
    """Test the analyzer in simulation mode (no API key)"""
    print("🧪 Testing Simulation Mode")
    print("=" * 50)
    
    analyzer = MistralRepositoryAnalyzer()
    report = analyzer.generate_comprehensive_report()
    
    print(f"✅ Simulation mode test completed")
    print(f"   Report sections: {list(report.keys())}")
    print(f"   Analysis results: {list(report['analysis_results'].keys())}")
    
    return report

def test_real_api_mode():
    """Test the analyzer with real API (if key is available)"""
    print("\n🔗 Testing Real API Mode")
    print("=" * 50)
    
    # Check for API key in environment
    api_key = os.getenv('MISTRAL_API_KEY') or os.getenv('MISTRALAI_API_KEY')
    
    if not api_key:
        print("⚠️  No Mistral API key found in environment variables")
        print("   Set MISTRAL_API_KEY or MISTRALAI_API_KEY to test real API")
        return None
    
    print(f"✅ Found API key: {api_key[:10]}...")
    
    try:
        analyzer = MistralRepositoryAnalyzer(api_key=api_key)
        report = analyzer.generate_comprehensive_report()
        
        print(f"✅ Real API mode test completed")
        print(f"   Report sections: {list(report.keys())}")
        print(f"   Analysis results: {list(report['analysis_results'].keys())}")
        
        # Check if responses contain AI-powered indicators
        for analysis_type, data in report['analysis_results'].items():
            if isinstance(data, dict) and data.get('ai_powered'):
                print(f"   🤖 {analysis_type}: Real AI analysis detected")
        
        return report
        
    except Exception as e:
        print(f"❌ Error testing real API: {e}")
        return None

def compare_modes(sim_report, api_report):
    """Compare simulation and real API results"""
    if not api_report:
        print("\n📊 Comparison skipped (no real API results)")
        return
    
    print("\n📊 Comparing Simulation vs Real API")
    print("=" * 50)
    
    sim_keys = set(sim_report['analysis_results'].keys())
    api_keys = set(api_report['analysis_results'].keys())
    
    print(f"Simulation analysis types: {sim_keys}")
    print(f"Real API analysis types: {api_keys}")
    
    common_keys = sim_keys.intersection(api_keys)
    print(f"Common analysis types: {common_keys}")
    
    for key in common_keys:
        sim_data = sim_report['analysis_results'][key]
        api_data = api_report['analysis_results'][key]
        
        print(f"\n{key.upper()}:")
        print(f"  Simulation: {type(sim_data).__name__} with {len(sim_data) if isinstance(sim_data, dict) else 'N/A'} fields")
        print(f"  Real API: {type(api_data).__name__} with {len(api_data) if isinstance(api_data, dict) else 'N/A'} fields")
        
        if isinstance(api_data, dict) and api_data.get('ai_powered'):
            print(f"  ✅ Real AI analysis confirmed")

def main():
    """Main test function"""
    print("🚀 Mistral AI Integration Test Suite")
    print("=" * 60)
    
    # Test simulation mode
    sim_report = test_simulation_mode()
    
    # Test real API mode
    api_report = test_real_api_mode()
    
    # Compare results
    compare_modes(sim_report, api_report)
    
    print("\n" + "=" * 60)
    print("🏁 Test Suite Complete")
    
    if api_report:
        print("✅ Both simulation and real API modes working")
    else:
        print("⚠️  Only simulation mode tested (no API key)")
    
    print("\nTo test with real Mistral AI:")
    print("  export MISTRAL_API_KEY='your-api-key-here'")
    print("  python test_mistral_api.py")

if __name__ == "__main__":
    main()