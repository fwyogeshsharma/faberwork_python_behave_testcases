# Faberwork Test Automation Framework

Comprehensive test automation framework for www.faberwork.com using Python, Behave (BDD), Selenium, and Docker.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Running Tests](#running-tests)
- [Docker Usage](#docker-usage)
- [Writing Tests](#writing-tests)
- [Configuration](#configuration)
- [Reports](#reports)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This framework provides automated testing for the Faberwork website, covering:
- Navigation and UI components
- Form submissions and validations
- Carousel and slider functionality
- Search capabilities
- Responsive design testing

## ✨ Features

- **BDD Framework**: Gherkin syntax for readable test scenarios
- **Page Object Model**: Maintainable and reusable code structure
- **Docker Support**: Single command execution with `docker-compose up`
- **Cross-Browser**: Chrome, Firefox, Edge support
- **Headless Execution**: Run tests without GUI
- **Comprehensive Reporting**: Allure, HTML, JSON reports
- **Screenshot on Failure**: Automatic screenshot capture
- **Parallel Execution**: Support for parallel test runs
- **CI/CD Ready**: GitHub Actions and Jenkins integration

## 🛠️ Tech Stack

- **Python** 3.11+
- **Behave** - BDD framework
- **Selenium** - Browser automation
- **Docker** & **Docker Compose** - Containerization
- **Chrome** - Primary test browser
- **Allure** - Test reporting
- **Loguru** - Enhanced logging
- **Faker** - Test data generation

## 📁 Project Structure

```
faberwork_python_behave_testcases/
├── features/                   # Feature files and step definitions
│   ├── steps/                 # Step definition files
│   ├── environment.py         # Behave hooks
│   ├── smoke.feature
│   ├── navigation.feature
│   ├── forms.feature
│   ├── carousel.feature
│   └── search.feature
├── pages/                      # Page Object Models
│   ├── base_page.py
│   ├── home_page.py
│   ├── services_page.py
│   ├── contact_page.py
│   └── about_page.py
├── utils/                      # Utilities and helpers
│   ├── config.py              # Configuration management
│   ├── driver_factory.py      # WebDriver factory
│   ├── helpers.py             # Helper functions
│   ├── test_data.py           # Test data generator
│   └── locator_finder.py      # Locator utilities
├── test_data/                  # Test data files
├── reports/                    # Test reports
├── screenshots/                # Screenshot storage
├── logs/                       # Test execution logs
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── behave.ini                  # Behave configuration
└── run_tests.sh               # Test execution script
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker
- Docker Compose

**Steps:**
```bash
# Clone the repository
git clone <repository-url>
cd faberwork_python_behave_testcases

# Copy environment file
cp .env.example .env

# Run tests with Docker
docker-compose up --build
```

### Option 2: Local Setup

**Prerequisites:**
- Python 3.11+
- Chrome browser
- Git

**Steps:**
```bash
# Clone the repository
git clone <repository-url>
cd faberwork_python_behave_testcases

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run tests
behave
```

## 🧪 Running Tests

### Using Docker

```bash
# Run all tests
docker-compose up --build

# Run specific test suite
docker-compose run tests behave --tags=@smoke

# Run specific feature file
docker-compose run tests behave features/forms.feature

# Run with Allure reports
docker-compose run tests behave -f allure_behave.formatter:AllureFormatter -o reports/
```

### Using Local Environment

```bash
# Run all tests
behave

# Run smoke tests
behave --tags=@smoke

# Run regression tests
behave --tags=@regression

# Run specific feature
behave features/navigation.feature

# Run with specific format
behave --format pretty --no-capture

# Run and generate Allure report
behave -f allure_behave.formatter:AllureFormatter -o reports/
allure serve reports/
```

### Using Test Script

```bash
# Make script executable (Linux/Mac)
chmod +x run_tests.sh

# Run smoke tests
./run_tests.sh smoke

# Run regression tests
./run_tests.sh regression

# Run all tests
./run_tests.sh all

# Generate Allure reports
./run_tests.sh allure

# Clean artifacts
./run_tests.sh clean

# Show help
./run_tests.sh help
```

## 🐳 Docker Usage

### Commands

```bash
# Build and run tests
docker-compose up --build

# Run tests and remove containers
docker-compose up --build --abort-on-container-exit

# Run specific tags
docker-compose run tests behave --tags=@smoke

# View logs
docker-compose logs -f tests

# Stop containers
docker-compose down

# Clean up everything
docker-compose down -v --rmi all
```

### View Allure Reports

```bash
# Start Allure service
docker-compose up allure

# Access reports at
http://localhost:5050
```

## ✍️ Writing Tests

### Create Feature File

```gherkin
@smoke @myfeature
Feature: My New Feature
  As a user
  I want to test something
  So that I can verify it works

  Background:
    Given I am on the homepage

  Scenario: Test scenario name
    When I perform an action
    Then I should see expected result
```

### Create Step Definitions

```python
# features/steps/my_steps.py
from behave import given, when, then

@when('I perform an action')
def step_perform_action(context):
    context.home_page.click_something()

@then('I should see expected result')
def step_verify_result(context):
    assert context.home_page.is_element_displayed(locator)
```

### Create Page Object

```python
# pages/my_page.py
from .base_page import BasePage
from selenium.webdriver.common.by import By

class MyPage(BasePage):
    ELEMENT = (By.ID, "my-element")

    def click_element(self):
        self.click(self.ELEMENT)
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
BASE_URL=https://www.faberwork.com
BROWSER=chrome
HEADLESS=True
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
TAKE_SCREENSHOT_ON_FAILURE=True
```

### Behave Tags

- `@smoke` - Critical path tests
- `@regression` - Full regression suite
- `@forms` - Form testing
- `@navigation` - Navigation tests
- `@carousel` - Carousel/slider tests
- `@search` - Search functionality
- `@wip` - Work in progress (skipped)
- `@skip` - Skipped tests

## 📊 Reports

### Allure Reports

```bash
# Generate and serve
behave -f allure_behave.formatter:AllureFormatter -o reports/
allure serve reports/
```

### HTML Reports

```bash
behave --format html --outfile reports/report.html
```

### JSON Reports

```bash
behave --format json --outfile reports/results.json
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: docker-compose up --build --abort-on-container-exit
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: reports/
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'docker-compose up --build --abort-on-container-exit'
            }
        }
        stage('Reports') {
            steps {
                publishHTML([reportDir: 'reports', reportFiles: 'index.html'])
            }
        }
    }
}
```

## 🔧 Troubleshooting

### Common Issues

**1. ChromeDriver version mismatch**
```bash
# Update webdriver-manager
pip install --upgrade webdriver-manager
```

**2. Docker permission issues**
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
```

**3. Tests running slowly**
```env
# Reduce wait times in .env
IMPLICIT_WAIT=5
EXPLICIT_WAIT=10
```

**4. Screenshot not captured**
```env
# Enable screenshots
TAKE_SCREENSHOT_ON_FAILURE=True
```

### Debug Mode

```bash
# Run with verbose output
behave --no-capture --format pretty -v

# Check browser logs
# Enable in .env
ENABLE_BROWSER_LOGGING=True
```

## 📝 Best Practices

1. **Use Page Objects**: Keep locators and actions in page objects
2. **Write Reusable Steps**: Create generic, reusable step definitions
3. **Tag Your Tests**: Use appropriate tags for test organization
4. **Keep Scenarios Focused**: One scenario should test one thing
5. **Use Background**: Extract common setup to Background
6. **Maintain Test Data**: Use test_data module for data generation
7. **Screenshot on Failure**: Already enabled by default
8. **Review Logs**: Check logs/ directory for detailed execution info

## 🤝 Contributing

1. Create a feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

For questions or support, contact the QA team.

---

**Generated with Claude Code** 🤖

Last Updated: 2025-12-26
