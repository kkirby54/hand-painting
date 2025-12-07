import os
import smtplib
import mimetypes
import json
import schedule
import time
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import io

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Update STATE_FILE to be in a dedicated data directory for easier volume mounting
DATA_DIR = Path("data")
STATE_FILE = DATA_DIR / "generation_state.json"

PROMPT_TEMPLATE = (
    "A detailed, hand-drawn graphite pencil sketch on textured drawing paper, "
    "mimicking the style of a page from a studio ghibli artist's sketchbook. "
    "The image focuses on {detailed_content}. "
    "The drawing relies on visible, confident pencil strokes to define basic shapes, "
    "using cross-hatching and dense shading to create simple volume and fuzzy textures. "
    "The eyes should have distinct white highlights against dark graphite. "
    "The background is minimalist, showing only the grain of the off-white paper and faint smudges, "
    "keeping the entire focus on the character. "
    "Natural, soft lighting suggests a real-life drawing context."
)

DETAILED_CONTENTS = [
    "a cluster of small Susuwatari (dust bunnies). They are essentially fuzzy, dense black circles created by scribbled, compacted graphite lines, with two distinct, wide circular white areas for eyes staring forward. The edges are soft and indistinct due to the fur texture.",
    "a single Kodama (tree spirit) head standing. It has a slightly wobbly, rounded rectangular head shape drawn with a clean but organic pencil outline. Three simple, dark, irregular circular holes represent its eyes and mouth.",
    "the small white Totoro (Chibi-Totoro) and the medium blue Totoro (Chu-Totoro) walking together. Chibi-Totoro is a simple, tiny, round bun-shape with rabbit-like ears, rendered with minimal shading. Chu-Totoro is a larger, rounded oval body defined by soft outlines and faint belly marking lines, carrying a small sack.",
    "the face of No-Face (Kaonashi). It is focused on a long, vertical oval mask shape defined by a clean outer line. The characteristic markings under the eyes and above the mouth are filled with soft grey graphite shading, and a tiny, subtle line indicates the mouth.",
    "Ponyo in her fish form. A very round, human-like face with big eyes is attached to a small, chubby, simple fish body with tiny fins. The entire shape is smooth and curved, rendered with gentle, flowing pencil lines.",
    
    "Jiji the black cat sitting stiffly in a front-facing pose. The focus is on his sleek, solid black silhouette created with dense, dark graphite shading. His large, pointed ears are disproportionately big compared to his head, and his wide, oval white eyes stand out sharply against the dark fur.",
    "Calcifer the fire demon burning on a log. He has a teardrop-shaped body with jagged, flickering edges drawn with loose, energetic pencil strokes to mimic fire. His large, expressive eyes and mouth are sketched with thick lines, conveying a grumpy but cute expression.",
    "Ootori-Sama (the giant duck spirit) standing. The drawing emphasizes the massive, egg-shaped volume of its body using soft, rounded hatching. It has a single leaf on its head, a tiny beak, and small webbed feet that look comically small supporting the large body.",
    "Boh transformed into a mouse, standing on hind legs. He is extremely chubby and round, rendered with soft, curved contour lines to emphasize his squishy weight. He has round mouse ears and tiny paws, looking slightly confused.",
    "the large Totoro standing upright, holding a simple umbrella. The drawing captures the iconic pear-shaped silhouette. The fur texture on his belly is detailed with inverted 'V' markings. The umbrella is sketched with straight, confident lines, contrasting with Totoro's fuzzy, round outline.",

    "a full-body sketch of No-Face (Kaonashi) standing quietly. The long, black, tube-like body is rendered with soft, vertical graphite shading to suggest a heavy, semi-transparent fabric texture. His arms hang loosely by his sides, and the white mask face is the focal point with high contrast against the dark body.",
    "a close-up portrait of Sosuke from 'Ponyo'. He has a round face and a short bowl-cut hairstyle. The hair is rendered with blocky, distinct pencil strokes to show the clumps and volume of the hair. His expression is serious and determined, with simple round eyes and a small button nose.",
    "a close-up of Mei from 'My Neighbor Totoro'. She has her signature pigtails held by hair ties, rendered with loose, curvy lines to show the hair's bounce. Her expression is joyful and energetic with a wide-open mouth (shouting or laughing), showing her teeth, captured with dynamic facial lines.",
    "Kiki's face viewed directly from the front. The large ribbon on her head is sketched with soft shading to show the fabric folds and volume. Her uneven bangs frame her face, drawn with quick, feathered strokes. Her eyes are large and reflective, with detailed pupils characteristic of the Ghibli style.",
    "Chihiro showing a shocked or surprised expression. Her eyes are wide open, detailed with distinct pupils and highlights to convey emotion. Her mouth is slightly open in a gasp. Her hair is pulled back into a high ponytail, but loose wisps of hair fall around her face, drawn with fine, faint pencil lines.",

    "a close-up portrait of Howl Jenkins Pendragon with dark short hair. The drawing focuses on delicate, elegant pencil strokes to render the fine texture of his hair falling over his forehead. He wears his signature earrings, and his expression is calm and charming with long eyelashes and distinct, deep eyes.",
    "San (Princess Mononoke) wearing her red clay mask and white wolf-fur cape. The mask is rendered with smooth, clean gradients, while the fur cape creates a contrast with rough, scribbled, and dense pencil textures. The circular eyes and mouth of the mask are dark and hollow, creating a mysterious atmosphere.",
    "a dynamic sketch of Kiki flying on her broomstick, viewed from the side. Her dark dress billows backwards, showing realistic fabric folds and wrinkles caused by the wind. Her hair flies wildly behind her. Her hands grip the broom handle tightly, and Jiji clings nervously to the back bristles. The lines are swift and gestural to suggest speed.",
    "a medium shot of the large Totoro sitting by the water (implied), holding a fishing rod. His posture is slumped and relaxed, emphasizing his heavy, rounded bottom. His tiny paws gently hold the thin rod. A small leaf is on his head, and he stares blankly at the line, capturing a quiet, whimsical moment.",
]

def load_state():
    """Loads the generation state from a JSON file."""
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error decoding state file. Starting fresh.")
    return {"last_processed_index": -1, "last_run_date": None}

def save_state(index, date_str):
    """Saves the generation state to a JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state = {
        "last_processed_index": index,
        "last_run_date": date_str
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def generate_image_from_prompt(client, prompt):
    """Generates an image using the Gemini API."""
    print(f"Generating image with prompt: {prompt}")
    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
            )
        )
        for part in response.parts:
            if part.inline_data:
                return part.inline_data.data
        
        print("No image generated.")
        return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def send_email_with_image(image_data, recipient, subject_suffix=""):
    """Sends the generated image via Gmail."""
    print(f"Sending email to {recipient}")
    msg = EmailMessage()
    msg['Subject'] = f'Generated Image from Hand Painting{subject_suffix}'
    msg['From'] = GMAIL_USER
    msg['To'] = recipient
    msg.set_content('Here is the image generated based on your hand painting prompt.')

    # Convert PIL Image to bytes if necessary
    if isinstance(image_data, Image.Image):
        img_byte_arr = io.BytesIO()
        image_data.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
    else:
        img_bytes = image_data

    # Add attachment
    msg.add_attachment(img_bytes, maintype='image', subtype='jpeg', filename='generated_image.jpg')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def job():
    """The job to be scheduled."""
    print(f"Starting scheduled job at {datetime.now()}")
    
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return
    if not GMAIL_USER or not GMAIL_PASSWORD:
        print("Error: GMAIL credentials not found.")
        return

    # Load state
    state = load_state()
    last_run_date = state.get("last_run_date")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Check if already run today
    if last_run_date == today_str:
        print(f"Already ran today ({today_str}). Skipping.")
        return

    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    # Calculate next index
    last_index = state.get("last_processed_index", -1)
    next_index = last_index + 1
    
    # Loop back if we reached the end
    if next_index >= len(DETAILED_CONTENTS):
        next_index = 0
        print("Reached end of list. Looping back to start.")

    content = DETAILED_CONTENTS[next_index]
    print(f"Processing Item {next_index + 1}/{len(DETAILED_CONTENTS)}")
    
    prompt = PROMPT_TEMPLATE.format(detailed_content=content)
    
    # Step 1: Generate image
    generated_image = generate_image_from_prompt(client, prompt)
    if not generated_image:
        print("Failed to generate image. Not updating state.")
        return

    # Step 2: Send email
    recipient = RECIPIENT_EMAIL or GMAIL_USER
    send_email_with_image(generated_image, recipient, subject_suffix=f" - {next_index + 1}")

    # Step 3: Update state
    save_state(next_index, today_str)
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
