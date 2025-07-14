import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt():
    """Construct a factual persona generation prompt for the LLM."""
    prompt = (
        "You are an analyst tasked with building a Reddit user's persona profile "
        "based on their public activity. Use the user's actual posts/comments below. "
        "Generate a concise structured persona. The following fields are examples:\n"
        "- Username\n"
        "- Location\n"
        "- Goals and needs\n"
        "- Motivations\n"
        "- Frustrations or pain points\n"
        "- Personality traits\n"
        "- Communication style or tone\n"
        "- Online behavior or Reddit usage patterns\n\n"
        "⚠️ IMPORTANT RULES:\n"
        "Do not output a persona yet. I will send you the Reddit content in chunks.\n"
        "Now analyze the following Reddit activity:\n\n"
    )
    return prompt

def generate_persona(data, username, chunk_size=10):
    """Send Reddit activity to the model in batches, then ask for the persona."""
    messages = []

    # System prompt (rules and instructions)
    messages.append({
        "role": "system",
        "content": build_prompt()
    })

    # Break activity into batches
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        chunk_text = ""
        for item in chunk:
            chunk_text += f"Text: {item['text']} Source: {item['url']}\n\n"

        messages.append({
            "role": "user",
            "content": f"Here is another batch of Reddit activity:\n\n{chunk_text}"
        })

    # Final instruction after all data is sent
    messages.append({
        "role": "user",
        "content": (
            f"Now that you have all the data, generate a structured user persona for {username}"
            "Format output in Markdown."
        )
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content
