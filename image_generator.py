import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Handles interaction with the Google GenAI SDK."""
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> bytes | None:
        logger.info(f"Generating image with prompt: {prompt}")
        try:
            response = self.client.models.generate_content(
                model='gemini-3-pro-image-preview',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE'],
                )
            )
            for part in response.parts:
                if part.inline_data:
                    return part.inline_data.data
            
            logger.warning("No image generated")
            return None
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
