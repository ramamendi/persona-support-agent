import os
from google import genai
from .escalator import should_escalate,handoff
from dotenv import load_dotenv
load_dotenv()

def generate_adaptive_response(user_query,persona,contexts):
    if should_escalate(user_query,contexts):
        return {
            'escalated':True,
            'response':'Your issue requires human review.',
            'handoff_summary':handoff(user_query,persona,contexts)
        }

    templates={
        'Technical Expert':'Provide detailed technical analysis and steps.',
        'Frustrated User':'Start empathetically and provide simple actions.',
        'Business Executive':'Focus on business impact and timelines.'
    }

    context='\n'.join([c['text'] for c in contexts])
    client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    r=client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=user_query,
        config={
            'system_instruction':f"{templates.get(persona)}\nOnly use:\n{context}"
        }
    )
    return {'escalated':False,'response':r.text,'handoff_summary':None}
