# Redditfiles: User persona generator

This tool scrapes a Reddit user's posts and comments, then generates a structured **user persona** using LLM (Groq's LLaMA 3.1 model). It extracts factual data only from publicly available Reddit activity and summarizes the user's behavior, tone, goals, frustrations, and more.

---

## 🗂️ Project Structure

```

redditfiles
├── .env                      # Your Groq API key goes here
├── app.py                  # Entry point to run the scraper + persona generator
├── persona\_generator.py     # Sends prompt to Groq's LLM and receives the persona
├── scraping.py        # Scrapes Reddit posts & comments using Selenium
├── requirements.txt         # Python dependencies
├── personas/                # Directory where final persona .md files are saved
└── README.md                # This file

````

---

## 🚀 How It Works

1. Scrapes the given Reddit user's recent **posts** and **comments**
2. Sends them to a Groq-hosted LLaMA-3.1-8B model
3. The model generates a structured persona — only using evidence from the text
4. The result is saved to:  
   **`personas/<username>_persona.md`**

---

## ⚙️ Requirements

- Python 3.9+
- Chrome & ChromeDriver (installed and in PATH)
- A [Groq API key](https://console.groq.com/)

---

## 📦 Installation

```bash
git clone https://github.com/shrivastavanolo/Redditfiles.git
cd redditfiles
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
````

---

## 🔑 Set Up Environment

Create a `.env` file in the root folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Usage

1. Run script

```bash
streamlit run app.py 
```
This will open streamlit UI deploy deployment for the webapp

2. Input the reddit user URL and hit the generate button

This will:

* Scrape the user’s 10 most recent posts and comments (limit can be adjusted via the script)
* Build and send the LLM prompt
* Save the final persona to `personas/{username}_persona.md`
* Also has the option to download the text file or directly copy text from the UI

---

## 🌐 Live Deployment

[https://reddit-persona.vercel.app](https://reddit-persona.vercel.app)

---

## Generated Persona Format

The LLM will return Markdown like:

```markdown
## Persona for Reddit User: spez

- **Username**: spez  
- **Occupation**: CEO of Reddit  
- **Tone**: Direct, opinionated  
- **Motivations**: Improve platform experience  
- **Frustrations**: Community backlash  
- **Reddit Usage**: Frequently posts on r/announcements  
...
```

Each detail is backed by source evidence — no hallucination.

---

## Example Output

You can find saved personas in the `/personas/` directory.

---
