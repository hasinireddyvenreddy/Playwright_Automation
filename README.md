# Smart Job Search Automation System

## About the Project
The Smart Job Search Automation System is a Python project that uses Playwright to automate browser activities and collect job listing information from a demo website.

It extracts job titles, company names, and locations, then saves the collected information into a CSV file.

## Features
- Automated browser launch and navigation
- Job listing extraction
- Job title, company, and location collection
- CSV file export
- Automatic screenshot capture
- Logging and exception handling
- Environment-based configuration
- Automatic browser closure

## Technologies Used
- Python
- Playwright
- Chromium
- CSV
- Python Logging
- python-dotenv

## Project Structure

```text
Playwright_Automation/
├── browser_automation.py
├── config.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── logs/
├── output/
└── screenshots/