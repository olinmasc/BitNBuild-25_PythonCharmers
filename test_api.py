import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


def test_gemini_api():
    """Test different API endpoints to find what works with your key."""

    if not API_KEY:
        print("❌ GOOGLE_API_KEY is not set in .env file")
        return

    print(f"🔑 Testing API Key: {API_KEY[:20]}...")
    print()

    # Test different endpoints and models
    test_cases = [
        {
            "name": "Gemini 2.0 Flash (v1beta)",
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}",
        },
        {
            "name": "Gemini 2.5 Flash (v1beta)",
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}",
        },
        {
            "name": "Gemini 2.5 Pro (v1beta)",
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}",
        },
        {
            "name": "Gemini 1.5 Flash (v1beta)",
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
        },
        {
            "name": "Gemini 1.5 Pro (v1beta)",
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}",
        },
        {
            "name": "Gemini Pro (v1beta)",
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}",
        },
        {
            "name": "Gemini 1.0 Pro (v1beta)",
            "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={API_KEY}",
        }
    ]

    # Simple text prompt to test
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Hello, can you respond with just 'API is working'?"}
                ]
            }
        ]
    }

    working_endpoints = []

    for test in test_cases:
        print(f"🧪 Testing: {test['name']}")

        try:
            response = requests.post(
                test['url'],
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            print(f"   Status Code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    print(f"   ✅ SUCCESS: {content[:50]}...")
                    working_endpoints.append(test['name'])
                else:
                    print(f"   ⚠️  No content in response")
            elif response.status_code == 404:
                print(f"   ❌ Model not found (404)")
            elif response.status_code == 403:
                print(f"   🚫 Access forbidden (403) - Check API key permissions")
            elif response.status_code == 400:
                print(f"   ⚠️  Bad request (400): {response.text[:100]}")
            else:
                print(f"   ❓ Other error: {response.text[:100]}")

        except requests.exceptions.RequestException as e:
            print(f"   💥 Network error: {str(e)}")

        print()

    print("=" * 50)
    if working_endpoints:
        print(f"✅ WORKING ENDPOINTS: {', '.join(working_endpoints)}")
        print("\nYou can use any of these models in your app!")
    else:
        print("❌ NO WORKING ENDPOINTS FOUND")
        print("\nPossible issues:")
        print("1. API key is from Google Cloud Console instead of Google AI Studio")
        print("2. API key doesn't have Generative Language API enabled")
        print("3. API key has restrictions that block these endpoints")
        print("4. Account/billing issues")
        print("\nSolutions:")
        print("1. Get a new API key from: https://aistudio.google.com/app/apikey")
        print("2. Make sure you're using Google AI Studio, NOT Google Cloud Console")


if __name__ == "__main__":
    test_gemini_api()
