#!/usr/bin/env python3
import sys
import os
from datetime import datetime
import re

def generate_html_report(results_file, output_file):
    """Generate HTML report from test results"""
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found")
        return
    
    with open(results_file, 'r') as f:
        content = f.read()
    
    # Parse summary stats
    total = cracked = weak = strong = 0
    lines = content.split('\n')
    for line in lines:
        if 'Total passwords tested:' in line:
            total = int(re.search(r'\d+', line).group())
        elif 'Passwords cracked:' in line:
            cracked = int(re.search(r'\d+', line).group())
        elif 'Weak passwords:' in line:
            weak = int(re.search(r'\d+', line).group())
        elif 'Strong passwords:' in line:
            strong = int(re.search(r'\d+', line).group())
    
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Password Strength Testing Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-box {{ flex: 1; padding: 20px; border-radius: 8px; text-align: center; }}
        .cracked {{ background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }}
        .weak {{ background: linear-gradient(135deg, #f39c12, #e67e22); color: white; }}
        .strong {{ background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; }}
        .total {{ background: linear-gradient(135deg, #3498db, #2980b9); color: white; }}
        pre {{ background: #f8f9fa; padding: 20px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Password Strength Testing Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-box total">
                <h3>Total Tested</h3>
                <h2>{total}</h2>
            </div>
            <div class="stat-box cracked">
                <h3>Cracked</h3>
                <h2>{cracked}</h2>
                <small>{cracked/total*100:.1f}%</small>
            </div>
            <div class="stat-box weak">
                <h3>Weak</h3>
                <h2>{weak}</h2>
                <small>{weak/total*100:.1f}%</small>
            </div>
            <div class="stat-box strong">
                <h3>Strong</h3>
                <h2>{strong}</h2>
                <small>{strong/total*100:.1f}%</small>
            </div>
        </div>
        
        <h2>📋 Detailed Results</h2>
        <pre>{content}</pre>
        
        <h2>✅ Recommendations</h2>
        <ul>
            <li>Enforce <strong>12+ character minimum</strong> length</li>
            <li>Require <strong>3+ character types</strong> (upper, lower, digits, symbols)</li>
            <li>Block <strong>common passwords</strong> (rockyou.txt, SecLists)</li>
            <li>Enable <strong>MFA</strong> for all accounts</li>
            <li>Conduct <strong>quarterly password audits</strong></li>
        </ul>
    </div>
</body>
</html>
    '''
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ HTML report generated: {output_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 generate_report.py <results_file> <output_file>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    output_file = sys.argv[2]
    
    generate_html_report(results_file, output_file)

if __name__ == "__main__":
    main()
