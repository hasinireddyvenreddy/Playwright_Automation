import logging

from config import LOGS_DIR
from browser_automation import run_browser_automation

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOGS_DIR / "automation.log",
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def main():
    """Run the Smart Job Search Automation System."""

    logger.info("Smart Job Search Automation System started.")

    # Public demo website for the initial browser test
    url = "https://realpython.github.io/fake-jobs/"

    success = run_browser_automation(url)

    if success:
        logger.info("Browser automation completed successfully.")
        print("\nAutomation completed successfully!")
        print("Check the screenshots folder for the captured screenshot.")
    else:
        logger.error("Browser automation failed.")
        print("\nAutomation failed. Check logs/automation.log for details.")


if __name__ == "__main__":
    main()