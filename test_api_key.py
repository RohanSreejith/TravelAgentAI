import google.generativeai as genai
import os

# Set your API key (you can also use environment variables)
genai.configure(api_key="AIzaSyBGwZk52pLOaHI1M7NgSdoswUNwsQXpqhs")

# Use Gemini model
model = genai.GenerativeModel("gemini-pro")

try:
    response = model.generate_content("Say hello in 3 different languages.")
    print("✅ API is working!")
    print("Response:\n", response.text)
except Exception as e:
    print("❌ API call failed:", e)
