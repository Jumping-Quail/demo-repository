#!/usr/bin/env python3
"""
Comparative Analysis Module

This module compares analysis results from Mistral and OpenAI,
identifying similarities, differences, and generating comparative reports.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AnalysisComparator:
    def __init__(self, mistral_report_path: str = "analysis_report.json", 
                 openai_report_path: str = "openai_analysis_report.json"):
        """
        Initialize the Analysis Comparator.
        
        Args:
            mistral_report_path: Path to the Mistral analysis report JSON file.
            openai_report_path: Path to the OpenAI analysis report JSON file.
        """
        self.mistral_report_path = mistral_report_path
        self.openai_report_path = openai_report_path
        self.mistral_data = None
        self.openai_data = None
        self.comparison_results = {}
        
    def load_reports(self):
        """Load analysis reports from JSON files"""
        print("📂 Loading analysis reports...")
        
        # Load Mistral report
        if os.path.exists(self.mistral_report_path):
            try:
                with open(self.mistral_report_path, 'r') as f:
                    self.mistral_data = json.load(f)
                print(f"✅ Loaded Mistral report from {self.mistral_report_path}")
            except Exception as e:
                print(f"❌ Error loading Mistral report: {str(e)}")
                self.mistral_data = None
        else:
            print(f"❌ Mistral report not found at {self.mistral_report_path}")
            self.mistral_data = None
        
        # Load OpenAI report
        if os.path.exists(self.openai_report_path):
            try:
                with open(self.openai_report_path, 'r') as f:
                    self.openai_data = json.load(f)
                print(f"✅ Loaded OpenAI report from {self.openai_report_path}")
            except Exception as e:
                print(f"❌ Error loading OpenAI report: {str(e)}")
                self.openai_data = None
        else:
            print(f"❌ OpenAI report not found at {self.openai_report_path}")
            self.openai_data = None
        
        return self.mistral_data is not None and self.openai_data is not None
    
    def compare_analyses(self):
        """Compare Mistral and OpenAI analyses"""
        if not self.load_reports():
            print("❌ Cannot compare analyses: one or both reports are missing.")
            return False
        
        print("🔍 Comparing analyses...")
        
        # Extract the analysis sections
        mistral_analysis = self.mistral_data.get("mistral_analysis", {})
        openai_analysis = self.openai_data.get("openai_analysis", {})
        
        # Compare repository type and purpose
        self.comparison_results["repository_info"] = {
            "mistral": {
                "type": mistral_analysis.get("repository_type", "N/A"),
                "purpose": mistral_analysis.get("primary_purpose", "N/A")
            },
            "openai": {
                "type": openai_analysis.get("repository_type", "N/A"),
                "purpose": openai_analysis.get("primary_purpose", "N/A")
            },
            "agreement": self._calculate_text_similarity(
                mistral_analysis.get("repository_type", "") + " " + mistral_analysis.get("primary_purpose", ""),
                openai_analysis.get("repository_type", "") + " " + openai_analysis.get("primary_purpose", "")
            )
        }
        
        # Compare technology stack
        mistral_tech = set(mistral_analysis.get("technology_stack", []))
        openai_tech = set(openai_analysis.get("technology_stack", []))
        
        self.comparison_results["technology_stack"] = {
            "mistral": list(mistral_tech),
            "openai": list(openai_tech),
            "common": list(mistral_tech.intersection(openai_tech)),
            "mistral_only": list(mistral_tech - openai_tech),
            "openai_only": list(openai_tech - mistral_tech),
            "agreement_percentage": self._calculate_set_similarity(mistral_tech, openai_tech)
        }
        
        # Compare code quality assessment
        mistral_quality = mistral_analysis.get("code_quality_assessment", {})
        openai_quality = openai_analysis.get("code_quality_assessment", {})
        
        self.comparison_results["code_quality"] = {
            "mistral": mistral_quality,
            "openai": openai_quality,
            "agreement": {}
        }
        
        # Calculate agreement for each quality aspect
        for key in set(mistral_quality.keys()).union(set(openai_quality.keys())):
            mistral_value = mistral_quality.get(key, "N/A")
            openai_value = openai_quality.get(key, "N/A")
            
            if mistral_value != "N/A" and openai_value != "N/A":
                self.comparison_results["code_quality"]["agreement"][key] = self._calculate_text_similarity(
                    mistral_value, openai_value
                )
            else:
                self.comparison_results["code_quality"]["agreement"][key] = 0
        
        # Compare security analysis
        mistral_security = mistral_analysis.get("security_analysis", {})
        openai_security = openai_analysis.get("security_analysis", {})
        
        self.comparison_results["security_analysis"] = {
            "mistral": mistral_security,
            "openai": openai_security,
            "agreement": {}
        }
        
        # Calculate agreement for each security aspect
        for key in set(mistral_security.keys()).union(set(openai_security.keys())):
            mistral_value = mistral_security.get(key, "N/A")
            openai_value = openai_security.get(key, "N/A")
            
            if mistral_value != "N/A" and openai_value != "N/A":
                self.comparison_results["security_analysis"]["agreement"][key] = self._calculate_text_similarity(
                    mistral_value, openai_value
                )
            else:
                self.comparison_results["security_analysis"]["agreement"][key] = 0
        
        # Compare recommendations
        mistral_recs = mistral_analysis.get("recommendations", [])
        openai_recs = openai_analysis.get("recommendations", [])
        
        self.comparison_results["recommendations"] = {
            "mistral": mistral_recs,
            "openai": openai_recs,
            "common_themes": self._identify_common_themes(mistral_recs, openai_recs),
            "agreement_percentage": self._calculate_recommendation_similarity(mistral_recs, openai_recs)
        }
        
        # Compare scores
        mistral_scores = {
            "complexity": self._extract_score(mistral_analysis.get("complexity_score", "0")),
            "maintainability": self._extract_score(mistral_analysis.get("maintainability_score", "0")),
            "scalability": self._extract_score(mistral_analysis.get("scalability_potential", "0"))
        }
        
        openai_scores = {
            "complexity": self._extract_score(openai_analysis.get("complexity_score", "0")),
            "maintainability": self._extract_score(openai_analysis.get("maintainability_score", "0")),
            "scalability": self._extract_score(openai_analysis.get("scalability_potential", "0"))
        }
        
        self.comparison_results["scores"] = {
            "mistral": mistral_scores,
            "openai": openai_scores,
            "difference": {
                key: abs(mistral_scores[key] - openai_scores[key])
                for key in mistral_scores.keys()
            },
            "average_difference": sum(
                abs(mistral_scores[key] - openai_scores[key])
                for key in mistral_scores.keys()
            ) / len(mistral_scores) if mistral_scores else 0
        }
        
        # Add metadata
        self.comparison_results["metadata"] = {
            "comparison_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "mistral_report_path": self.mistral_report_path,
            "openai_report_path": self.openai_report_path,
            "overall_agreement_percentage": self._calculate_overall_agreement()
        }
        
        return True
    
    def _extract_score(self, score_text):
        """Extract numeric score from text like 'High (8/10)'"""
        try:
            if isinstance(score_text, (int, float)):
                return float(score_text)
            
            # Try to find a number in the format (X/10)
            import re
            match = re.search(r'(\d+)\/10', score_text)
            if match:
                return float(match.group(1))
            
            # Try to find any number
            match = re.search(r'(\d+(\.\d+)?)', score_text)
            if match:
                return float(match.group(1))
            
            # Map text ratings to numbers
            text_mapping = {
                "very low": 1,
                "low": 2,
                "medium-low": 3,
                "medium": 5,
                "medium-high": 7,
                "high": 8,
                "very high": 10
            }
            
            score_text_lower = score_text.lower()
            for text, value in text_mapping.items():
                if text in score_text_lower:
                    return value
            
            return 0
        except:
            return 0
    
    def _calculate_text_similarity(self, text1, text2):
        """Calculate simple similarity between two text strings"""
        # This is a very basic similarity measure
        # In a production system, you might use more sophisticated NLP techniques
        if not text1 or not text2:
            return 0
            
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def _calculate_set_similarity(self, set1, set2):
        """Calculate Jaccard similarity between two sets"""
        if not set1 or not set2:
            return 0
            
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return (intersection / union) * 100 if union else 0
    
    def _identify_common_themes(self, recs1, recs2):
        """Identify common themes in recommendations"""
        # This is a simplified implementation
        # In a production system, you might use topic modeling or clustering
        common_themes = []
        
        # Keywords to look for
        themes = {
            "testing": ["test", "testing", "unit test", "integration test"],
            "documentation": ["document", "documentation", "readme", "comment"],
            "security": ["security", "secure", "vulnerability", "auth", "authentication"],
            "performance": ["performance", "optimize", "optimization", "speed", "efficient"],
            "code quality": ["quality", "clean", "refactor", "maintainable", "readable"],
            "ci/cd": ["ci", "cd", "pipeline", "workflow", "github actions", "continuous"],
            "dependencies": ["dependency", "dependencies", "package", "library", "framework"]
        }
        
        # Combine all recommendations
        all_recs = " ".join(recs1 + recs2).lower()
        
        # Check for each theme
        for theme, keywords in themes.items():
            if any(keyword in all_recs for keyword in keywords):
                common_themes.append(theme)
        
        return common_themes
    
    def _calculate_recommendation_similarity(self, recs1, recs2):
        """Calculate similarity between recommendation lists"""
        if not recs1 or not recs2:
            return 0
            
        # Calculate pairwise similarities
        similarities = []
        for rec1 in recs1:
            for rec2 in recs2:
                similarities.append(self._calculate_text_similarity(rec1, rec2))
        
        # Return average of top N similarities where N is min(len(recs1), len(recs2))
        top_n = min(len(recs1), len(recs2))
        if not similarities or top_n == 0:
            return 0
            
        similarities.sort(reverse=True)
        return sum(similarities[:top_n]) / top_n * 100
    
    def _calculate_overall_agreement(self):
        """Calculate overall agreement percentage between analyses"""
        # Weights for different components
        weights = {
            "repository_info": 0.1,
            "technology_stack": 0.2,
            "code_quality": 0.2,
            "security_analysis": 0.2,
            "recommendations": 0.2,
            "scores": 0.1
        }
        
        agreement_scores = {
            "repository_info": self.comparison_results.get("repository_info", {}).get("agreement", 0) * 100,
            "technology_stack": self.comparison_results.get("technology_stack", {}).get("agreement_percentage", 0),
            "code_quality": sum(self.comparison_results.get("code_quality", {}).get("agreement", {}).values()) / 
                           max(len(self.comparison_results.get("code_quality", {}).get("agreement", {})), 1) * 100,
            "security_analysis": sum(self.comparison_results.get("security_analysis", {}).get("agreement", {}).values()) / 
                                max(len(self.comparison_results.get("security_analysis", {}).get("agreement", {})), 1) * 100,
            "recommendations": self.comparison_results.get("recommendations", {}).get("agreement_percentage", 0),
            "scores": (1 - min(self.comparison_results.get("scores", {}).get("average_difference", 10) / 10, 1)) * 100
        }
        
        weighted_sum = sum(agreement_scores[key] * weights[key] for key in weights)
        return weighted_sum
    
    def generate_comparison_report(self):
        """Generate a comprehensive comparison report"""
        if not self.comparison_results:
            if not self.compare_analyses():
                return None
        
        print("📊 Generating comparison report...")
        
        # Add overall summary
        overall_agreement = self.comparison_results["metadata"]["overall_agreement_percentage"]
        agreement_level = "High" if overall_agreement >= 75 else "Medium" if overall_agreement >= 50 else "Low"
        
        summary = {
            "overall_agreement": {
                "percentage": overall_agreement,
                "level": agreement_level,
                "interpretation": self._get_agreement_interpretation(overall_agreement)
            },
            "key_differences": self._identify_key_differences(),
            "key_agreements": self._identify_key_agreements(),
            "conclusion": self._generate_conclusion()
        }
        
        self.comparison_results["summary"] = summary
        
        return self.comparison_results
    
    def _get_agreement_interpretation(self, agreement_percentage):
        """Get interpretation of agreement percentage"""
        if agreement_percentage >= 80:
            return "The analyses from Mistral and OpenAI are highly consistent, suggesting strong confidence in the findings."
        elif agreement_percentage >= 60:
            return "The analyses show good consistency with some variations in specific areas."
        elif agreement_percentage >= 40:
            return "The analyses show moderate consistency with notable differences in several areas."
        else:
            return "The analyses show significant differences, suggesting the need for human review."
    
    def _identify_key_differences(self):
        """Identify key differences between analyses"""
        differences = []
        
        # Check technology stack differences
        mistral_only = self.comparison_results.get("technology_stack", {}).get("mistral_only", [])
        openai_only = self.comparison_results.get("technology_stack", {}).get("openai_only", [])
        
        if mistral_only:
            differences.append(f"Mistral identified {len(mistral_only)} technologies not found by OpenAI: {', '.join(mistral_only)}")
        
        if openai_only:
            differences.append(f"OpenAI identified {len(openai_only)} technologies not found by Mistral: {', '.join(openai_only)}")
        
        # Check score differences
        score_diff = self.comparison_results.get("scores", {}).get("difference", {})
        for metric, diff in score_diff.items():
            if diff >= 3:  # Significant difference threshold
                mistral_score = self.comparison_results.get("scores", {}).get("mistral", {}).get(metric, 0)
                openai_score = self.comparison_results.get("scores", {}).get("openai", {}).get(metric, 0)
                differences.append(f"Significant difference in {metric} score: Mistral ({mistral_score}/10) vs OpenAI ({openai_score}/10)")
        
        # Check recommendation differences
        mistral_recs = set(self.comparison_results.get("recommendations", {}).get("mistral", []))
        openai_recs = set(self.comparison_results.get("recommendations", {}).get("openai", []))
        
        if len(mistral_recs) != len(openai_recs):
            differences.append(f"Different number of recommendations: Mistral ({len(mistral_recs)}) vs OpenAI ({len(openai_recs)})")
        
        # If no significant differences found
        if not differences:
            differences.append("No significant differences found between the analyses.")
        
        return differences
    
    def _identify_key_agreements(self):
        """Identify key agreements between analyses"""
        agreements = []
        
        # Check technology stack agreements
        common_tech = self.comparison_results.get("technology_stack", {}).get("common", [])
        if common_tech:
            agreements.append(f"Both models identified {len(common_tech)} core technologies: {', '.join(common_tech)}")
        
        # Check common recommendation themes
        common_themes = self.comparison_results.get("recommendations", {}).get("common_themes", [])
        if common_themes:
            agreements.append(f"Both models recommended improvements in: {', '.join(common_themes)}")
        
        # Check score agreements
        score_diff = self.comparison_results.get("scores", {}).get("difference", {})
        for metric, diff in score_diff.items():
            if diff <= 1:  # Close agreement threshold
                mistral_score = self.comparison_results.get("scores", {}).get("mistral", {}).get(metric, 0)
                openai_score = self.comparison_results.get("scores", {}).get("openai", {}).get(metric, 0)
                agreements.append(f"Close agreement on {metric} score: Mistral ({mistral_score}/10) vs OpenAI ({openai_score}/10)")
        
        # If no significant agreements found
        if not agreements:
            agreements.append("No significant agreements found between the analyses.")
        
        return agreements
    
    def _generate_conclusion(self):
        """Generate a conclusion based on the comparison"""
        overall_agreement = self.comparison_results["metadata"]["overall_agreement_percentage"]
        
        if overall_agreement >= 75:
            return "The high level of agreement between Mistral and OpenAI analyses suggests strong confidence in the findings. The repository assessment is likely accurate and the recommendations should be prioritized."
        elif overall_agreement >= 50:
            return "The moderate agreement between Mistral and OpenAI analyses provides reasonable confidence in the shared findings. Areas of disagreement may benefit from human review."
        else:
            return "The significant differences between Mistral and OpenAI analyses suggest the need for careful human review before acting on the recommendations."
    
    def save_comparison_report(self, output_path="comparison_report.json"):
        """Save the comparison report to a JSON file"""
        if not self.comparison_results:
            if not self.generate_comparison_report():
                print("❌ Cannot save report: comparison failed.")
                return False
        
        try:
            with open(output_path, 'w') as f:
                json.dump(self.comparison_results, f, indent=2)
            print(f"✅ Comparison report saved to {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving comparison report: {str(e)}")
            return False
    
    def generate_visualizations(self, output_dir="./visualizations"):
        """Generate visualizations of the comparison results"""
        if not self.comparison_results:
            if not self.generate_comparison_report():
                print("❌ Cannot generate visualizations: comparison failed.")
                return False
        
        print("📊 Generating visualizations...")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate score comparison radar chart
        self._generate_score_radar_chart(os.path.join(output_dir, "score_comparison.html"))
        
        # Generate agreement bar chart
        self._generate_agreement_bar_chart(os.path.join(output_dir, "agreement_comparison.html"))
        
        print(f"✅ Visualizations saved to {output_dir}")
        return True
    
    def _generate_score_radar_chart(self, output_path):
        """Generate a radar chart comparing scores"""
        mistral_scores = self.comparison_results.get("scores", {}).get("mistral", {})
        openai_scores = self.comparison_results.get("scores", {}).get("openai", {})
        
        categories = list(mistral_scores.keys())
        mistral_values = [mistral_scores.get(cat, 0) for cat in categories]
        openai_values = [openai_scores.get(cat, 0) for cat in categories]
        
        # Add the first value at the end to close the loop
        categories.append(categories[0])
        mistral_values.append(mistral_values[0])
        openai_values.append(openai_values[0])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=mistral_values,
            theta=categories,
            fill='toself',
            name='Mistral'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=openai_values,
            theta=categories,
            fill='toself',
            name='OpenAI'
        ))
        
        fig.update_layout(
            title="Score Comparison: Mistral vs OpenAI",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True
        )
        
        fig.write_html(output_path)
    
    def _generate_agreement_bar_chart(self, output_path):
        """Generate a bar chart showing agreement percentages"""
        categories = [
            "Repository Info",
            "Technology Stack",
            "Code Quality",
            "Security Analysis",
            "Recommendations",
            "Scores",
            "Overall"
        ]
        
        agreement_values = [
            self.comparison_results.get("repository_info", {}).get("agreement", 0) * 100,
            self.comparison_results.get("technology_stack", {}).get("agreement_percentage", 0),
            sum(self.comparison_results.get("code_quality", {}).get("agreement", {}).values()) / 
            max(len(self.comparison_results.get("code_quality", {}).get("agreement", {})), 1) * 100,
            sum(self.comparison_results.get("security_analysis", {}).get("agreement", {}).values()) / 
            max(len(self.comparison_results.get("security_analysis", {}).get("agreement", {})), 1) * 100,
            self.comparison_results.get("recommendations", {}).get("agreement_percentage", 0),
            (1 - min(self.comparison_results.get("scores", {}).get("average_difference", 10) / 10, 1)) * 100,
            self.comparison_results.get("metadata", {}).get("overall_agreement_percentage", 0)
        ]
        
        colors = ['lightblue' if val < 50 else 'lightgreen' if val < 75 else 'green' for val in agreement_values]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=agreement_values,
                marker_color=colors
            )
        ])
        
        fig.update_layout(
            title="Agreement Percentage by Category",
            xaxis_title="Category",
            yaxis_title="Agreement (%)",
            yaxis=dict(range=[0, 100])
        )
        
        fig.write_html(output_path)
    
    def print_comparison_summary(self):
        """Print a summary of the comparison results"""
        if not self.comparison_results:
            if not self.generate_comparison_report():
                print("❌ Cannot print summary: comparison failed.")
                return
        
        summary = self.comparison_results.get("summary", {})
        
        print("\n" + "="*60)
        print("📊 ANALYSIS COMPARISON SUMMARY")
        print("="*60)
        
        # Print overall agreement
        overall = summary.get("overall_agreement", {})
        print(f"\n🔍 Overall Agreement: {overall.get('level', 'N/A')} ({overall.get('percentage', 0):.1f}%)")
        print(f"📝 {overall.get('interpretation', 'N/A')}")
        
        # Print key agreements
        print("\n✅ Key Agreements:")
        for agreement in summary.get("key_agreements", []):
            print(f"  • {agreement}")
        
        # Print key differences
        print("\n❓ Key Differences:")
        for difference in summary.get("key_differences", []):
            print(f"  • {difference}")
        
        # Print conclusion
        print(f"\n🎯 Conclusion:")
        print(f"  {summary.get('conclusion', 'N/A')}")
        
        print("\n" + "="*60)

def main():
    """Main execution function"""
    comparator = AnalysisComparator()
    comparator.generate_comparison_report()
    comparator.print_comparison_summary()
    comparator.save_comparison_report()
    comparator.generate_visualizations()

if __name__ == "__main__":
    main()
