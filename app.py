import os
import html
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="MailCraft AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    .stApp {
        background: #f7f8fc;
        color: #172033;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 0;
    }

    [data-testid="stSidebar"] * {
        color: #eef2ff !important;
    }

    .brand {
        font-family: 'Playfair Display', serif;
        font-size: 30px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
    }

    .tagline {
        color: #667085;
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        margin-bottom: 22px;
    }

    .hero {
        padding: 28px 30px;
        border-radius: 24px;
        background: linear-gradient(135deg, #111827 0%, #312e81 55%, #7c3aed 100%);
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 18px 45px rgba(49, 46, 129, 0.16);
    }

    .hero h1 {
        font-family: 'Playfair Display', serif;
        font-size: 42px;
        line-height: 1.05;
        margin: 0 0 9px 0;
    }

    .hero p {
        margin: 0;
        color: #e9e7ff;
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
    }

    .section-card {
        background: white;
        border: 1px solid #e7e9f0;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(16, 24, 40, 0.04);
        min-height: 470px;
    }

    .section-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #667085;
        font-size: 13px;
        margin-bottom: 16px;
    }

    .mode-pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: #f0edff;
        color: #5b35d5;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .result-box {
        background: #fbfbfe;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        white-space: pre-wrap;
        line-height: 1.65;
        min-height: 300px;
        font-family: 'DM Sans', sans-serif;
    }

    .empty-state {
        text-align: center;
        padding: 90px 20px;
        color: #667085;
    }

    .empty-icon {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .tip {
        padding: 12px 14px;
        border-radius: 12px;
        background: #f5f3ff;
        border: 1px solid #e9e3ff;
        color: #4c3a94;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 12px;
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 44px;
        border: 1px solid #d9dce5;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5b35d5, #7c3aed);
        border: 0;
    }

    .footer {
        text-align: center;
        color: #98a2b3;
        font-size: 12px;
        margin-top: 28px;
        padding-bottom: 10px;
    }

    textarea {
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")

def build_prompt(mode, email_type, tone, length, details, existing_email):
    if mode == "Generate Email":
        return f"""
You are MailCraft AI, an expert professional email writer.

Create a polished email based ONLY on the user's information.

Email type: {email_type}
Tone: {tone}
Length: {length}
User's message/details:
{details}

Requirements:
- Return a clear "Subject:" line first.
- Then write the complete email body.
- Do not invent names, dates, organizations, facts, attachments, or promises.
- Make the wording natural, concise, and professional.
- Do not add explanations before or after the email.
"""

    if mode == "Improve Email":
        return f"""
You are MailCraft AI, an expert email editor.

Improve the email below while preserving its original meaning and factual details.

Desired tone: {tone}
Desired length: {length}

Original email:
{existing_email}

Requirements:
- Return a clear "Subject:" line if the original has one; otherwise create a concise subject based only on the email content.
- Then provide the improved email.
- Fix grammar, clarity, structure, and professionalism.
- Do not invent facts.
- Do not add explanations before or after the email.
"""

    return f"""
You are MailCraft AI, an expert email reply writer.

Write a natural reply to the email below.

Reply tone: {tone}
Reply length: {length}
Additional instructions:
{details if details else "No additional instructions."}

Received email:
{existing_email}

Requirements:
- Return a clear "Subject:" line first.
- Then write the complete reply.
- Answer or acknowledge the message appropriately.
- Do not invent facts, commitments, dates, or information.
- Do not add explanations before or after the reply.
"""

def generate_email(prompt):
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "Groq API key is missing. Add GROQ_API_KEY to Streamlit Cloud Secrets."
        )

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You write high-quality emails. Follow the requested format exactly."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.65,
        max_tokens=1200,
    )
    return response.choices[0].message.content.strip()

# ---------- State ----------
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="brand">✦ MailCraft AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Write better emails, effortlessly.</div>', unsafe_allow_html=True)

    st.markdown("### Workspace")
    mode = st.radio(
        "Choose an action",
        ["Generate Email", "Improve Email", "Reply to Email"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Quick tips")
    st.markdown(
        '<div class="tip">Be specific about the purpose and key points. '
        'MailCraft will handle the structure and wording.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="tip">Your API key is read from Streamlit Secrets and is never displayed in the app.</div>',
        unsafe_allow_html=True,
    )

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <h1>Your words. Better emails.</h1>
    <p>Generate, improve, or reply to emails with a polished AI writing assistant.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Main UI ----------
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="mode-pill">{html.escape(mode)}</div>', unsafe_allow_html=True)

    if mode == "Generate Email":
        st.markdown('<div class="section-title">Create a new email</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Tell AI what you want to say.</div>', unsafe_allow_html=True)

        email_types = [
            "Job Application", "Internship", "Leave Request", "Meeting Request",
            "Follow-up", "Thank You", "Complaint", "Business Inquiry",
            "Customer Support", "Cold Email", "Other"
        ]
        email_type = st.selectbox("Email type", email_types)

        c1, c2 = st.columns(2)
        with c1:
            tone = st.selectbox(
                "Tone",
                ["Professional", "Formal", "Friendly", "Polite", "Casual", "Apologetic"]
            )
        with c2:
            length = st.selectbox("Length", ["Short", "Medium", "Detailed"])

        details = st.text_area(
            "What do you want to say?",
            height=190,
            placeholder="Example: I want to apply for a Python internship. Mention that I have built AI and Streamlit projects and ask about the application process.",
        )
        existing_email = ""

    else:
        st.markdown(f'<div class="section-title">{mode}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Paste the email and let AI improve the wording.</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)
        with c1:
            tone = st.selectbox(
                "Tone",
                ["Professional", "Formal", "Friendly", "Polite", "Casual", "Apologetic"],
                key="edit_tone"
            )
        with c2:
            length = st.selectbox(
                "Length",
                ["Short", "Medium", "Detailed"],
                key="edit_length"
            )

        existing_email = st.text_area(
            "Paste email",
            height=185,
            placeholder="Paste the email you received or your draft here...",
        )

        details = st.text_area(
            "Additional instructions (optional)",
            height=95,
            placeholder="Example: Make it more concise and confident.",
        )
        email_type = "General"

    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button(
        "✨ Generate Email",
        type="primary",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI result</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Your polished email will appear here.</div>', unsafe_allow_html=True)

    if generate:
        valid_input = details.strip() if mode == "Generate Email" else existing_email.strip()

        if not valid_input:
            st.warning(
                "Please provide some content first. Tell me what you want to say or paste an email."
            )
        else:
            prompt = build_prompt(
                mode, email_type, tone, length, details.strip(), existing_email.strip()
            )
            with st.spinner("Crafting your email..."):
                try:
                    st.session_state.generated_email = generate_email(prompt)
                except Exception as e:
                    error_text = str(e)
                    if "401" in error_text or "authentication" in error_text.lower():
                        st.error("Groq authentication failed. Check your GROQ_API_KEY.")
                    elif "model" in error_text.lower() and "not found" in error_text.lower():
                        st.error("The selected Groq model is unavailable. Update the model name in app.py.")
                    else:
                        st.error(f"Could not generate the email: {error_text}")

    result = st.session_state.generated_email

    if result:
        st.markdown(
            f'<div class="result-box">{html.escape(result)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            st.download_button(
                "📥 Download .txt",
                data=result,
                file_name="mailcraft_email.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with b2:
            # Streamlit does not provide a universal clipboard API for every browser.
            # Showing the text in a code block/text area makes browser copying easy.
            st.info("Select the email text above and copy it with Ctrl+C.")
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">✉️</div>
            <strong>Your email is waiting to be written.</strong>
            <p>Choose an action, add your details, and click Generate Email.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer">MailCraft AI V1 • Built with Streamlit + Groq</div>',
    unsafe_allow_html=True
)
