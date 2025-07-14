import os
import streamlit as st
from scraping import get_user_content
from persona_generator import generate_persona

st.set_page_config(page_title="Reddit User Persona Generator")

st.title("👨‍💻 Reddit User Persona Generator")

profile_url = st.text_input(
    "Enter Reddit Profile URL (e.g., https://www.reddit.com/user/kojied/)"
)

if st.button("Generate Persona") and profile_url:
    with st.spinner("Scraping Reddit profile..."):
        username, data = get_user_content(profile_url)

    with st.spinner("Generating persona using Groq..."):
        persona = generate_persona(data, username)

    st.success("✅ Persona generated!")

    # Show persona in app
    st.text_area("Generated Persona", value=persona, height=400)

    # Ensure output folder exists
    os.makedirs("personas", exist_ok=True)
    file_path = f"personas/{username}_persona.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(persona)

    with open(file_path, "rb") as f:
        st.download_button(
            label="📥 Download Persona as a text file",
            data=f,
            file_name=f"{username}_persona.md",
            mime="text/plain"
        )
