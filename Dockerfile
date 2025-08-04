# Use Playwright's base image
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install browser dependencies (already included in base image, but safe to re-run)
RUN playwright install --with-deps

# Set the command to run your bot
CMD ["python", "ihouse_checker_playwright.py"]
