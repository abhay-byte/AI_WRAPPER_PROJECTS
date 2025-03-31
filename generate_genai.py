import base64
import os
from google import genai
from pandas.core.dtypes.dtypes import re
from google.genai import types

def generate(input):
    
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
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
