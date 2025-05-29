#!/usr/bin/env python3
"""
Repository Analysis Tool using OpenAI
Analyzes the repository structure, code quality, and provides insights.
Mirrors the structure of analyze_repo.py but uses OpenAI instead of Mistral.
"""

import os
import json
import time
from pathlib import Path
import subprocess
from typing import Dict, Any, List, Optional

from openai_config import get_client, OpenAIClient

class OpenAIRepositoryAnalyzer:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the OpenAI Repository Analyzer.
        
        Args:
            api_key: OpenAI API key. If None, uses the environment variable.
            model: OpenAI model to use. If None, uses the default model.
        """
        try:
            self.openai_client = OpenAIClient(api_key=api_key, model=model)
        except ValueError as e:
            print(f"Error initializing OpenAI client: {str(e)}")
            print("Analysis will be simulated without API calls.")
            self.openai_client = None
            
        self.repo_path = Path(".")
        self.analysis_results = {}
        
    def collect_repository_info(self):
        """Collect comprehensive repository information"""
        print("📂 Collecting repository information...")
        info = {
            "structure": self.get_file_structure(),
            "content": self.get_file_contents(),
            "git_info": self.get_git_info(),
            "dependencies": self.get_dependencies(),
            "workflows": self.get_github_workflows()
        }
        return info
    
    def get_file_structure(self):
        """Get repository file structure"""
        structure = []
        for root, dirs, files in os.walk("."):
            # Skip .git directory and other hidden directories
            if any(part.startswith('.') for part in root.split(os.sep)):
                continue
            level = root.replace(".", "").count(os.sep)
            indent = " " * 2 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files:
                if not file.startswith('.'):
                    structure.append(f"{subindent}{file}")
        return "\n".join(structure)
    
    def get_file_contents(self):
        """Get contents of key files"""
        key_files = ["README.md", "package.json", "index.html"]
        contents = {}
        
        for file in key_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        contents[file] = f.read()
                except Exception as e:
                    contents[file] = f"Error reading file: {str(e)}"
        
        # Get workflow files
        workflow_dir = Path(".github/workflows")
        if workflow_dir.exists():
            for workflow_file in workflow_dir.glob("*.yml"):
                try:
                    with open(workflow_file, 'r', encoding='utf-8') as f:
                        contents[str(workflow_file)] = f.read()
                except Exception as e:
                    contents[str(workflow_file)] = f"Error reading file: {str(e)}"
        
        # Get Python files (limited to avoid token limits)
        python_files = list(Path(".").glob("**/*.py"))[:5]  # Limit to 5 Python files
        for py_file in python_files:
            if ".git" not in str(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        contents[str(py_file)] = f.read()
                except Exception as e:
                    contents[str(py_file)] = f"Error reading file: {str(e)}"
        
        return contents
    
    def get_git_info(self):
        """Get git repository information"""
        try:
            # Get remote info
            remote_result = subprocess.run(
                ["git", "remote", "-v"], 
                capture_output=True, 
                text=True, 
                cwd="."
            )
            
            # Get branch info
            branch_result = subprocess.run(
                ["git", "branch"], 
                capture_output=True, 
                text=True, 
                cwd="."
            )
            
            # Get commit info
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-5"], 
                capture_output=True, 
                text=True, 
                cwd="."
            )
            
            return {
                "remotes": remote_result.stdout,
                "branches": branch_result.stdout,
                "recent_commits": log_result.stdout
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_dependencies(self):
        """Analyze dependencies"""
        deps = {}
        
        # Check package.json for npm dependencies
        if os.path.exists("package.json"):
            try:
                with open("package.json", 'r') as f:
                    package_data = json.load(f)
                    deps["npm"] = package_data.get("dependencies", {})
                    deps["dev_dependencies"] = package_data.get("devDependencies", {})
            except Exception as e:
                deps["npm_error"] = str(e)
        
        # Check requirements.txt for Python dependencies
        if os.path.exists("requirements.txt"):
            try:
                with open("requirements.txt", 'r') as f:
                    requirements = f.read().splitlines()
                    deps["python"] = requirements
            except Exception as e:
                deps["python_error"] = str(e)
        
        return deps
    
    def get_github_workflows(self):
        """Analyze GitHub Actions workflows"""
        workflows = {}
        workflow_dir = Path(".github/workflows")
        
        if workflow_dir.exists():
            for workflow_file in workflow_dir.glob("*.yml"):
                workflows[workflow_file.name] = {
                    "path": str(workflow_file),
                    "exists": True
                }
        
        return workflows
    
    def analyze_with_openai(self, repo_info):
        """Analyze repository using OpenAI"""
        if self.openai_client is None:
            return self._simulate_analysis(repo_info)
        
        print("🧠 Analyzing repository with OpenAI...")
        
        # Prepare the prompt with repository information
        structure = repo_info["structure"]
        
        # Get a sample of file contents to avoid token limits
        content_sample = {}
        for key, content in repo_info["content"].items():
            if len(content) > 1000:
                content_sample[key] = content[:1000] + "... (truncated)"
            else:
                content_sample[key] = content
        
        # Create the analysis prompt
        prompt = f"""
        Analyze this GitHub repository based on the following information:
        
        FILE STRUCTURE:
        {structure}
        
        KEY FILE CONTENTS (samples):
        {json.dumps(content_sample, indent=2)}
        
        DEPENDENCIES:
        {json.dumps(repo_info["dependencies"], indent=2)}
        
        GITHUB WORKFLOWS:
        {json.dumps(repo_info["workflows"], indent=2)}
        
        Provide a comprehensive analysis including:
        1. Repository type and primary purpose
        2. Technology stack identification
        3. Code quality assessment (structure, documentation, testing, CI/CD)
        4. Security analysis
        5. Specific recommendations for improvement
        6. Analysis of GitHub workflows
        7. Scores for complexity (1-10), maintainability (1-10), and scalability potential (1-10)
        
        Format your response as a JSON object with the following structure:
        {
            "repository_type": "string",
            "primary_purpose": "string",
            "technology_stack": ["string"],
            "code_quality_assessment": {
                "structure": "string",
                "documentation": "string",
                "testing": "string",
                "ci_cd": "string"
            },
            "security_analysis": {
                "dependencies": "string",
                "workflows": "string",
                "secrets_management": "string"
            },
            "recommendations": ["string"],
            "workflow_analysis": {
                "workflow_name.yml": {
                    "purpose": "string",
                    "triggers": "string",
                    "security": "string"
                }
            },
            "complexity_score": "string (e.g., 'Low (1/10)')",
            "maintainability_score": "string (e.g., 'High (8/10)')",
            "scalability_potential": "string (e.g., 'Medium (5/10)')"
        }
        """
        
        try:
            # Call OpenAI API
            response = self.openai_client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a code analysis expert that provides detailed repository analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            # Extract and parse the JSON response
            analysis_text = response.choices[0].message.content
            analysis = json.loads(analysis_text)
            
            return analysis
        except Exception as e:
            print(f"Error during OpenAI analysis: {str(e)}")
            return self._simulate_analysis(repo_info)
    
    def _simulate_analysis(self, repo_info):
        """Simulate OpenAI analysis when API is not available"""
        print("⚠️ Using simulated analysis (OpenAI API not available)")
        
        # This would normally call OpenAI API
        # For demo purposes, we'll provide a structured analysis
        analysis = {
            "repository_type": "GitHub Demo Repository",
            "primary_purpose": "Demonstration of GitHub features and AI-powered code analysis",
            "technology_stack": [
                "Python",
                "Flask",
                "HTML",
                "CSS (Primer CSS framework)",
                "GitHub Actions",
                "Node.js/npm (package management)"
            ],
            "code_quality_assessment": {
                "structure": "Well-organized with clear separation of concerns",
                "documentation": "Good README with comprehensive documentation",
                "testing": "Limited test coverage detected",
                "ci_cd": "GitHub Actions workflows present for basic CI"
            },
            "security_analysis": {
                "dependencies": "Modern dependencies with no obvious vulnerabilities",
                "workflows": "Standard GitHub Actions with appropriate permissions",
                "secrets_management": "Uses environment variables for API keys"
            },
            "recommendations": [
                "Implement comprehensive test suite",
                "Add input validation for API endpoints",
                "Consider containerization for consistent deployment",
                "Implement structured logging",
                "Add code quality checks to workflows"
            ],
            "workflow_analysis": {
                "auto-assign.yml": {
                    "purpose": "Automatically assigns issues and PRs",
                    "triggers": "On issue/PR creation",
                    "security": "Appropriate permissions set"
                },
                "proof-html.yml": {
                    "purpose": "HTML validation",
                    "triggers": "On push and manual dispatch",
                    "tool": "anishathalye/proof-html action"
                }
            },
            "complexity_score": "Medium (5/10)",
            "maintainability_score": "High (8/10)",
            "scalability_potential": "Medium (6/10)"
        }
        
        return analysis
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("🔍 Starting Repository Analysis with OpenAI...")
        start_time = time.time()
        
        # Collect repository information
        repo_info = self.collect_repository_info()
        
        # Analyze with OpenAI
        analysis = self.analyze_with_openai(repo_info)
        
        # Generate report
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "repository_info": repo_info,
            "openai_analysis": analysis,
            "analysis_duration_seconds": round(time.time() - start_time, 2)
        }
        
        return report
    
    def print_analysis(self, report):
        """Print formatted analysis results"""
        print("\n" + "="*60)
        print("📊 OPENAI REPOSITORY ANALYSIS REPORT")
        print("="*60)
        
        analysis = report["openai_analysis"]
        
        print(f"\n🏷️  Repository Type: {analysis['repository_type']}")
        print(f"🎯 Primary Purpose: {analysis['primary_purpose']}")
        
        print(f"\n🛠️  Technology Stack:")
        for tech in analysis['technology_stack']:
            print(f"   • {tech}")
        
        print(f"\n📈 Quality Assessment:")
        quality = analysis['code_quality_assessment']
        for key, value in quality.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🔒 Security Analysis:")
        security = analysis['security_analysis']
        for key, value in security.items():
            print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🔄 Workflow Analysis:")
        workflows = analysis['workflow_analysis']
        for workflow, details in workflows.items():
            print(f"   📋 {workflow}:")
            for key, value in details.items():
                print(f"      - {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n📊 Scores:")
        print(f"   • Complexity: {analysis['complexity_score']}")
        print(f"   • Maintainability: {analysis['maintainability_score']}")
        print(f"   • Scalability Potential: {analysis['scalability_potential']}")
        
        print(f"\n⏱️  Analysis Duration: {report['analysis_duration_seconds']} seconds")
        
        print("\n" + "="*60)
        print("✅ Analysis Complete!")
        print("="*60)

def main():
    """Main execution function"""
    analyzer = OpenAIRepositoryAnalyzer()
    report = analyzer.generate_report()
    analyzer.print_analysis(report)
    
    # Save detailed report to file
    with open("openai_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: openai_analysis_report.json")

if __name__ == "__main__":
    main()
