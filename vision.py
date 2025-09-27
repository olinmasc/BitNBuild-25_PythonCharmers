import os
import requests
import base64
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


def analyze_image(image_file):
    """
    Analyzes an image using the Google AI Gemini API endpoint.
    """
    if not API_KEY:
        return "Error: GOOGLE_API_KEY is not set."

    # Try different model versions that are currently available
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro",
        "gemini-pro-vision"
    ]

    try:
        # Reset file pointer to beginning
        image_file.seek(0)
        image = Image.open(image_file)

        # Convert image to bytes with proper format detection
        byte_arr = io.BytesIO()

        # Determine the correct format and mime type
        if image.format == 'PNG':
            image.save(byte_arr, format='PNG')
            mime_type = "image/png"
        else:
            # Convert to RGB if necessary (for JPEG compatibility)
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            image.save(byte_arr, format='JPEG', quality=85)
            mime_type = "image/jpeg"

        image_bytes = byte_arr.getvalue()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        prompt = """Analyze this image for social media content creation. Please provide:
        
        1. A detailed description of what you see in the image
        2. The overall mood and atmosphere 
        3. Key objects, people, or elements present
        4. The setting or environment
        5. Colors and visual style
        6. Any emotions or feelings the image conveys
        
        Make your analysis engaging and suitable for social media content creation."""

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }

        # Try each model until one works
        for model_name in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"

            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result and result['candidates']:
                        if 'content' in result['candidates'][0]:
                            return result['candidates'][0]['content']['parts'][0]['text']
                    continue  # Try next model if this one doesn't return content

                elif response.status_code == 404:
                    continue  # Try next model
                elif response.status_code == 403:
                    return f"Error: Access forbidden. Your API key may not have permission to use Generative Language API. Please check that your API key from Google AI Studio has proper permissions."
                elif response.status_code == 503:
                    return f"Error: Google's Gemini API service is temporarily unavailable (503). This is usually temporary - please try again in a few minutes. The servers may be overloaded or under maintenance."
                elif response.status_code == 429:
                    return f"Error: Rate limit exceeded. Please wait a moment before trying again."
                else:
                    continue  # Try next model

            except requests.exceptions.RequestException:
                continue  # Try next model

        # If all models failed
        return f"Error: All available Gemini models failed to respond. Please verify your API key is from Google AI Studio (ai.google.dev) and try again later. Models tried: {', '.join(models_to_try)}"

    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
