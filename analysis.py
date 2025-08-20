#!/usr/bin/env python3
"""
Financial Services CAC Analysis Script
Contact: 22f3002203@ds.study.iitm.ac.in
Purpose: Comprehensive analysis of Customer Acquisition Cost performance for 2024

This script performs complete analysis of quarterly CAC data and generates
visualizations and insights for executive decision-making.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import statistics
from datetime import datetime

class CACAnalysis:
    def __init__(self):
        """Initialize with 2024 quarterly CAC data"""
        # Quarterly CAC data for 2024
        self.quarterly_data = {
            'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
            'CAC': [225.6, 228.97, 234.24, 234.71]
        }
        
        # Industry benchmark
        self.target_cac = 150
        
        # Calculate average CAC - REQUIRED: 230.88
        self.average_cac = np.mean(self.quarterly_data['CAC'])
        
        print(f"Verification - Average CAC: ${self.average_cac:.2f}")
        print(f"Target CAC: ${self.target_cac}")
        print(f"Analysis Contact: 22f3002203@ds.study.iitm.ac.in")
    
    def perform_analysis(self):
        """Execute comprehensive CAC analysis"""
        print("\n" + "="*60)
        print("FINANCIAL SERVICES CAC ANALYSIS - 2024")
        print("="*60)
        
        # Create DataFrame
        df = pd.DataFrame(self.quarterly_data)
        df['Gap_to_Target'] = df['CAC'] - self.target_cac
        df['Percentage_Above_Target'] = ((df['CAC'] - self.target_cac) / self.target_cac * 100).round(2)
        
        print("\nQuarterly Performance:")
        print(df.to_string(index=False))
        
        # Statistical analysis
        cac_values = self.quarterly_data['CAC']
        stats = {
            'Mean CAC': np.mean(cac_values),
            'Median CAC': np.median(cac_values),
            'Standard Deviation': np.std(cac_values),
            'Min CAC': np.min(cac_values),
            'Max CAC': np.max(cac_values),
            'Range': np.max(cac_values) - np.min(cac_values),
            'Coefficient of Variation': (np.std(cac_values) / np.mean(cac_values)) * 100,
            'Total Gap from Target': self.average_cac - self.target_cac,
            'Percentage Above Target': ((self.average_cac - self.target_cac) / self.target_cac) * 100
        }
        
        print("\nStatistical Analysis:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key:.<30} ${value:.2f}")
            else:
                print(f"{key:.<30} {value}")
        
        return df, stats
    
    def create_visualizations(self, df):
        """Generate all required visualizations"""
        
        # 1. Trend Analysis Chart
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=df['Quarter'],
            y=df['CAC'],
            mode='lines+markers',
            name='Actual CAC',
            line=dict(color='red', width=3),
            marker=dict(size=10)
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=df['Quarter'],
            y=[self.target_cac] * len(df),
            mode='lines',
            name='Industry Target ($150)',
            line=dict(color='green', width=2, dash='dash')
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=df['Quarter'],
            y=[self.average_cac] * len(df),
            mode='lines',
            name=f'2024 Average (${self.average_cac:.2f})',
            line=dict(color='blue', width=2, dash='dot')
        ))
        
        fig_trend.update_layout(
            title='Customer Acquisition Cost (CAC) Trend Analysis - 2024',
            xaxis_title='Quarter',
            yaxis_title='CAC ($)',
            hovermode='x unified',
            height=500
        )
        
        # Save visualization
        fig_trend.write_html("cac_trend_analysis.html")
        print("\n✓ Trend analysis chart saved as 'cac_trend_analysis.html'")
        
        # 2. Gap Analysis Chart
        fig_gap = go.Figure()
        
        fig_gap.add_trace(go.Bar(
            x=df['Quarter'],
            y=df['Gap_to_Target'],
            name='Gap to Target ($)',
            marker_color='red',
            text=[f'${gap:.2f}' for gap in df['Gap_to_Target']],
            textposition='auto'
        ))
        
        fig_gap.update_layout(
            title='CAC Gap Analysis: Difference from Industry Target ($150)',
            xaxis_title='Quarter',
            yaxis_title='Gap to Target ($)',
            height=400
        )
        
        fig_gap.write_html("cac_gap_analysis.html")
        print("✓ Gap analysis chart saved as 'cac_gap_analysis.html'")
        
        # 3. Performance Dashboard
        fig_dashboard = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quarterly CAC Trend', 'Gap to Target', 'Percentage Above Target', 'Key Metrics'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "table"}]]
        )
        
        # Add traces to dashboard
        fig_dashboard.add_trace(
            go.Scatter(x=df['Quarter'], y=df['CAC'], mode='lines+markers', name='CAC', line=dict(color='red')),
            row=1, col=1
        )
        fig_dashboard.add_trace(
            go.Scatter(x=df['Quarter'], y=[self.target_cac]*len(df), mode='lines', name='Target', line=dict(color='green', dash='dash')),
            row=1, col=1
        )
        
        fig_dashboard.add_trace(
            go.Bar(x=df['Quarter'], y=df['Gap_to_Target'], name='Gap', marker_color='red'),
            row=1, col=2
        )
        
        fig_dashboard.add_trace(
            go.Bar(x=df['Quarter'], y=df['Percentage_Above_Target'], name='% Above Target', marker_color='orange'),
            row=2, col=1
        )
        
        # Add metrics table
        fig_dashboard.add_trace(
            go.Table(
                header=dict(values=['Metric', 'Value'], fill_color='lightblue'),
                cells=dict(values=[
                    ['Average CAC', 'Target CAC', 'Gap', '% Above Target', 'Q4 CAC'],
                    [f'${self.average_cac:.2f}', f'${self.target_cac}', f'${self.average_cac - self.target_cac:.2f}', 
                     f'{((self.average_cac - self.target_cac) / self.target_cac * 100):.1f}%', f'${df["CAC"].iloc[-1]}']
                ])
            ),
            row=2, col=2
        )
        
        fig_dashboard.update_layout(height=800, showlegend=False, title_text="CAC Performance Dashboard - 2024")
        fig_dashboard.write_html("cac_performance_dashboard.html")
        print("✓ Performance dashboard saved as 'cac_performance_dashboard.html'")
    
    def generate_insights_and_recommendations(self):
        """Generate business insights and strategic recommendations"""
        
        print("\n" + "="*60)
        print("BUSINESS INSIGHTS & RECOMMENDATIONS")
        print("="*60)
        
        print("\nKEY FINDINGS:")
        findings = [
            f"Average CAC of ${self.average_cac:.2f} is ${self.average_cac - self.target_cac:.2f} above industry target",
            f"Consistent upward trend from Q1 (${self.quarterly_data['CAC'][0]}) to Q4 (${self.quarterly_data['CAC'][-1]})",
            f"Company is paying {((self.average_cac - self.target_cac) / self.target_cac * 100):.1f}% premium over industry benchmark",
            "Rising marketing costs indicate urgent need for channel optimization"
        ]
        
        for i, finding in enumerate(findings, 1):
            print(f"{i}. {finding}")
        
        print("\nSTRATEGIC RECOMMENDATIONS:")
        recommendations = [
            "Implement data-driven attribution modeling to identify highest-ROI marketing channels",
            "Optimize digital marketing spend allocation based on channel-specific CAC performance", 
            "Deploy marketing automation and personalization to improve conversion rates",
            "Conduct comprehensive audit of underperforming marketing channels",
            "Establish real-time CAC monitoring dashboard with automated alerts",
            "Develop customer segmentation strategy for high-value, low-cost acquisition",
            "Launch A/B testing framework for continuous campaign optimization",
            "Negotiate better rates with marketing partners based on volume commitments"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        print("\nSOLUTION FOCUS: OPTIMIZE DIGITAL MARKETING CHANNELS")
        print("- Priority: Reallocate budget to highest-performing channels")
        print("- Target: Reduce CAC to $150 industry benchmark")
        print(f"- Potential Savings: ${self.average_cac - self.target_cac:.2f} per customer acquisition")

def main():
    """Main execution function"""
    print("Starting Financial Services CAC Analysis...")
    print("Analysis Contact: 22f3002203@ds.study.iitm.ac.in")
    
    # Initialize analyzer
    analyzer = CACAnalysis()
    
    # Perform comprehensive analysis
    df, stats = analyzer.perform_analysis()
    
    # Generate visualizations
    analyzer.create_visualizations(df)
    
    # Generate insights and recommendations
    analyzer.generate_insights_and_recommendations()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("Generated Files:")
    print("- cac_trend_analysis.html")
    print("- cac_gap_analysis.html") 
    print("- cac_performance_dashboard.html")
    print("\nVerification Email: 22f3002203@ds.study.iitm.ac.in")
    print(f"Average CAC (Required): ${analyzer.average_cac:.2f}")

if __name__ == "__main__":
    main()
