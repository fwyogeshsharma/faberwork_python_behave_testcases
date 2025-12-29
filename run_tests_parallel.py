#!/usr/bin/env python3
"""
Parallel Test Runner for Behave
Runs tests in parallel to dramatically reduce execution time
"""

import os
import sys
import subprocess
import multiprocessing
import json
import shutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import glob


# Project directories
PROJECT_ROOT = Path(__file__).parent
FEATURES_DIR = PROJECT_ROOT / "features"
REPORTS_DIR = PROJECT_ROOT / "reports"
PARALLEL_RESULTS_DIR = REPORTS_DIR / "parallel-results"


def print_banner(message):
    """Print formatted banner"""
    width = 80
    print("\n" + "=" * width)
    print(f"  {message}")
    print("=" * width + "\n")


def get_all_feature_files(tag=None):
    """Get all feature files, optionally filtered by tag"""
    feature_files = []

    for feature_file in FEATURES_DIR.glob("*.feature"):
        # Skip if tag filter is specified
        if tag:
            with open(feature_file, 'r') as f:
                content = f.read()
                if f"@{tag}" in content:
                    feature_files.append(feature_file)
        else:
            feature_files.append(feature_file)

    return feature_files


def run_feature_file(args):
    """Run a single feature file"""
    feature_file, worker_id, output_format = args

    feature_name = feature_file.stem
    print(f"[Worker {worker_id}] Running: {feature_name}")

    # Create output directory for this worker
    worker_dir = PARALLEL_RESULTS_DIR / f"worker_{worker_id}"
    worker_dir.mkdir(parents=True, exist_ok=True)

    # Output files
    json_output = worker_dir / f"{feature_name}_results.json"
    allure_output = worker_dir / "allure-results"
    allure_output.mkdir(exist_ok=True)

    # Build command
    cmd = [
        "behave",
        str(feature_file),
        "-f", "json",
        "-o", str(json_output),
        "--no-capture",
        "--no-skipped"
    ]

    # Add Allure formatter if requested
    if output_format == "allure":
        cmd.extend([
            "-f", "allure_behave.formatter:AllureFormatter",
            "-o", str(allure_output)
        ])

    # Run the test
    start_time = datetime.now()
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=900  # 15 minute timeout per feature (increased for stability)
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Check if JSON was generated
        json_exists = json_output.exists()

        return {
            'feature': feature_name,
            'worker_id': worker_id,
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'duration': duration,
            'json_output': str(json_output) if json_exists else None,
            'allure_output': str(allure_output) if output_format == "allure" else None,
            'stdout': result.stdout[-500:] if result.stdout else "",  # Last 500 chars
            'stderr': result.stderr[-500:] if result.stderr else ""
        }

    except subprocess.TimeoutExpired:
        print(f"[Worker {worker_id}] TIMEOUT: {feature_name}")
        return {
            'feature': feature_name,
            'worker_id': worker_id,
            'success': False,
            'returncode': -1,
            'duration': 900,
            'json_output': None,
            'error': 'Timeout after 15 minutes'
        }
    except Exception as e:
        print(f"[Worker {worker_id}] ERROR: {feature_name} - {str(e)}")
        return {
            'feature': feature_name,
            'worker_id': worker_id,
            'success': False,
            'returncode': -1,
            'duration': 0,
            'json_output': None,
            'error': str(e)
        }


def merge_json_results(result_files):
    """Merge multiple JSON result files into one"""
    print("\nMerging JSON results...")

    merged_features = []

    for result_file in result_files:
        if not result_file or not Path(result_file).exists():
            continue

        try:
            with open(result_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    merged_features.extend(data)
                else:
                    merged_features.append(data)
        except Exception as e:
            print(f"Warning: Could not read {result_file}: {e}")

    # Write merged results
    merged_output = REPORTS_DIR / "test_results.json"
    with open(merged_output, 'w') as f:
        json.dump(merged_features, f, indent=2)

    print(f"Merged results saved to: {merged_output}")
    return merged_output


def merge_allure_results(allure_dirs):
    """Merge Allure results from multiple workers"""
    print("\nMerging Allure results...")

    final_allure_dir = REPORTS_DIR / "allure-results"

    # Clean and recreate
    if final_allure_dir.exists():
        shutil.rmtree(final_allure_dir)
    final_allure_dir.mkdir(parents=True)

    # Copy all results
    for allure_dir in allure_dirs:
        if not allure_dir or not Path(allure_dir).exists():
            continue

        for file in Path(allure_dir).glob("*"):
            if file.is_file():
                shutil.copy2(file, final_allure_dir / file.name)

    print(f"Merged Allure results saved to: {final_allure_dir}")
    return final_allure_dir


def calculate_statistics(results):
    """Calculate test execution statistics"""
    stats = {
        'total_features': len(results),
        'passed_features': sum(1 for r in results if r['success']),
        'failed_features': sum(1 for r in results if not r['success']),
        'total_duration': sum(r['duration'] for r in results),
        'max_duration': max(r['duration'] for r in results) if results else 0,
        'min_duration': min(r['duration'] for r in results) if results else 0,
        'avg_duration': sum(r['duration'] for r in results) / len(results) if results else 0
    }

    return stats


def print_results(results, stats):
    """Print execution results"""
    print_banner("Parallel Execution Results")

    # Print statistics
    print(f"Total Features:     {stats['total_features']}")
    print(f"Passed:             {stats['passed_features']}")
    print(f"Failed:             {stats['failed_features']}")
    print(f"Success Rate:       {(stats['passed_features']/stats['total_features']*100):.1f}%")
    print(f"\nTotal Duration:     {stats['total_duration']:.2f}s ({stats['total_duration']/60:.2f}m)")
    print(f"Longest Feature:    {stats['max_duration']:.2f}s")
    print(f"Shortest Feature:   {stats['min_duration']:.2f}s")
    print(f"Average Duration:   {stats['avg_duration']:.2f}s")

    # Print failed features
    failed = [r for r in results if not r['success']]
    if failed:
        print("\n" + "=" * 80)
        print("  Failed Features")
        print("=" * 80)
        for r in failed:
            print(f"\n- {r['feature']}")
            print(f"  Worker: {r['worker_id']}")
            print(f"  Duration: {r['duration']:.2f}s")
            if 'error' in r:
                print(f"  Error: {r['error']}")
            if r.get('stderr'):
                print(f"  Stderr: {r['stderr'][:200]}")

    # Print passed features
    passed = [r for r in results if r['success']]
    if passed:
        print("\n" + "=" * 80)
        print("  Passed Features")
        print("=" * 80)
        for r in sorted(passed, key=lambda x: x['duration'], reverse=True)[:10]:
            print(f"- {r['feature']}: {r['duration']:.2f}s")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description="Run Behave tests in parallel")
    parser.add_argument("--workers", "-w", type=int, default=None,
                       help="Number of parallel workers (default: CPU count)")
    parser.add_argument("--tag", "-t", type=str, default=None,
                       help="Run only features with specific tag (e.g., smoke)")
    parser.add_argument("--format", "-f", type=str, default="json",
                       choices=["json", "allure"],
                       help="Output format (default: json)")
    parser.add_argument("--clean", action="store_true",
                       help="Clean previous results before running")
    parser.add_argument("--generate-report", action="store_true",
                       help="Generate HTML report after tests")

    args = parser.parse_args()

    # Determine number of workers (conservative for stability)
    cpu_count = multiprocessing.cpu_count()
    # Use fewer workers to avoid resource exhaustion (max 6 workers)
    default_workers = min(6, max(2, cpu_count // 2))
    workers = args.workers if args.workers else default_workers

    print_banner("Parallel Test Execution")
    print(f"CPU Cores Available: {cpu_count}")
    print(f"Parallel Workers:    {workers}")
    print(f"Output Format:       {args.format}")
    if args.tag:
        print(f"Tag Filter:          @{args.tag}")
    print()

    # Clean previous results
    if args.clean and PARALLEL_RESULTS_DIR.exists():
        print("Cleaning previous results...")
        shutil.rmtree(PARALLEL_RESULTS_DIR)

    PARALLEL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Get feature files
    feature_files = get_all_feature_files(args.tag)

    if not feature_files:
        print("ERROR: No feature files found!")
        if args.tag:
            print(f"Hint: Make sure features are tagged with @{args.tag}")
        sys.exit(1)

    print(f"Found {len(feature_files)} feature files to run\n")

    # Prepare tasks
    tasks = [
        (feature_file, i % workers, args.format)
        for i, feature_file in enumerate(feature_files)
    ]

    # Run in parallel
    print(f"Starting parallel execution with {workers} workers...")
    print("=" * 80 + "\n")

    start_time = datetime.now()
    results = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_feature_file, task): task for task in tasks}

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            status = "PASSED" if result['success'] else "FAILED"
            print(f"[{len(results)}/{len(feature_files)}] {result['feature']}: {status} ({result['duration']:.2f}s)")

    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()

    print("\n" + "=" * 80)
    print(f"Parallel execution completed in {total_duration:.2f}s ({total_duration/60:.2f}m)")
    print("=" * 80)

    # Calculate statistics
    stats = calculate_statistics(results)
    stats['parallel_duration'] = total_duration
    stats['speedup'] = stats['total_duration'] / total_duration if total_duration > 0 else 1

    print(f"\nSpeedup: {stats['speedup']:.2f}x faster than sequential")
    print(f"(Sequential would take: {stats['total_duration']/60:.2f}m)")

    # Merge results
    print_banner("Merging Results")

    json_files = [r['json_output'] for r in results if r.get('json_output')]
    if json_files:
        merged_json = merge_json_results(json_files)

    if args.format == "allure":
        allure_dirs = [r['allure_output'] for r in results if r.get('allure_output')]
        if allure_dirs:
            merged_allure = merge_allure_results(allure_dirs)

    # Print results
    print_results(results, stats)

    # Generate HTML report if requested
    if args.generate_report and json_files:
        print_banner("Generating HTML Report")
        try:
            subprocess.run([
                sys.executable,
                "generate_html_report.py",
                str(REPORTS_DIR / "test_results.json"),
                str(REPORTS_DIR / "test_report.html")
            ], cwd=PROJECT_ROOT, check=True)
        except Exception as e:
            print(f"Warning: Could not generate HTML report: {e}")

    # Save summary
    summary_file = REPORTS_DIR / "parallel_execution_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'workers': workers,
            'statistics': stats,
            'results': results
        }, f, indent=2)

    print(f"\nExecution summary saved to: {summary_file}")

    # Exit with appropriate code
    if stats['failed_features'] > 0:
        print("\nSome tests failed!")
        sys.exit(1)
    else:
        print("\nAll tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
