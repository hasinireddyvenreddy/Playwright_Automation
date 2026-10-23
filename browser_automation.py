import logging
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from config import HEADLESS, TIMEOUT, SCREENSHOTS_DIR,OUTPUT_DIR



logger = logging.getLogger(__name__)
def extract_job_details(page):
    """Extract job titles, companies, and locations from job listings."""

    jobs = []

    job_cards = page.locator("div.card-content")

    for index in range(job_cards.count()):
        card = job_cards.nth(index)

        title = card.locator("h2.title").inner_text().strip()
        company = card.locator("h3.company").inner_text().strip()
        location = card.locator("p.location").inner_text().strip()

        jobs.append({
            "Job Title": title,
            "Company": company,
            "Location": location,
        })

    logger.info("Extracted %s job listings.", len(jobs))

    return jobs
def save_jobs_to_csv(jobs):
    """Save extracted job listings to a CSV file."""

    output_file = OUTPUT_DIR / "job_listings.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Job Title", "Company", "Location"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    logger.info("Job listings saved to %s", output_file)

def run_browser_automation(url: str) -> bool:
    """Open a webpage, capture a screenshot, and close the browser safely."""

    with sync_playwright() as playwright:
        browser = None

        try:
            logger.info("Launching Chromium browser.")

            browser = playwright.chromium.launch(headless=HEADLESS)

            page = browser.new_page()
            page.set_default_timeout(TIMEOUT)

            logger.info("Navigating to %s", url)
            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=TIMEOUT,
            )

            if response is not None and response.status >= 400:
                logger.error("Page returned HTTP status %s", response.status)
                return False

            page.screenshot(
                path=str(SCREENSHOTS_DIR / "homepage.png"),
                full_page=True,
            )

            logger.info("Page title: %s", page.title())
            logger.info("Screenshot saved successfully.")
            jobs = extract_job_details(page)
            if jobs:
                save_jobs_to_csv(jobs)
                logger.info("Total jobs extracted: %d", len(jobs))
                print(f"Extracted {len(jobs)} job listings.")
                print(f"CSV file saved to: {OUTPUT_DIR / 'job_listings.csv'}")
            else:
                logger.warning("No job listings were found.")
                print("No job listings were found.")
            return True

        except PlaywrightTimeoutError:
            logger.exception("The page navigation or operation timed out.")
            return False

        except Exception:
            logger.exception("Browser automation failed.")
            return False

        finally:
            if browser is not None:
                browser.close()
                logger.info("Browser closed.")