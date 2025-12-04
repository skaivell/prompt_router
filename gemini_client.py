from google import genai

from config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def get_answer_from_gemini(prompt: str):
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    )

    return response.text
