import schedule
import time
import logging
from datetime import datetime

# Import configuration and services
import config
from state_manager import StateManager
from image_generator import ImageGenerator
from email_service import EmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def job_ghibli():
    """The job for Ghibli characters."""
    logger.info("Starting Ghibli job")
    
    if not config.GOOGLE_API_KEY:
        logger.error("GOOGLE_API_KEY not found in environment variables")
        return
    if not config.GMAIL_USER or not config.GMAIL_PASSWORD:
        logger.error("GMAIL credentials not found")
        return

    # Initialize services
    state_manager = StateManager(config.STATE_FILE)
    image_generator = ImageGenerator(config.GOOGLE_API_KEY)
    email_service = EmailService(config.GMAIL_USER, config.GMAIL_PASSWORD)

    # Check if already run today
    if not state_manager.can_run_today():
        today_str = datetime.now().strftime("%Y-%m-%d")
        logger.info(f"Ghibli job already ran today ({today_str}). Skipping")
        return

    # Calculate next index
    next_index = state_manager.get_next_index(len(config.DETAILED_CONTENTS))
    content = config.DETAILED_CONTENTS[next_index]
    logger.info(f"Processing Ghibli Item {next_index + 1}/{len(config.DETAILED_CONTENTS)}")
    
    prompt = config.PROMPT_TEMPLATE.format(detailed_content=content)
    
    # Step 1: Generate image
    generated_image = image_generator.generate(prompt)
    if not generated_image:
        logger.error("Failed to generate image. Not updating state")
        return

    # Step 2: Send email
    recipient = config.RECIPIENT_EMAIL or config.GMAIL_USER
    email_service.send_image(recipient, generated_image, subject_suffix=f" - Ghibli {next_index + 1}")

    # Step 3: Update state
    today_str = datetime.now().strftime("%Y-%m-%d")
    state_manager.save(next_index, today_str)
    logger.info(f"Ghibli state updated: Index {next_index}, Date {today_str}")

def job_daily_objects():
    """The job for daily objects."""
    logger.info("Starting Daily Objects job")
    
    if not config.GOOGLE_API_KEY:
        logger.error("GOOGLE_API_KEY not found in environment variables")
        return
    if not config.GMAIL_USER or not config.GMAIL_PASSWORD:
        logger.error("GMAIL credentials not found")
        return

    # Initialize services with separate state file
    state_manager = StateManager(config.DAILY_OBJECTS_STATE_FILE)
    image_generator = ImageGenerator(config.GOOGLE_API_KEY)
    email_service = EmailService(config.GMAIL_USER, config.GMAIL_PASSWORD)

    # Check if already run today
    if not state_manager.can_run_today():
        today_str = datetime.now().strftime("%Y-%m-%d")
        logger.info(f"Daily Objects job already ran today ({today_str}). Skipping")
        return

    # Calculate next index
    next_index = state_manager.get_next_index(len(config.DAILY_OBJECTS))
    content = config.DAILY_OBJECTS[next_index]
    logger.info(f"Processing Daily Object {next_index + 1}/{len(config.DAILY_OBJECTS)}")
    
    prompt = config.DAILY_OBJECTS_PROMPT_TEMPLATE.format(detailed_content=content)
    
    # Step 1: Generate image
    generated_image = image_generator.generate(prompt)
    if not generated_image:
        logger.error("Failed to generate image. Not updating state")
        return

    # Step 2: Send email
    recipient = config.RECIPIENT_EMAIL or config.GMAIL_USER
    email_service.send_image(recipient, generated_image, subject_suffix=f" - Daily Object {next_index + 1}")

    # Step 3: Update state
    today_str = datetime.now().strftime("%Y-%m-%d")
    state_manager.save(next_index, today_str)
    logger.info(f"Daily Objects state updated: Index {next_index}, Date {today_str}")

def main():
    logger.info("Hand Painting Generator Service Started")
    logger.info("Schedule:")
    logger.info("  - Ghibli Characters: Daily at 09:00 AM")
    logger.info("  - Daily Objects: Daily at 15:00 PM")
    
    # Run once immediately on startup if needed, or just wait for schedule
    # Uncomment the next lines to run immediately upon container start for testing
    # job_ghibli()
    job_daily_objects()

    # Schedule both jobs
    # schedule.every().day.at("09:00").do(job_ghibli)
    # schedule.every().day.at("15:00").do(job_daily_objects)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

