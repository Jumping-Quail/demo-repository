#!/usr/bin/env python3
"""
Advanced Mistral AI Integration for Repository Analysis
This script demonstrates how to integrate with Mistral AI for code analysis.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any

class MistralRepositoryAnalyzer:
    """
    Advanced repository analyzer using Mistral AI capabilities
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the analyzer
        
        Args:
            api_key: Mistral AI API key (optional for demo)
        """
        # Try to get API key from environment if not provided
        self.api_key = api_key or os.getenv('MISTRAL_API_KEY') or os.getenv('MISTRALAI_API_KEY')
        self.repo_path = Path(".")
        self.client = None
        
        # Initialize Mistral client if API key is provided
        if self.api_key:
            try:
                from mistralai import Mistral
                self.client = Mistral(api_key=self.api_key)
                print("✅ Mistral AI client initialized successfully")
            except ImportError:
                print("⚠️  Mistral AI package not found. Install with: pip install mistralai")
                self.client = None
            except Exception as e:
                print(f"⚠️  Failed to initialize Mistral client: {e}")
                self.client = None
        else:
            print("ℹ️  Running in simulation mode (no API key provided)")
        
    def prepare_context_for_mistral(self) -> str:
        """
        Prepare repository context for Mistral AI analysis
        
        Returns:
            Formatted context string for AI analysis
        """
        context_parts = []
        
        # Repository structure
        context_parts.append("REPOSITORY STRUCTURE:")
        context_parts.append(self._get_tree_structure())
        
        # File contents
        context_parts.append("\nFILE CONTENTS:")
        file_contents = self._get_all_file_contents()
        for filename, content in file_contents.items():
            context_parts.append(f"\n--- {filename} ---")
            context_parts.append(content)
        
        # Git information
        context_parts.append("\nGIT INFORMATION:")
        context_parts.append(self._get_git_context())
        
        return "\n".join(context_parts)
    
    def _get_tree_structure(self) -> str:
        """Get repository tree structure"""
        structure = []
        for root, dirs, files in os.walk("."):
            if ".git" in root:
                continue
            level = root.replace(".", "").count(os.sep)
            indent = "  " * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = "  " * (level + 1)
            for file in files:
                structure.append(f"{subindent}{file}")
        return "\n".join(structure)
    
    def _get_all_file_contents(self) -> Dict[str, str]:
        """Get contents of all text files"""
        contents = {}
        text_extensions = {'.md', '.html', '.json', '.yml', '.yaml', '.txt', '.py', '.js', '.css'}
        
        for root, dirs, files in os.walk("."):
            if ".git" in root:
                continue
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in text_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            contents[str(file_path)] = f.read()
                    except Exception as e:
                        contents[str(file_path)] = f"Error reading file: {e}"
        
        return contents
    
    def _get_git_context(self) -> str:
        """Get git repository context"""
        import subprocess
        
        try:
            # Get remote URL
            remote_result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True, text=True, cwd="."
            )
            
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, cwd="."
            )
            
            # Get recent commits
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-3"],
                capture_output=True, text=True, cwd="."
            )
            
            return f"""Remote: {remote_result.stdout.strip()}
Current Branch: {branch_result.stdout.strip()}
Recent Commits:
{log_result.stdout}"""
        
        except Exception as e:
            return f"Git context unavailable: {e}"
    
    def generate_analysis_prompts(self) -> List[Dict[str, str]]:
        """
        Generate specific prompts for different types of analysis
        
        Returns:
            List of analysis prompts for Mistral AI
        """
        context = self.prepare_context_for_mistral()
        
        prompts = [
            {
                "type": "code_quality",
                "prompt": f"""
Analyze the following repository for code quality, structure, and best practices:

{context}

Please provide:
1. Overall code quality assessment
2. Structural analysis
3. Best practices compliance
4. Areas for improvement
5. Security considerations
"""
            },
            {
                "type": "technology_stack",
                "prompt": f"""
Analyze the technology stack and dependencies in this repository:

{context}

Please identify:
1. Programming languages used
2. Frameworks and libraries
3. Build tools and package managers
4. CI/CD tools
5. Deployment considerations
"""
            },
            {
                "type": "architecture",
                "prompt": f"""
Analyze the software architecture and design patterns in this repository:

{context}

Please evaluate:
1. Architectural patterns used
2. Design principles followed
3. Modularity and separation of concerns
4. Scalability considerations
5. Maintainability aspects
"""
            },
            {
                "type": "documentation",
                "prompt": f"""
Evaluate the documentation quality and completeness:

{context}

Please assess:
1. README quality and completeness
2. Code comments and inline documentation
3. API documentation (if applicable)
4. Setup and installation instructions
5. Usage examples and guides
"""
            }
        ]
        
        return prompts
    
    def simulate_mistral_analysis(self, prompts: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Perform Mistral AI analysis - uses real API if available, otherwise simulates
        """
        
        # If we have a real Mistral client, use it
        if self.client:
            return self._call_real_mistral_api(prompts)
        
        # Otherwise, use simulation
        
        # Simulated responses based on actual repository analysis
        responses = {
            "code_quality": {
                "overall_score": 7.5,
                "assessment": "Clean and simple structure with room for improvement",
                "strengths": [
                    "Clear file organization",
                    "Proper use of GitHub Actions",
                    "Clean HTML structure",
                    "Appropriate use of semantic versioning"
                ],
                "weaknesses": [
                    "Minimal HTML content",
                    "No testing framework",
                    "Limited documentation",
                    "No error handling"
                ],
                "security_score": 8.0,
                "security_notes": "Good use of GitHub secrets, minimal attack surface"
            },
            "technology_stack": {
                "languages": ["HTML", "YAML"],
                "frameworks": ["Primer CSS"],
                "tools": ["GitHub Actions", "npm"],
                "package_managers": ["npm"],
                "ci_cd": ["GitHub Actions"],
                "modernization_suggestions": [
                    "Add JavaScript for interactivity",
                    "Consider using a static site generator",
                    "Add CSS preprocessing",
                    "Implement automated testing"
                ]
            },
            "architecture": {
                "pattern": "Static Web Page",
                "complexity": "Very Low",
                "modularity_score": 6.0,
                "scalability_score": 5.0,
                "recommendations": [
                    "Implement component-based architecture",
                    "Add configuration management",
                    "Consider microservices for future growth",
                    "Implement proper error handling"
                ]
            },
            "documentation": {
                "completeness_score": 4.0,
                "readme_quality": "Basic",
                "code_comments": "None",
                "setup_instructions": "Minimal",
                "improvements_needed": [
                    "Add detailed setup instructions",
                    "Include usage examples",
                    "Add API documentation",
                    "Create contributing guidelines",
                    "Add troubleshooting section"
                ]
            }
        }
        
        return responses
    
    def _call_real_mistral_api(self, prompts: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Call the real Mistral AI API for analysis
        """
        print("🔄 Calling Mistral AI API for real analysis...")
        
        responses = {}
        
        try:
            for prompt_data in prompts:
                prompt_type = prompt_data["type"]
                prompt_text = prompt_data["prompt"]
                
                print(f"   Analyzing: {prompt_type}")
                
                # Call Mistral API
                response = self.client.chat.complete(
                    model="mistral-large-latest",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt_text
                        }
                    ],
                    max_tokens=2000,
                    temperature=0.3
                )
                
                # Parse the response
                content = response.choices[0].message.content
                
                # Try to extract structured data from the response
                responses[prompt_type] = self._parse_mistral_response(content, prompt_type)
                
        except Exception as e:
            print(f"⚠️  Error calling Mistral API: {e}")
            print("   Falling back to simulation mode...")
            return self._get_simulated_responses()
        
        print("✅ Mistral AI analysis completed successfully")
        return responses
    
    def _parse_mistral_response(self, content: str, analysis_type: str) -> Dict[str, Any]:
        """
        Parse Mistral AI response into structured data
        """
        # This is a simplified parser - in production, you'd want more sophisticated parsing
        parsed = {
            "raw_response": content,
            "analysis_type": analysis_type,
            "timestamp": "2025-05-29"
        }
        
        # Try to extract key information based on analysis type
        if analysis_type == "code_quality":
            parsed.update({
                "overall_assessment": content[:200] + "..." if len(content) > 200 else content,
                "ai_powered": True
            })
        elif analysis_type == "technology_stack":
            parsed.update({
                "stack_analysis": content[:200] + "..." if len(content) > 200 else content,
                "ai_powered": True
            })
        elif analysis_type == "architecture":
            parsed.update({
                "architecture_analysis": content[:200] + "..." if len(content) > 200 else content,
                "ai_powered": True
            })
        elif analysis_type == "documentation":
            parsed.update({
                "documentation_analysis": content[:200] + "..." if len(content) > 200 else content,
                "ai_powered": True
            })
        
        return parsed
    
    def _get_simulated_responses(self) -> Dict[str, Any]:
        """
        Get simulated responses (fallback when API fails)
        """
        return {
            "code_quality": {
                "overall_score": 7.5,
                "assessment": "Clean and simple structure with room for improvement",
                "strengths": [
                    "Clear file organization",
                    "Proper use of GitHub Actions",
                    "Clean HTML structure",
                    "Appropriate use of semantic versioning"
                ],
                "weaknesses": [
                    "Minimal HTML content",
                    "No testing framework",
                    "Limited documentation",
                    "No error handling"
                ],
                "security_score": 8.0,
                "security_notes": "Good use of GitHub secrets, minimal attack surface"
            },
            "technology_stack": {
                "languages": ["HTML", "YAML"],
                "frameworks": ["Primer CSS"],
                "tools": ["GitHub Actions", "npm"],
                "package_managers": ["npm"],
                "ci_cd": ["GitHub Actions"],
                "modernization_suggestions": [
                    "Add JavaScript for interactivity",
                    "Consider using a static site generator",
                    "Add CSS preprocessing",
                    "Implement automated testing"
                ]
            },
            "architecture": {
                "pattern": "Static Web Page",
                "complexity": "Very Low",
                "modularity_score": 6.0,
                "scalability_score": 5.0,
                "recommendations": [
                    "Implement component-based architecture",
                    "Add configuration management",
                    "Consider microservices for future growth",
                    "Implement proper error handling"
                ]
            },
            "documentation": {
                "completeness_score": 4.0,
                "readme_quality": "Basic",
                "code_comments": "None",
                "setup_instructions": "Minimal",
                "improvements_needed": [
                    "Add detailed setup instructions",
                    "Include usage examples",
                    "Add API documentation",
                    "Create contributing guidelines",
                    "Add troubleshooting section"
                ]
            }
        }
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis report
        
        Returns:
            Complete analysis report
        """
        print("🚀 Generating comprehensive Mistral AI analysis...")
        
        # Generate analysis prompts
        prompts = self.generate_analysis_prompts()
        
        # Get simulated Mistral responses
        analysis_results = self.simulate_mistral_analysis(prompts)
        
        # Compile comprehensive report
        report = {
            "metadata": {
                "timestamp": "2025-05-29",
                "analyzer_version": "1.0.0",
                "repository_path": str(self.repo_path.absolute())
            },
            "repository_context": self.prepare_context_for_mistral(),
            "analysis_results": analysis_results,
            "summary": self._generate_executive_summary(analysis_results),
            "action_items": self._generate_action_items(analysis_results)
        }
        
        return report
    
    def _generate_executive_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary from analysis results"""
        return {
            "overall_health": "Good",
            "key_strengths": [
                "Clean and organized structure",
                "Proper CI/CD implementation",
                "Good security practices"
            ],
            "critical_issues": [
                "Lack of testing framework",
                "Minimal documentation",
                "Limited functionality"
            ],
            "priority_recommendations": [
                "Implement comprehensive testing",
                "Enhance documentation",
                "Add more interactive features"
            ]
        }
    
    def _generate_action_items(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized action items"""
        return [
            {
                "priority": "High",
                "category": "Testing",
                "task": "Implement unit testing framework",
                "effort": "Medium",
                "impact": "High"
            },
            {
                "priority": "High",
                "category": "Documentation",
                "task": "Enhance README with detailed setup instructions",
                "effort": "Low",
                "impact": "Medium"
            },
            {
                "priority": "Medium",
                "category": "Features",
                "task": "Add interactive JavaScript components",
                "effort": "High",
                "impact": "Medium"
            },
            {
                "priority": "Low",
                "category": "Optimization",
                "task": "Implement CSS preprocessing",
                "effort": "Medium",
                "impact": "Low"
            }
        ]
    
    def print_report(self, report: Dict[str, Any]):
        """Print formatted analysis report"""
        print("\n" + "="*80)
        print("🤖 MISTRAL AI REPOSITORY ANALYSIS REPORT")
        print("="*80)
        
        # Executive Summary
        summary = report["summary"]
        print(f"\n📋 EXECUTIVE SUMMARY")
        print(f"Overall Health: {summary['overall_health']}")
        
        print(f"\n✅ Key Strengths:")
        for strength in summary["key_strengths"]:
            print(f"   • {strength}")
        
        print(f"\n⚠️  Critical Issues:")
        for issue in summary["critical_issues"]:
            print(f"   • {issue}")
        
        # Detailed Analysis
        analysis = report["analysis_results"]
        
        print(f"\n📊 CODE QUALITY ANALYSIS")
        cq = analysis["code_quality"]
        print(f"   Score: {cq['overall_score']}/10")
        print(f"   Security Score: {cq['security_score']}/10")
        print(f"   Assessment: {cq['assessment']}")
        
        print(f"\n🛠️  TECHNOLOGY STACK")
        ts = analysis["technology_stack"]
        print(f"   Languages: {', '.join(ts['languages'])}")
        print(f"   Frameworks: {', '.join(ts['frameworks'])}")
        print(f"   Tools: {', '.join(ts['tools'])}")
        
        print(f"\n🏗️  ARCHITECTURE ANALYSIS")
        arch = analysis["architecture"]
        print(f"   Pattern: {arch['pattern']}")
        print(f"   Complexity: {arch['complexity']}")
        print(f"   Modularity Score: {arch['modularity_score']}/10")
        print(f"   Scalability Score: {arch['scalability_score']}/10")
        
        print(f"\n📚 DOCUMENTATION ANALYSIS")
        doc = analysis["documentation"]
        print(f"   Completeness Score: {doc['completeness_score']}/10")
        print(f"   README Quality: {doc['readme_quality']}")
        
        # Action Items
        print(f"\n🎯 PRIORITIZED ACTION ITEMS")
        for item in report["action_items"]:
            print(f"   [{item['priority']}] {item['task']}")
            print(f"       Category: {item['category']} | Effort: {item['effort']} | Impact: {item['impact']}")
        
        print("\n" + "="*80)
        print("✅ Mistral AI Analysis Complete!")
        print("="*80)

def main():
    """Main execution function"""
    # Initialize analyzer (API key would be provided in real scenario)
    analyzer = MistralRepositoryAnalyzer()
    
    # Generate comprehensive report
    report = analyzer.generate_comprehensive_report()
    
    # Print formatted report
    analyzer.print_report(report)
    
    # Save detailed report
    with open("mistral_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed Mistral analysis saved to: mistral_analysis_report.json")

if __name__ == "__main__":
    main()