import os
from dotenv import load_dotenv
from google import genai

# Force reload the environment
load_dotenv(override=True)
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("❌ Key still not found in environment!")
else:
    print(f"Key found: {key[:8]}...")
    try:
        # Pass the key directly into the Client
        client = genai.Client(api_key=key)
        
        # EXPLICIT TEST: Call a specific model
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Say 'Connection Verified'"
        )
        print(f"✅ Success! Gemini says: {response.text}")
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")