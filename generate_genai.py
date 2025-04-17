import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate(input):
    model = ["gemini-2.0-flash-thinking-exp-01-21", "gemini-2.0-flash",""]
    try:
        return generate_content(input,model[0])
    except Exception as error:
        print(error)
        print("Trying Another Model...")
        return generate_content(input,model[1])


def generate_content(input,model):
    
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    chunk = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    return chunk.text
