import streamlit as st
import google.generativeai as genai
import time

# --- Configuration ---
# Set the page title and icon
st.set_page_config(page_title="AI Career Agent", page_icon="🤖")

# --- Helper Function ---
def get_gemini_response(prompt, retries=3, delay=5):
    """
    Calls the Gemini API with retry logic.
    
    Args:
        prompt (str): The complete prompt to send to the model.
        retries (int): Number of retries on failure.
        delay (int): Delay between retries in seconds.

    Returns:
        str: The generated text response or an error message.
    """
    try:
        # Load the API key from Streamlit's secrets
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Set up the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 4096,
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        
        # Generate content
        attempt = 0
        while attempt < retries:
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                attempt += 1
                if attempt >= retries:
                    # Log the final error
                    print(f"Final attempt failed: {e}")
                    return f"Error: Failed to get response from AI model after {retries} attempts. {e}"
                # Exponential backoff
                time.sleep(delay * (2 ** attempt)) 
                
    except KeyError:
        return "Error: `GEMINI_API_KEY` not found in Streamlit secrets. Please add it to your `.streamlit/secrets.toml` file."
    except Exception as e:
        # Catch other potential errors (e.g., configuration)
        return f"An unexpected error occurred: {e}"

# --- The "Agent" Prompt ---
# This is the core instruction for the AI.
# It defines its persona, mission, and output format.
AGENT_PROMPT = """
You are an expert AI Career Agent. Your mission is to provide a comprehensive analysis of a user's resume against a specific job description.

**USER-PROVIDED RESUME:**
{resume}

**USER-PROVIDED JOB DESCRIPTION:**
{job_description}

**YOUR TASK:**
Analyze both documents and generate a detailed, professional report in Markdown format. The report MUST include the following sections:

1.  **## 🎯 Overall Fit Analysis**
    * Provide a brief, encouraging summary (2-3 sentences) of the candidate's fit for the role.

2.  **## 🚀 Key Strengths & Matches**
    * Create a bulleted list of the top 3-5 skills or experiences from the resume that directly match the job description's requirements.
    * For each point, briefly explain *why* it's a strong match.

3.  **## 💡 Potential Gaps & Areas to Emphasize**
    * Identify 2-3 key requirements from the job description that are not clearly addressed in the resume.
    * Suggest how the candidate might address these gaps (e.g., "Consider adding a project that demonstrates X" or "Be prepared to discuss your experience with Y in an interview").

4.  **## 🔑 Resume Keyword Optimization**
    * List 5-10 specific keywords and phrases from the job description (like "Agile Methodologies," "Stakeholder Management," "Python," "Data Visualization") that the candidate should ensure are present in their resume (if applicable to their experience).

5.  **## ✉️ Draft: Tailored Cover Letter Snippet**
    * Write a concise, high-impact introductory paragraph (4-6 sentences) for a cover letter. This paragraph must be tailored to the job, referencing 1-2 key requirements from the job description and matching them with specific experiences from the resume. It should be ready for the user to copy and paste.

---
**IMPORTANT:** Format your entire response in clean, readable Markdown.
"""


# --- Streamlit UI ---

# Main Title
st.title("🤖 AI Career Agent")
st.markdown("Analyze your resume against a job description and get actionable insights.")
st.markdown("---")

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.header("📄 Your Resume")
    resume_text = st.text_area("Paste your full resume text here:", height=500, label_visibility="collapsed")

with col2:
    st.header("🔍 Job Description")
    job_description_text = st.text_area("Paste the job description text here:", height=500, label_visibility="collapsed")

# The "Analyze" button
if st.button("🚀 Analyze My Application", type="primary", use_container_width=True):
    
    # Simple validation
    if not resume_text or not job_description_text:
        st.error("Please paste both your resume and the job description.")
    elif len(resume_text) < 100:
        st.warning("Your resume seems short. For best results, paste the full text.")
    elif len(job_description_text) < 100:
        st.warning("The job description seems short. For best results, paste the full text.")
    else:
        # If validation passes, run the agent
        with st.spinner("🤖 Your AI agent is thinking... This may take a moment..."):
            
            # Format the final prompt
            final_prompt = AGENT_PROMPT.format(
                resume=resume_text, 
                job_description=job_description_text
            )
            
            # Call the AI
            response_text = get_gemini_response(final_prompt)
            
            # Display the result
            st.markdown("---")
            st.header("📝 Your Personalized Analysis")
            st.markdown(response_text)

# Footer/Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    """
    This application is a **project** demonstrating how to build an AI "agent" 
    using **Python**, **Streamlit**, and the **Gemini API**.
    
    You can find the full guide and code on [GitHub](https://github.com/).
    """
)
st.sidebar.header("How to Use")
st.sidebar.markdown(
    """
    1.  **Paste** your resume text into the left box.
    2.  **Paste** the text of a job description you're interested in into the right box.
    3.  **Click** the "Analyze" button.
    4.  **Review** the AI-generated report below!
    """
)
