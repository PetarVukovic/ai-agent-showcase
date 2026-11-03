import os
from dotenv import dotenv_values

def google_key():
 key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
 if key: return key
 source=os.getenv("PROVIDER_ENV_FILE")
 return dotenv_values(source).get("GOOGLE_API_KEY") if source else None
