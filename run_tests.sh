#!/bin/bash
# Faberwork Test Automation - Test Execution Script
# This script provides various options for running tests

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${GREEN}========================================${NC}"
}

print_info() {
    echo -e "${YELLOW}INFO:${NC} $1"
}

print_error() {
    echo -e "${RED}ERROR:${NC} $1"
}

# Main script
print_header "Faberwork Test Automation"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_info "Creating .env file from .env.example"
    cp .env.example .env
fi

# Parse command line arguments
TEST_TYPE="${1:-all}"
TAG="${2:-}"

case $TEST_TYPE in
    smoke)
        print_header "Running Smoke Tests"
        behave --tags=@smoke --no-capture --format pretty
        ;;
    regression)
        print_header "Running Regression Tests"
        behave --tags=@regression --no-capture --format pretty
        ;;
    forms)
        print_header "Running Form Tests"
        behave --tags=@forms --no-capture --format pretty
        ;;
    navigation)
        print_header "Running Navigation Tests"
        behave --tags=@navigation --no-capture --format pretty
        ;;
    carousel)
        print_header "Running Carousel Tests"
        behave --tags=@carousel --no-capture --format pretty
        ;;
    search)
        print_header "Running Search Tests"
        behave --tags=@search --no-capture --format pretty
        ;;
    allure)
        print_header "Running Tests with Allure Reports"
        behave -f allure_behave.formatter:AllureFormatter -o reports/
        print_info "Generating Allure report..."
        allure serve reports/
        ;;
    json)
        print_header "Running Tests with JSON Output"
        behave --format json --outfile reports/results.json
        ;;
    parallel)
        print_header "Running Tests in Parallel"
        print_error "Parallel execution requires behave-parallel package"
        print_info "Install with: pip install behave-parallel"
        ;;
    clean)
        print_header "Cleaning Test Artifacts"
        rm -rf reports/* screenshots/* logs/*
        print_info "Cleaned reports, screenshots, and logs"
        ;;
    help|--help|-h)
        echo "Usage: ./run_tests.sh [TEST_TYPE]"
        echo ""
        echo "Test Types:"
        echo "  smoke       - Run smoke tests (@smoke tag)"
        echo "  regression  - Run regression tests (@regression tag)"
        echo "  forms       - Run form tests (@forms tag)"
        echo "  navigation  - Run navigation tests (@navigation tag)"
        echo "  carousel    - Run carousel tests (@carousel tag)"
        echo "  search      - Run search tests (@search tag)"
        echo "  all         - Run all tests (default)"
        echo "  allure      - Run tests and generate Allure report"
        echo "  json        - Run tests and output JSON results"
        echo "  clean       - Clean test artifacts"
        echo "  help        - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh smoke"
        echo "  ./run_tests.sh regression"
        echo "  ./run_tests.sh all"
        ;;
    all|*)
        print_header "Running All Tests"
        behave --no-capture --format pretty
        ;;
esac

echo ""
print_info "Test execution completed!"
print_info "Reports: ./reports/"
print_info "Screenshots: ./screenshots/"
print_info "Logs: ./logs/"
