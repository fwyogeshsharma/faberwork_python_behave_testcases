"""
Test Report Generator for Faberwork Test Automation
Generates a comprehensive HTML report from Behave test results
"""

import json
import os
from datetime import datetime
from pathlib import Path


def generate_html_report(json_file, output_file):
    """Generate HTML report from JSON results"""

    # Load JSON results
    with open(json_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # Calculate statistics
    total_features = len(results)
    total_scenarios = sum(len(feature['elements']) for feature in results)
    passed_scenarios = 0
    failed_scenarios = 0
    skipped_scenarios = 0
    total_steps = 0
    passed_steps = 0
    failed_steps = 0
    skipped_steps = 0
    undefined_steps = 0

    feature_details = []

    for feature in results:
        feature_name = feature['name']
        feature_status = 'passed'
        feature_scenarios = []

        for scenario in feature['elements']:
            scenario_name = scenario['name']
            scenario_type = scenario['type']

            if scenario_type == 'background':
                continue

            scenario_status = 'passed'
            scenario_steps = []

            for step in scenario['steps']:
                total_steps += 1
                step_status = step['result']['status']

                if step_status == 'passed':
                    passed_steps += 1
                elif step_status == 'failed':
                    failed_steps += 1
                    scenario_status = 'failed'
                    feature_status = 'failed'
                elif step_status == 'skipped':
                    skipped_steps += 1
                    if scenario_status != 'failed':
                        scenario_status = 'skipped'
                elif step_status == 'undefined':
                    undefined_steps += 1
                    scenario_status = 'undefined'
                    feature_status = 'undefined'

                error_message = ''
                if 'error_message' in step['result']:
                    error_message = step['result']['error_message']

                scenario_steps.append({
                    'keyword': step['keyword'],
                    'name': step['name'],
                    'status': step_status,
                    'duration': step['result'].get('duration', 0),
                    'error': error_message
                })

            if scenario_status == 'passed':
                passed_scenarios += 1
            elif scenario_status == 'failed':
                failed_scenarios += 1
            else:
                skipped_scenarios += 1

            feature_scenarios.append({
                'name': scenario_name,
                'status': scenario_status,
                'steps': scenario_steps
            })

        feature_details.append({
            'name': feature_name,
            'status': feature_status,
            'scenarios': feature_scenarios
        })

    # Calculate success rate
    success_rate = (passed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0

    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Faberwork Test Automation Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}

        .stat-card.passed {{
            border-left-color: #48bb78;
        }}

        .stat-card.failed {{
            border-left-color: #f56565;
        }}

        .stat-card.skipped {{
            border-left-color: #ed8936;
        }}

        .stat-card h3 {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }}

        .success-rate {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .success-rate .percentage {{
            font-size: 4em;
            font-weight: bold;
            color: {'#48bb78' if success_rate >= 80 else '#ed8936' if success_rate >= 50 else '#f56565'};
        }}

        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e2e8f0;
            border-radius: 15px;
            overflow: hidden;
            margin-top: 20px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #48bb78, #38a169);
            transition: width 0.3s ease;
        }}

        .features {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .feature {{
            margin-bottom: 30px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }}

        .feature-header {{
            background: #f7fafc;
            padding: 20px;
            font-weight: bold;
            font-size: 1.1em;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .feature-header.passed {{
            background: #f0fff4;
            border-left: 4px solid #48bb78;
        }}

        .feature-header.failed {{
            background: #fff5f5;
            border-left: 4px solid #f56565;
        }}

        .scenario {{
            padding: 15px 20px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .scenario:last-child {{
            border-bottom: none;
        }}

        .scenario-header {{
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .status-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .status-badge.passed {{
            background: #c6f6d5;
            color: #22543d;
        }}

        .status-badge.failed {{
            background: #fed7d7;
            color: #742a2a;
        }}

        .status-badge.skipped {{
            background: #feebc8;
            color: #7c2d12;
        }}

        .status-badge.undefined {{
            background: #e2e8f0;
            color: #2d3748;
        }}

        .steps {{
            margin-top: 10px;
            padding-left: 20px;
        }}

        .step {{
            padding: 8px;
            margin: 4px 0;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}

        .step.passed {{
            background: #f0fff4;
        }}

        .step.failed {{
            background: #fff5f5;
            border-left: 3px solid #f56565;
        }}

        .step.skipped {{
            background: #fefcbf;
        }}

        .error-message {{
            background: #feb2b2;
            color: #742a2a;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            white-space: pre-wrap;
            word-break: break-word;
        }}

        .timestamp {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            padding: 20px;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .container {{
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Faberwork Test Automation Report</h1>
            <div class="subtitle">Comprehensive Test Execution Results</div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <h3>Total Features</h3>
                <div class="number">{total_features}</div>
            </div>
            <div class="stat-card">
                <h3>Total Scenarios</h3>
                <div class="number">{total_scenarios}</div>
            </div>
            <div class="stat-card passed">
                <h3>Passed Scenarios</h3>
                <div class="number">{passed_scenarios}</div>
            </div>
            <div class="stat-card failed">
                <h3>Failed Scenarios</h3>
                <div class="number">{failed_scenarios}</div>
            </div>
            <div class="stat-card skipped">
                <h3>Skipped Scenarios</h3>
                <div class="number">{skipped_scenarios}</div>
            </div>
            <div class="stat-card">
                <h3>Total Steps</h3>
                <div class="number">{total_steps}</div>
            </div>
            <div class="stat-card passed">
                <h3>Passed Steps</h3>
                <div class="number">{passed_steps}</div>
            </div>
            <div class="stat-card failed">
                <h3>Failed Steps</h3>
                <div class="number">{failed_steps}</div>
            </div>
        </div>

        <div class="success-rate">
            <h2>Success Rate</h2>
            <div class="percentage">{success_rate:.1f}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {success_rate}%"></div>
            </div>
        </div>

        <div class="features">
            <h2 style="margin-bottom: 20px;">📋 Detailed Test Results</h2>
"""

    # Add feature details
    for feature in feature_details:
        html_content += f"""
            <div class="feature">
                <div class="feature-header {feature['status']}">
                    <span class="status-badge {feature['status']}">{feature['status']}</span>
                    <span>{feature['name']}</span>
                </div>
"""

        for scenario in feature['scenarios']:
            html_content += f"""
                <div class="scenario">
                    <div class="scenario-header">
                        <span class="status-badge {scenario['status']}">{scenario['status']}</span>
                        <span>{scenario['name']}</span>
                    </div>
                    <div class="steps">
"""

            for step in scenario['steps']:
                html_content += f"""
                        <div class="step {step['status']}">
                            <strong>{step['keyword']}</strong> {step['name']}
"""
                if step['error']:
                    html_content += f"""
                            <div class="error-message">{step['error'][:500]}</div>
"""
                html_content += """
                        </div>
"""

            html_content += """
                    </div>
                </div>
"""

        html_content += """
            </div>
"""

    html_content += f"""
        </div>

        <div class="timestamp">
            <p>Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Test Environment: Production | Browser: Chrome (Headless)</p>
            <p>Base URL: https://www.faberwork.com</p>
        </div>
    </div>
</body>
</html>
"""

    # Write HTML report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML report generated: {output_file}")
    print(f"\n📊 Test Summary:")
    print(f"   Total Features: {total_features}")
    print(f"   Total Scenarios: {total_scenarios}")
    print(f"   Passed: {passed_scenarios} ({success_rate:.1f}%)")
    print(f"   Failed: {failed_scenarios}")
    print(f"   Skipped: {skipped_scenarios}")
    print(f"   Total Steps: {total_steps}")
    print(f"   Passed Steps: {passed_steps}")
    print(f"   Failed Steps: {failed_steps}")


if __name__ == "__main__":
    json_file = "reports/test_results.json"
    output_file = "reports/test_report.html"

    if os.path.exists(json_file):
        generate_html_report(json_file, output_file)
        print(f"\n🌐 Open the report in your browser:")
        print(f"   file:///{Path(output_file).resolve()}")
    else:
        print(f"❌ JSON results file not found: {json_file}")
        print("   Run tests first with: behave --format json --outfile reports/test_results.json")
