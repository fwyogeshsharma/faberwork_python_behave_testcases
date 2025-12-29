#!/usr/bin/env python3
"""
HTML Report Generator from Behave JSON Results
Generates beautiful TestNG/JaCoCo-style HTML reports
"""

import json
import os
from pathlib import Path
from datetime import datetime
import base64


def load_json_results(json_file):
    """Load test results from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_statistics(features):
    """Calculate test statistics"""
    stats = {
        'total_features': len(features),
        'total_scenarios': 0,
        'passed_scenarios': 0,
        'failed_scenarios': 0,
        'skipped_scenarios': 0,
        'total_steps': 0,
        'passed_steps': 0,
        'failed_steps': 0,
        'skipped_steps': 0,
        'undefined_steps': 0,
        'total_duration': 0,
        'failed_features': [],
        'passed_features': [],
    }

    for feature in features:
        feature_failed = False
        feature_scenarios = 0

        for element in feature.get('elements', []):
            if element.get('type') == 'scenario':
                stats['total_scenarios'] += 1
                feature_scenarios += 1

                scenario_status = element.get('status', 'unknown')
                scenario_duration = element.get('duration', 0)
                stats['total_duration'] += scenario_duration

                if scenario_status == 'passed':
                    stats['passed_scenarios'] += 1
                elif scenario_status == 'failed':
                    stats['failed_scenarios'] += 1
                    feature_failed = True
                elif scenario_status == 'skipped':
                    stats['skipped_scenarios'] += 1

                for step in element.get('steps', []):
                    stats['total_steps'] += 1
                    step_status = step.get('result', {}).get('status', 'unknown')

                    if step_status == 'passed':
                        stats['passed_steps'] += 1
                    elif step_status == 'failed':
                        stats['failed_steps'] += 1
                    elif step_status == 'skipped':
                        stats['skipped_steps'] += 1
                    elif step_status == 'undefined':
                        stats['undefined_steps'] += 1

        if feature_scenarios > 0:
            if feature_failed:
                stats['failed_features'].append(feature)
            else:
                stats['passed_features'].append(feature)

    # Calculate success rate
    if stats['total_scenarios'] > 0:
        stats['success_rate'] = (stats['passed_scenarios'] / stats['total_scenarios']) * 100
    else:
        stats['success_rate'] = 0

    return stats


def format_duration(seconds):
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.2f}s"


def get_status_badge(status):
    """Get HTML badge for status"""
    badges = {
        'passed': '<span class="badge badge-success">✓ PASSED</span>',
        'failed': '<span class="badge badge-danger">✗ FAILED</span>',
        'skipped': '<span class="badge badge-warning">⊘ SKIPPED</span>',
        'undefined': '<span class="badge badge-secondary">? UNDEFINED</span>',
    }
    return badges.get(status, f'<span class="badge badge-secondary">{status}</span>')


def get_screenshot_html(step):
    """Get screenshot HTML if available"""
    embeddings = step.get('embeddings', [])
    screenshots = []

    for embed in embeddings:
        if embed.get('mime_type') == 'image/png':
            data = embed.get('data', '')
            screenshots.append(f'<img src="data:image/png;base64,{data}" class="screenshot" alt="Screenshot">')

    return ''.join(screenshots) if screenshots else ''


def generate_html_report(json_file, output_file):
    """Generate HTML report from JSON"""

    # Load JSON data
    features = load_json_results(json_file)
    stats = calculate_statistics(features)

    # Get timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Execution Report - Faberwork</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .stat-card h3 {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}

        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}

        .stat-card .subtitle {{
            color: #999;
            font-size: 0.9em;
        }}

        .stat-card.success .value {{ color: #28a745; }}
        .stat-card.danger .value {{ color: #dc3545; }}
        .stat-card.warning .value {{ color: #ffc107; }}
        .stat-card.info .value {{ color: #17a2b8; }}

        .content {{
            padding: 30px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}

        .feature-card {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}

        .feature-header {{
            background: #f8f9fa;
            padding: 20px;
            cursor: pointer;
            transition: background 0.3s;
        }}

        .feature-header:hover {{
            background: #e9ecef;
        }}

        .feature-header h3 {{
            font-size: 1.3em;
            color: #333;
            margin-bottom: 5px;
        }}

        .feature-header .description {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .feature-tags {{
            margin-top: 10px;
        }}

        .tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-right: 5px;
        }}

        .scenario-list {{
            padding: 0;
        }}

        .scenario {{
            border-top: 1px solid #eee;
            padding: 20px;
        }}

        .scenario:hover {{
            background: #f8f9fa;
        }}

        .scenario-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .scenario-name {{
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
        }}

        .badge {{
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 600;
        }}

        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}

        .badge-danger {{
            background: #f8d7da;
            color: #721c24;
        }}

        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}

        .badge-secondary {{
            background: #e2e3e5;
            color: #383d41;
        }}

        .steps-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}

        .steps-table th {{
            background: #f8f9fa;
            padding: 10px;
            text-align: left;
            font-size: 0.85em;
            text-transform: uppercase;
            color: #666;
        }}

        .steps-table td {{
            padding: 10px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.9em;
        }}

        .steps-table tr:hover {{
            background: #f8f9fa;
        }}

        .step-passed {{
            color: #28a745;
        }}

        .step-failed {{
            color: #dc3545;
            font-weight: 600;
        }}

        .step-skipped {{
            color: #6c757d;
        }}

        .error-message {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.85em;
            color: #721c24;
            white-space: pre-wrap;
        }}

        .screenshot {{
            max-width: 100%;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .chart-container {{
            padding: 20px;
            background: white;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}

        .progress-segment {{
            height: 100%;
            float: left;
            text-align: center;
            line-height: 30px;
            color: white;
            font-size: 0.85em;
            font-weight: 600;
        }}

        .progress-success {{ background: #28a745; }}
        .progress-danger {{ background: #dc3545; }}
        .progress-warning {{ background: #ffc107; }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Test Execution Report</h1>
            <p>Faberwork Website Automation Testing</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated on {timestamp}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card success">
                <h3>Success Rate</h3>
                <div class="value">{stats['success_rate']:.1f}%</div>
                <div class="subtitle">Overall Performance</div>
            </div>

            <div class="stat-card info">
                <h3>Total Scenarios</h3>
                <div class="value">{stats['total_scenarios']}</div>
                <div class="subtitle">{stats['total_features']} Features</div>
            </div>

            <div class="stat-card success">
                <h3>Passed</h3>
                <div class="value">{stats['passed_scenarios']}</div>
                <div class="subtitle">{stats['passed_steps']} Steps</div>
            </div>

            <div class="stat-card danger">
                <h3>Failed</h3>
                <div class="value">{stats['failed_scenarios']}</div>
                <div class="subtitle">{stats['failed_steps']} Steps</div>
            </div>

            <div class="stat-card warning">
                <h3>Skipped</h3>
                <div class="value">{stats['skipped_scenarios']}</div>
                <div class="subtitle">{stats['skipped_steps']} Steps</div>
            </div>

            <div class="stat-card info">
                <h3>Duration</h3>
                <div class="value" style="font-size: 1.5em;">{format_duration(stats['total_duration'])}</div>
                <div class="subtitle">Execution Time</div>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <h2>📊 Test Results Overview</h2>
                <div class="chart-container">
                    <div class="progress-bar">
"""

    # Add progress bar segments
    if stats['total_scenarios'] > 0:
        passed_pct = (stats['passed_scenarios'] / stats['total_scenarios']) * 100
        failed_pct = (stats['failed_scenarios'] / stats['total_scenarios']) * 100
        skipped_pct = (stats['skipped_scenarios'] / stats['total_scenarios']) * 100

        if passed_pct > 0:
            html += f'<div class="progress-segment progress-success" style="width: {passed_pct}%">{stats["passed_scenarios"]} Passed</div>'
        if failed_pct > 0:
            html += f'<div class="progress-segment progress-danger" style="width: {failed_pct}%">{stats["failed_scenarios"]} Failed</div>'
        if skipped_pct > 0:
            html += f'<div class="progress-segment progress-warning" style="width: {skipped_pct}%">{stats["skipped_scenarios"]} Skipped</div>'

    html += """
                    </div>
                </div>
            </div>
"""

    # Add failed features first
    if stats['failed_features']:
        html += """
            <div class="section">
                <h2>❌ Failed Features</h2>
"""
        for feature in stats['failed_features']:
            html += generate_feature_html(feature, show_passed=False)

        html += "</div>"

    # Add passed features
    if stats['passed_features']:
        html += """
            <div class="section">
                <h2>✅ Passed Features</h2>
"""
        for feature in stats['passed_features']:
            html += generate_feature_html(feature, show_passed=True)

        html += "</div>"

    # Footer
    html += f"""
        </div>

        <div class="footer">
            <p>Generated by Faberwork Test Automation Framework</p>
            <p>Total execution time: {format_duration(stats['total_duration'])} | {stats['total_scenarios']} scenarios | {stats['total_steps']} steps</p>
        </div>
    </div>
</body>
</html>
"""

    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    return stats


def generate_feature_html(feature, show_passed=True):
    """Generate HTML for a single feature"""
    html = '<div class="feature-card">'
    html += '<div class="feature-header">'
    html += f'<h3>{feature.get("name", "Unnamed Feature")}</h3>'

    if feature.get('description'):
        html += f'<div class="description">{feature["description"]}</div>'

    if feature.get('tags'):
        html += '<div class="feature-tags">'
        for tag in feature['tags']:
            tag_name = tag if isinstance(tag, str) else tag.get("name", tag)
            html += f'<span class="tag">{tag_name}</span>'
        html += '</div>'

    html += '</div>'
    html += '<div class="scenario-list">'

    # Add scenarios
    for element in feature.get('elements', []):
        if element.get('type') == 'scenario':
            status = element.get('status', 'unknown')

            # Skip passed scenarios if we're only showing failed
            if not show_passed and status == 'passed':
                continue

            html += '<div class="scenario">'
            html += '<div class="scenario-header">'
            html += f'<span class="scenario-name">{element.get("name", "Unnamed Scenario")}</span>'
            html += get_status_badge(status)
            html += '</div>'

            # Add scenario tags
            if element.get('tags'):
                html += '<div class="feature-tags">'
                for tag in element['tags']:
                    tag_name = tag if isinstance(tag, str) else tag.get("name", tag)
                    html += f'<span class="tag">{tag_name}</span>'
                html += '</div>'

            # Add steps table
            html += '<table class="steps-table">'
            html += '<thead><tr><th>Keyword</th><th>Step</th><th>Duration</th><th>Status</th></tr></thead>'
            html += '<tbody>'

            for step in element.get('steps', []):
                step_status = step.get('result', {}).get('status', 'unknown')
                step_duration = step.get('result', {}).get('duration', 0)
                step_class = f'step-{step_status}'

                html += '<tr>'
                html += f'<td><strong>{step.get("keyword", "")}</strong></td>'
                html += f'<td class="{step_class}">{step.get("name", "")}</td>'
                html += f'<td>{format_duration(step_duration)}</td>'
                html += f'<td>{get_status_badge(step_status)}</td>'
                html += '</tr>'

                # Add error message if step failed
                if step_status == 'failed':
                    error_msg = step.get('result', {}).get('error_message', '')
                    if error_msg:
                        html += '<tr><td colspan="4">'
                        html += f'<div class="error-message">{error_msg}</div>'
                        html += '</td></tr>'

                # Add screenshots if available
                screenshot_html = get_screenshot_html(step)
                if screenshot_html:
                    html += '<tr><td colspan="4">'
                    html += screenshot_html
                    html += '</td></tr>'

            html += '</tbody></table>'
            html += '</div>'

    html += '</div></div>'
    return html


def main():
    """Main function"""
    import sys

    # Get JSON file path
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = 'reports/test_results.json'

    # Get output file path
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = 'reports/test_report.html'

    # Check if JSON file exists
    if not os.path.exists(json_file):
        print(f"ERROR: JSON file not found: {json_file}")
        print(f"\nPlease run tests first to generate JSON results:")
        print(f"  behave --tags=@smoke -f json -o {json_file}")
        sys.exit(1)

    print("=" * 80)
    print("  HTML Report Generator")
    print("=" * 80)
    print(f"\nInput:  {json_file}")
    print(f"Output: {output_file}")

    try:
        stats = generate_html_report(json_file, output_file)

        print("\nReport generated successfully!")
        print("\n" + "=" * 80)
        print("  Test Execution Summary")
        print("=" * 80)
        print(f"Total Scenarios:    {stats['total_scenarios']}")
        print(f"Passed:             {stats['passed_scenarios']}")
        print(f"Failed:             {stats['failed_scenarios']}")
        print(f"Skipped:            {stats['skipped_scenarios']}")
        print(f"Success Rate:       {stats['success_rate']:.1f}%")
        print(f"Execution Time:     {format_duration(stats['total_duration'])}")
        print("=" * 80)

        # Open report in browser
        import webbrowser
        abs_path = os.path.abspath(output_file)
        print(f"\nOpening report in browser...")
        print(f"   {abs_path}")
        webbrowser.open(f'file://{abs_path}')

    except Exception as e:
        print(f"\nERROR: Failed to generate report")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
