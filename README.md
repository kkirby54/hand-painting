# Hand Painting Image Generator

This project takes a hand-drawn sketch from `resources/`, analyzes it using Gemini, generates a high-quality version using `gemini-3-pro-image-preview`, and emails the result.

## Setup

1.  **Install `uv`**: Ensure you have `uv` installed.
2.  **Environment Variables**:
    *   Copy `.env.example` to `.env`.
    *   Fill in your `GOOGLE_API_KEY` (with access to Gemini models).
    *   Fill in your `GMAIL_USER` and `GMAIL_PASSWORD` (App Password recommended).
    *   Set the `RECIPIENT_EMAIL`.

## Running

Run the script using `uv`:

```bash
uv run main.py
```

## Docker

Build and run with Docker:

```bash
docker build -t hand-painting .
docker run --env-file .env hand-painting
```
