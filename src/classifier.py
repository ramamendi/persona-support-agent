import os, json
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def classify_customer_persona(user_message:str)->dict:
    client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    schema={
        "type":"OBJECT",
        "properties":{
            "persona":{"type":"STRING","enum":["Technical Expert","Frustrated User","Business Executive"]},
            "confidence":{"type":"NUMBER"},
            "reasoning":{"type":"STRING"}
        },
        "required":["persona","confidence","reasoning"]
    }
    response=client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=user_message,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.1
        )
    )
    return json.loads(response.text)
