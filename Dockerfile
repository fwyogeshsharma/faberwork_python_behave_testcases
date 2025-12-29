# Dockerfile for Faberwork Test Automation
# Python + Selenium + Chrome in containerized environment

FROM python:3.11-slim

# Set labels
LABEL maintainer="Faberwork QA Team"
LABEL description="Behave + Selenium test automation for www.faberwork.com"

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
    libgbm1 \
    libxss1 \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Verify Chrome installation
RUN google-chrome --version

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create directories for reports and screenshots
RUN mkdir -p reports screenshots logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV PYTHONDONTWRITEBYTECODE=1

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import selenium; print('OK')" || exit 1

# Default command - run all tests
CMD ["behave", "--no-capture", "--format", "pretty"]
