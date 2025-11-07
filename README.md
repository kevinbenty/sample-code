# sample-code

## AI Career Agent

A Streamlit application that analyzes resumes against job descriptions using Google's Gemini API.

### Features
- Resume and job description analysis
- AI-powered matching insights
- Keyword optimization suggestions
- Cover letter snippet generation

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.streamlit/secrets.toml` with your Gemini API key:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

3. Run the application:
```bash
streamlit run ai_agent_app.py
```