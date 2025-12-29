# Faberwork.com Test Automation Plan
## Python + Behave + Selenium Project

---

## 📋 Project Overview

**Website Under Test:** https://www.faberwork.com
**Framework:** Behave (BDD)
**Language:** Python 3.8+
**Browser:** Chrome (with DevTools for locator identification)
**Approach:** Page Object Model (POM) with BDD
**Deployment:** Docker + Docker Compose (Single Command Execution)
**Production Ready:** Yes - Containerized for easy deployment on production servers

---

## 🎯 What We're Testing

Based on website analysis, we'll test:

### 1. **Navigation & UI Components**
- Header navigation menu
- Footer links
- Logo and branding elements
- Mobile responsive menu

### 2. **Service Pages**
- SnowPro® Certified Developers
- Software Development
- Mobile App Development
- AI Solutions
- Database Solutions
- Test Automation

### 3. **Interactive Features**
- Success Stories carousel (12+ projects)
- Testimonial slider (auto-rotating)
- Service cards grid
- Company stats display

### 4. **Forms & Input Validation**
- Consultation request form (Name, Company, Email, Phone)
- Newsletter subscription
- Contact form
- Field validations (email, phone formats)
- Form submission and error handling

### 5. **Search & Filter Functionality**
- Article search with AJAX
- Content filtering dropdowns
- Dynamic results display

### 6. **Chatbot Integration**
- Chatbot widget interaction
- Message submission
- Response handling

### 7. **Cross-Browser & Responsive**
- Desktop layouts
- Mobile responsive views
- Different screen resolutions

---

## 🛠️ Required Dependencies

### Python Packages
```txt
behave==1.2.6
selenium==4.15.2
webdriver-manager==4.0.1
allure-behave==2.13.2
pytest==7.4.3
faker==20.1.0
python-dotenv==1.0.0
requests==2.31.0
pillow==10.1.0
openpyxl==3.1.2
```

### Additional Tools
- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Chrome Browser** (in Docker container)
- **ChromeDriver** (auto-managed by webdriver-manager)
- **Allure** (for reporting - optional)
- **Git** (version control)

---

## 📁 Proposed Project Structure

```
faberwork_python_behave_testcases/
│
├── features/
│   ├── steps/
│   │   ├── __init__.py
│   │   ├── navigation_steps.py
│   │   ├── form_steps.py
│   │   ├── carousel_steps.py
│   │   ├── search_steps.py
│   │   └── common_steps.py
│   │
│   ├── environment.py           # Behave hooks (before/after scenario)
│   ├── navigation.feature
│   ├── forms.feature
│   ├── carousel.feature
│   ├── search.feature
│   ├── contact.feature
│   └── responsive.feature
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py            # Base page with common methods
│   ├── home_page.py
│   ├── services_page.py
│   ├── contact_page.py
│   ├── about_page.py
│   └── blog_page.py
│
├── utils/
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   ├── driver_factory.py       # WebDriver setup
│   ├── helpers.py              # Common helper functions
│   ├── locator_finder.py       # Tool to find locators using Chrome DevTools
│   └── test_data.py            # Test data management
│
├── reports/
│   └── .gitkeep
│
├── screenshots/
│   └── .gitkeep
│
├── test_data/
│   ├── test_users.json
│   └── form_data.json
│
├── .env.example                # Environment variables template
├── .env                        # Environment variables (not in git)
├── .gitignore
├── .dockerignore               # Docker ignore file
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose orchestration
├── requirements.txt
├── behave.ini                  # Behave configuration
├── pytest.ini                  # Pytest configuration
├── run_tests.sh                # Shell script to run tests
├── README.md
└── TEST_AUTOMATION_PLAN.md     # This file
```

---

## 🔍 Approach to Finding Locators Using Chrome DevTools

### Method 1: Using Chrome Inspect Element
1. **Open Chrome and navigate** to https://www.faberwork.com
2. **Right-click** on element → "Inspect" (or F12)
3. **In Elements tab**, hover over HTML to highlight elements
4. **Copy locators**:
   - Right-click element → Copy → Copy selector (CSS)
   - Right-click element → Copy → Copy XPath
   - Right-click element → Copy → Copy JS path

### Method 2: Using Chrome Console for Testing
```javascript
// Test CSS Selector
document.querySelector('button.cta-button')

// Test XPath
$x("//button[contains(text(), 'Get Started')]")

// Get all matching elements
document.querySelectorAll('.service-card')
```

### Method 3: Automated Locator Strategy (Priority Order)
1. **ID** - `id="unique-id"` → `driver.find_element(By.ID, "unique-id")`
2. **Name** - `name="email"` → `driver.find_element(By.NAME, "email")`
3. **CSS Selector** - `class="btn-primary"` → `driver.find_element(By.CSS_SELECTOR, ".btn-primary")`
4. **XPath** - `//button[@type='submit']` → `driver.find_element(By.XPATH, "//button[@type='submit']")`
5. **Link Text** - `<a>Contact Us</a>` → `driver.find_element(By.LINK_TEXT, "Contact Us")`

### Best Practices for Locators
- ✅ Prefer **ID** and **Name** (most stable)
- ✅ Use **data-testid** attributes if available
- ✅ CSS Selectors for simple class/attribute combinations
- ⚠️ Avoid complex XPath with positions like `[1]`, `[2]`
- ⚠️ Avoid locators based on text that might change

---

## 🐳 Docker Configuration & Single Command Execution

### Why Docker?
- **Consistent Environment**: Same setup on dev, staging, and production
- **No Local Dependencies**: No need to install Python, Chrome, or other tools
- **Easy Deployment**: Deploy to any server with just Docker installed
- **Isolation**: Tests run in isolated containers
- **Scalability**: Easy to run parallel tests with multiple containers

### Single Command Execution
```bash
# Run all tests with a single command
docker-compose up --build

# Run tests and remove containers after completion
docker-compose up --build --abort-on-container-exit

# Run specific tags
docker-compose run tests behave --tags=@smoke
```

### Dockerfile Structure
```dockerfile
# Use Python slim image with Chrome support
FROM python:3.11-slim

# Install system dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test framework
COPY . .

# Create directories for reports and screenshots
RUN mkdir -p reports screenshots

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Run tests by default
CMD ["behave"]
```

### docker-compose.yml Structure
```yaml
version: '3.8'

services:
  tests:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: faberwork_test_automation
    volumes:
      # Mount reports and screenshots to host
      - ./reports:/app/reports
      - ./screenshots:/app/screenshots
      # Mount test code for live updates during development
      - ./features:/app/features
      - ./pages:/app/pages
      - ./utils:/app/utils
    environment:
      - BASE_URL=${BASE_URL:-https://www.faberwork.com}
      - BROWSER=${BROWSER:-chrome}
      - HEADLESS=${HEADLESS:-True}
      - IMPLICIT_WAIT=${IMPLICIT_WAIT:-10}
      - EXPLICIT_WAIT=${EXPLICIT_WAIT:-20}
      - ENVIRONMENT=${ENVIRONMENT:-production}
    networks:
      - test-network
    shm_size: '2gb'  # Increase shared memory for Chrome
    command: behave --no-capture --format pretty

  # Optional: Allure reporting service
  allure:
    image: frankescobar/allure-docker-service:latest
    container_name: faberwork_allure_reports
    ports:
      - "5050:5050"
    volumes:
      - ./reports:/app/allure-results
    networks:
      - test-network

networks:
  test-network:
    driver: bridge
```

### .dockerignore File
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Testing
.pytest_cache/
.tox/
htmlcov/
.coverage
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore

# Reports (will be volume mounted)
reports/*
screenshots/*

# Environment
.env

# OS
.DS_Store
Thumbs.db
```

### Environment Variables (.env file)
```env
# Application Settings
BASE_URL=https://www.faberwork.com
ENVIRONMENT=production

# Browser Configuration
BROWSER=chrome
HEADLESS=True

# Wait Times (seconds)
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30

# Test Configuration
TAKE_SCREENSHOT_ON_FAILURE=True
RETRY_FAILED_TESTS=2

# Reporting
ALLURE_RESULTS_DIR=reports
SCREENSHOT_DIR=screenshots
```

### Production Server Deployment

#### Prerequisites on Server
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Deploy and Run Tests
```bash
# 1. Clone repository
git clone <repository-url>
cd faberwork_python_behave_testcases

# 2. Create .env file (copy from .env.example)
cp .env.example .env

# 3. Run tests with single command
docker-compose up --build

# 4. View reports
# Reports are automatically saved to ./reports and ./screenshots
```

### Advanced Docker Commands

#### Run Specific Test Suites
```bash
# Run smoke tests only
docker-compose run tests behave --tags=@smoke

# Run regression tests
docker-compose run tests behave --tags=@regression

# Run specific feature file
docker-compose run tests behave features/forms.feature

# Run with custom format
docker-compose run tests behave --format json --outfile reports/results.json
```

#### Run Tests in Headless Mode (Default for Production)
```bash
# Already configured in docker-compose.yml
# Chrome runs in headless mode by default in container
docker-compose up
```

#### Run Tests with Live Browser (for debugging)
```bash
# Modify .env file: HEADLESS=False
# Run with X11 forwarding (Linux/Mac)
docker-compose run -e DISPLAY=$DISPLAY tests behave

# Or use VNC for remote viewing
docker-compose run tests behave
```

#### Parallel Execution
```bash
# Run multiple instances
docker-compose up --scale tests=3
```

#### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Remove volumes and images
docker-compose down -v --rmi all

# Clean up old reports
rm -rf reports/* screenshots/*
```

### CI/CD Integration with Docker

#### GitHub Actions Example
```yaml
name: Run Selenium Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Run tests with Docker Compose
      run: docker-compose up --build --abort-on-container-exit

    - name: Upload test reports
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: |
          reports/
          screenshots/
```

#### Jenkins Pipeline Example
```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker-compose up --build --abort-on-container-exit'
            }
        }

        stage('Publish Reports') {
            steps {
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'index.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**,screenshots/**', allowEmptyArchive: true
        }
    }
}
```

### Monitoring & Logging

#### View Container Logs
```bash
# Follow logs in real-time
docker-compose logs -f tests

# View last 100 lines
docker-compose logs --tail=100 tests

# Save logs to file
docker-compose logs tests > test_execution.log
```

#### Access Container Shell (for debugging)
```bash
# Open bash in running container
docker-compose exec tests bash

# Run commands inside container
docker-compose exec tests python --version
docker-compose exec tests which google-chrome
```

---

## 🚀 Implementation Steps

### Phase 1: Environment Setup (Day 1)

#### Option A: Docker Setup (Recommended for Production)
1. ✅ Install Docker and Docker Compose on your machine/server
   ```bash
   # For Linux
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # For Windows/Mac: Download Docker Desktop from docker.com
   ```

2. ✅ Setup project structure (folders and files)
   ```bash
   mkdir -p features/steps pages utils reports screenshots test_data
   ```

3. ✅ Create Docker configuration files
   - Dockerfile
   - docker-compose.yml
   - .dockerignore
   - .env (from .env.example)

4. ✅ Configure environment variables (.env file)
   ```env
   BASE_URL=https://www.faberwork.com
   BROWSER=chrome
   HEADLESS=True
   IMPLICIT_WAIT=10
   EXPLICIT_WAIT=20
   ENVIRONMENT=production
   ```

5. ✅ Test Docker setup
   ```bash
   docker-compose up --build
   ```

#### Option B: Local Setup (For Development)
1. ✅ Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. ✅ Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. ✅ Setup project structure (folders and files)

4. ✅ Configure environment variables (.env file)
   ```env
   BASE_URL=https://www.faberwork.com
   BROWSER=chrome
   HEADLESS=False
   IMPLICIT_WAIT=10
   EXPLICIT_WAIT=20
   ```

### Phase 2: Framework Foundation (Day 1-2)
1. ✅ Create `driver_factory.py` for WebDriver management
2. ✅ Create `base_page.py` with common methods:
   - `click_element()`
   - `enter_text()`
   - `wait_for_element()`
   - `scroll_to_element()`
   - `take_screenshot()`

3. ✅ Setup `environment.py` with Behave hooks:
   - `before_all()` - Initialize config
   - `before_scenario()` - Launch browser
   - `after_scenario()` - Take screenshot on failure
   - `after_all()` - Cleanup

### Phase 3: Locator Identification (Day 2-3)
Using Chrome DevTools, identify and document locators for:

#### Homepage Elements
- Navigation menu items
- Hero section CTA buttons
- Service cards
- Success stories carousel
- Testimonial slider
- Newsletter form
- Footer links

#### Forms
- Consultation form fields (name, email, company, phone)
- Submit buttons
- Error messages
- Success messages

#### Interactive Elements
- Carousel next/previous buttons
- Search input
- Filter dropdowns
- Chatbot widget

### Phase 4: Page Objects Creation (Day 3-4)
1. ✅ `home_page.py` - All homepage elements and methods
2. ✅ `services_page.py` - Service page elements
3. ✅ `contact_page.py` - Contact form elements
4. ✅ `about_page.py` - About page elements

Example structure:
```python
class HomePage(BasePage):
    # Locators
    LOGO = (By.CSS_SELECTOR, "img.logo")
    NAV_SERVICES = (By.LINK_TEXT, "Services")
    CONSULTATION_FORM = (By.ID, "consultation-form")

    # Methods
    def click_services_menu(self):
        self.click_element(self.NAV_SERVICES)

    def fill_consultation_form(self, name, email, company, phone):
        # Implementation
        pass
```

### Phase 5: Feature Files (Day 4-5)
Write BDD scenarios in Gherkin syntax:

**Example: forms.feature**
```gherkin
Feature: Contact Form Functionality
  As a potential client
  I want to submit a consultation request
  So that Faberwork can contact me

  Background:
    Given I am on the Faberwork homepage

  Scenario: Submit consultation form with valid data
    When I fill in the consultation form with:
      | Field   | Value                    |
      | Name    | John Doe                 |
      | Company | Tech Corp                |
      | Email   | john@example.com         |
      | Phone   | +1234567890              |
    And I submit the form
    Then I should see a success message

  Scenario Outline: Form validation for invalid email
    When I enter "<email>" in the email field
    And I submit the form
    Then I should see an error message "<error>"

    Examples:
      | email          | error                      |
      | invalid        | Please enter a valid email |
      | @example.com   | Please enter a valid email |
      | test@          | Please enter a valid email |
```

### Phase 6: Step Definitions (Day 5-6)
Implement step functions:

```python
# features/steps/form_steps.py
from behave import given, when, then

@given('I am on the Faberwork homepage')
def step_navigate_to_homepage(context):
    context.home_page.navigate_to_homepage()

@when('I fill in the consultation form with')
def step_fill_form(context):
    for row in context.table:
        # Implementation
        pass

@then('I should see a success message')
def step_verify_success(context):
    assert context.home_page.is_success_message_displayed()
```

### Phase 7: Test Execution & Reporting (Day 6-7)

#### With Docker (Production)
1. ✅ Run all tests
   ```bash
   docker-compose up --build --abort-on-container-exit
   ```

2. ✅ Run individual feature files
   ```bash
   docker-compose run tests behave features/forms.feature
   ```

3. ✅ Run with tags
   ```bash
   docker-compose run tests behave --tags=@smoke
   docker-compose run tests behave --tags=@regression
   ```

4. ✅ Generate Allure reports
   ```bash
   docker-compose run tests behave -f allure_behave.formatter:AllureFormatter -o reports/
   docker-compose up allure  # View reports on http://localhost:5050
   ```

#### Without Docker (Local Development)
1. ✅ Run individual feature files
   ```bash
   behave features/forms.feature
   ```

2. ✅ Run all tests
   ```bash
   behave
   ```

3. ✅ Generate Allure reports
   ```bash
   behave -f allure_behave.formatter:AllureFormatter -o reports/
   allure serve reports/
   ```

4. ✅ Run with tags
   ```bash
   behave --tags=@smoke
   behave --tags=@regression
   ```

### Phase 8: Docker & CI/CD Integration (Day 7+)
1. ✅ Finalize Dockerfile and docker-compose.yml
2. ✅ Setup GitHub Actions / Jenkins pipeline with Docker
3. ✅ Configure scheduled test runs (cron jobs)
4. ✅ Email/Slack notifications for failures
5. ✅ Automated report generation and archiving
6. ✅ Deploy to production server

---

## 📊 Test Coverage Plan

### Priority 1 - Critical Paths (Smoke Tests)
- ✅ Homepage loads successfully
- ✅ Navigation menu functional
- ✅ Consultation form submission
- ✅ Contact form submission

### Priority 2 - Core Features (Regression)
- ✅ All service pages accessible
- ✅ Success stories carousel navigation
- ✅ Testimonial slider
- ✅ Form validations
- ✅ Search functionality
- ✅ Newsletter subscription

### Priority 3 - Extended Coverage
- ✅ Chatbot interaction
- ✅ Mobile responsive views
- ✅ Footer links validation
- ✅ Blog/article filtering
- ✅ Error handling scenarios
- ✅ Broken links check

---

## 🔧 Utilities to Build

### 1. Locator Finder Helper
A Python script to help find and test locators:

```python
# utils/locator_finder.py
def find_element_by_text(driver, text):
    """Find elements containing specific text"""
    xpath = f"//*[contains(text(), '{text}')]"
    return driver.find_elements(By.XPATH, xpath)

def validate_locator(driver, locator_type, locator_value):
    """Test if a locator works"""
    try:
        element = driver.find_element(locator_type, locator_value)
        return True, element
    except NoSuchElementException:
        return False, None
```

### 2. Screenshot on Failure
Automatically capture screenshots when tests fail:

```python
# In environment.py
def after_scenario(context, scenario):
    if scenario.status == 'failed':
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"{scenario.name}_{timestamp}.png"
        context.driver.save_screenshot(f"screenshots/{screenshot_name}")
```

### 3. Test Data Generator
Using Faker for generating test data:

```python
from faker import Faker
fake = Faker()

def generate_user_data():
    return {
        'name': fake.name(),
        'email': fake.email(),
        'company': fake.company(),
        'phone': fake.phone_number()
    }
```

---

## 🎨 Sample Feature Files to Create

1. **navigation.feature** - Menu navigation, page routing
2. **forms.feature** - All form submissions and validations
3. **carousel.feature** - Success stories and testimonial sliders
4. **search.feature** - Search and filter functionality
5. **contact.feature** - Contact page specific tests
6. **responsive.feature** - Mobile/tablet view tests
7. **chatbot.feature** - Chatbot interaction tests
8. **smoke.feature** - Critical path smoke tests

---

## 📈 Success Metrics

- ✅ **Test Coverage**: >80% of user journeys
- ✅ **Execution Time**: <15 minutes for full suite
- ✅ **Pass Rate**: >95% on stable environments
- ✅ **Maintainability**: Clear page objects, reusable steps
- ✅ **Reporting**: Clear failure analysis with screenshots

---

## 🚨 Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Dynamic content/ads | Use explicit waits, flexible locators |
| AJAX requests | Implement wait strategies for async operations |
| Flaky tests | Add retry logic, improve waits |
| Locator changes | Use data-testid, maintain locator documentation |
| Environment differences | Parameterize base URL, use config files |

---

## 📝 Next Steps

1. **Review this plan** with stakeholders
2. **Install Docker** on development and production servers
3. **Setup project structure** (folders and files)
4. **Create Docker configuration** (Dockerfile, docker-compose.yml)
5. **Start Phase 1** - Docker environment setup
6. **Create first feature file** as proof of concept
7. **Test with single command**: `docker-compose up --build`
8. **Deploy to production server** and schedule automated runs
9. **Iterate and expand** based on feedback

---

## 🎯 Quick Start Guide (TL;DR)

### For Production Server Deployment

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clone repository
git clone <your-repo-url>
cd faberwork_python_behave_testcases

# 3. Configure environment
cp .env.example .env
# Edit .env if needed

# 4. Run tests with ONE COMMAND
docker-compose up --build

# That's it! Reports will be in ./reports and ./screenshots
```

### Key Commands

| Command | Description |
|---------|-------------|
| `docker-compose up --build` | Build and run all tests |
| `docker-compose run tests behave --tags=@smoke` | Run smoke tests only |
| `docker-compose run tests behave features/forms.feature` | Run specific feature |
| `docker-compose logs -f tests` | View live test logs |
| `docker-compose down` | Stop and clean up containers |
| `docker-compose up allure` | View Allure reports on port 5050 |

---

## 🤝 Collaboration & Maintenance

- **Code Reviews**: All test code should be reviewed
- **Documentation**: Keep locators and page objects documented
- **Version Control**: Use Git with meaningful commit messages
- **Regular Updates**: Update tests when UI changes
- **Knowledge Sharing**: Team training on Behave/Selenium

---

**Created:** 2025-12-26
**Last Updated:** 2025-12-26
**Status:** Planning Phase - Docker Integration Added
**Deployment:** Production-ready with Docker + Docker Compose
**Single Command Execution:** `docker-compose up --build`
**Estimated Timeline:** 7-10 days for initial framework + core tests
