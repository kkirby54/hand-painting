import schedule
import time
from datetime import datetime

# Import configuration and services
import config
from state_manager import StateManager
from image_generator import ImageGenerator
from email_service import EmailService

def job():
    """The job to be scheduled."""
    print(f"Starting scheduled job at {datetime.now()}")
    
    if not config.GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return
    if not config.GMAIL_USER or not config.GMAIL_PASSWORD:
        print("Error: GMAIL credentials not found.")
        return

    # Initialize services
    state_manager = StateManager(config.STATE_FILE)
    image_generator = ImageGenerator(config.GOOGLE_API_KEY)
    email_service = EmailService(config.GMAIL_USER, config.GMAIL_PASSWORD)

    # Check if already run today
    if not state_manager.can_run_today():
        today_str = datetime.now().strftime("%Y-%m-%d")
        print(f"Already ran today ({today_str}). Skipping.")
        return

    # Calculate next index
    next_index = state_manager.get_next_index(len(config.DETAILED_CONTENTS))
    content = config.DETAILED_CONTENTS[next_index]
    print(f"Processing Item {next_index + 1}/{len(config.DETAILED_CONTENTS)}")
    
    prompt = config.PROMPT_TEMPLATE.format(detailed_content=content)
    
    # Step 1: Generate image
    generated_image = image_generator.generate(prompt)
    if not generated_image:
        print("Failed to generate image. Not updating state.")
        return

    # Step 2: Send email
    recipient = config.RECIPIENT_EMAIL or config.GMAIL_USER
    email_service.send_image(recipient, generated_image, subject_suffix=f" - {next_index + 1}")

    # Step 3: Update state
    today_str = datetime.now().strftime("%Y-%m-%d")
    state_manager.save(next_index, today_str)
    print(f"State updated: Index {next_index}, Date {today_str}")

def main():
    print("Hand Painting Generator Service Started")
    print("Schedule: Running daily at 09:00 AM (Server Time)")
    
    # Run once immediately on startup if needed, or just wait for schedule
    # Uncomment the next line to run immediately upon container start for testing
    # job()

    # Schedule the job
    schedule.every().day.at("09:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
