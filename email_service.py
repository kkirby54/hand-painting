import smtplib
from email.message import EmailMessage
from PIL import Image
import io

class EmailService:
    """Handles sending emails with attachments."""
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password

    def send_image(self, recipient: str, image_data: bytes | Image.Image, subject_suffix: str = ""):
        print(f"Sending email to {recipient}")
        msg = EmailMessage()
        msg['Subject'] = f'Generated Image from Hand Painting{subject_suffix}'
        msg['From'] = self.user
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
                smtp.login(self.user, self.password)
                smtp.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
