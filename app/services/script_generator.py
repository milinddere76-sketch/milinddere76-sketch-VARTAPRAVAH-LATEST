from groq import Groq
import os
from app import config

# Using config.GROQ_API_KEY for consistency with the project structure
client = Groq(api_key=config.GROQ_API_KEY or os.getenv("GROQ_API_KEY"))

def generate_script(news):
    """Uses Groq (Llama 3.1) to generate the news script."""
    try:
        # Convert list of news to string if necessary
        if isinstance(news, list):
            news = "\n".join(news)
            
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a professional, senior Marathi news anchor at Varta Pravah. "
                        "Your task is to convert raw news headlines into a formal, grammatically perfect, and meaningful news script. "
                        "Use high-quality journalistic Marathi vocabulary (शुद्ध मराठी). "
                        "Do not use literal translations; ensure the sentences flow naturally like a real news broadcast. "
                        "Structure the script with a strong opening (नमस्कार, मी आहे आपला AI रिपोर्टर...), a detailed body, and a professional closing."
                    )
                },
                {"role": "user", "content": news}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Groq error:", e)
        return None

# Maintaining the class wrapper for the scheduler if it uses it
class ScriptGenerator:
    def generate_marathi_script(self, news_items):
        return generate_script(news_items)
