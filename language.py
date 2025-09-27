import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


def generate_content(description):
    """
    Generates content using the Google AI Gemini API endpoint.
    """
    if not API_KEY:
        return "Error: GOOGLE_API_KEY is not set."

    # Updated list to match the WORKING models from your test
    models_to_try = [
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-2.5-pro"
    ]

    prompt = f"""Based on this image description: "{description}"

Create a comprehensive social media content package with the following sections:

## 🎨 Caption Variations

### 😄 Witty Caption
[Create a clever, humorous caption that might include wordplay or a fun observation]

### ✨ Inspirational Caption  
[Create an uplifting, motivational caption that inspires the audience]

### 👔 Professional Caption
[Create a polished caption suitable for business or professional contexts]

### 😊 Casual Caption
[Create a friendly, relaxed caption like you're talking to a close friend]

## #️⃣ Hashtag Recommendations

### Trending Hashtags (High Reach)
[5 popular, high-volume hashtags]

### Niche Hashtags (Targeted Audience)  
[5 specific, relevant hashtags for targeted engagement]

### Branded/Community Hashtags
[5 community or brand-specific hashtags]

## 📊 Content Insights

### 🎭 Mood Analysis
[Describe the emotional tone and atmosphere of the image]

### 🎯 Target Audience
[Suggest who would most engage with this content]

### ⏰ Best Posting Times
[Suggest optimal times to post this type of content]

### 💡 Engagement Tips
[2-3 specific tips to increase engagement for this post]

Format everything clearly with emojis and proper markdown formatting. Make it engaging and actionable!"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
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

    try:
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

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
