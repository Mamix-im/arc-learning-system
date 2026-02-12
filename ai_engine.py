import os
from openai import OpenAI


# Render environment se API key lo
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)


def demo_ai(q):

    q = q.lower()

    if "english" in q:
        return "Practice English daily. Speak for 15 minutes."

    if "job" in q or "career" in q:
        return "Build skills and apply daily."

    if "money" in q:
        return "Learn freelancing and online skills."

    if "motivation" in q:
        return "Never quit. Small steps matter."

    return "Keep learning. You are improving every day."


def ask_ai(question):

    # Safety check
    if not API_KEY:
        return "API key missing. Check Render settings."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful coach."},
                {"role": "user", "content": question}
            ],
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception:
        return demo_ai(question)
