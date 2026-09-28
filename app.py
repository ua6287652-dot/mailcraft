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

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background: #f7f8fc;
    color: #172033;
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827 !important;
}
[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #f8fafc !important;
}
.sidebar-tip {
    background: #f1edff;
    border: 1px solid #ddd4ff;
    border-radius: 14px;
    padding: 14px;
    margin: 10px 0;
    color: #34256f !important;
    font-size: 13px;
    line-height: 1.45;
}
.sidebar-tip strong,
.sidebar-tip span {
    color: #34256f !important;
}

/* Brand */
.brand {
    font-family: 'Playfair Display', serif !important;
    font-size: 30px !important;
    font-weight: 700;
    color: #ffffff !important;
}
.tagline {
    color: #dbe4f0 !important;
    font-size: 14px;
    margin-bottom: 24px;
}

/* Hero */
.hero {
    padding: 28px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #111827 0%, #312e81 55%, #7c3aed 100%);
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 18px 45px rgba(49, 46, 129, .16);
}
.hero h1 {
    font-family: 'Playfair Display', serif !important;
    color: #ffffff !important;
    font-size: 42px;
    line-height: 1.05;
    margin: 0 0 8px 0;
}
.hero p {
    color: #eeeaff !important;
    margin: 0;
    font-size: 16px;
}

/* Section headings */
.section-title {
    color: #172033 !important;
    font-size: 20px;
    font-weight: 700;
    margin-top: 4px;
}
.section-subtitle {
    color: #667085 !important;
    font-size: 13px;
    margin-bottom: 16px;
}
.mode-pill {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: #f0edff;
    color: #5b35d5 !important;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 8px;
}

/* ALL text areas: dark editor + white typing */
[data-testid="stTextArea"] textarea {
    background-color: #242631 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
    border: 1px solid #414552 !important;
    border-radius: 12px !important;
    font-size: 14px !important;
    line-height: 1.55 !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: #b9bfca !important;
    -webkit-text-fill-color: #b9bfca !important;
    opacity: 1 !important;
}
[data-testid="stTextArea"] label,
[data-testid="stTextArea"] label p {
    color: #172033 !important;
}

/* Select boxes */
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p {
    color: #172033 !important;
}
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] * {
    color: #172033 !important;
}

/* Buttons */
div.stButton > button {
    border-radius: 12px !important;
    min-height: 44px !important;
    font-weight: 700 !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #5b35d5, #7c3aed) !important;
    color: white !important;
    border: 0 !important;
}

/* Result area */
.result-label {
    color: #172033 !important;
    font-size: 20px;
    font-weight: 700;
}
.result-sub {
    color: #667085 !important;
    font-size: 13px;
    margin-bottom: 16px;
}

/* Empty result */
.empty-result {
    min-height: 365px;
    border: 1px dashed #cfd4df;
    border-radius: 18px;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: #667085;
    padding: 30px;
}
.empty-result .icon {
    font-size: 42px;
    margin-bottom: 10px;
}
.empty-result strong {
    color: #344054;
}
.empty-result p {
    color: #667085;
    margin-top: 6px;
}

/* Footer */
.footer {
    text-align: center;
    color: #98a2b3;
    font-size: 12px;
    margin-top: 30px;
    padding-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- Helpers ----------------
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

Create a polished email using ONLY the user's information.

Email type: {email_type}
Tone: {tone}
Length: {length}
User details:
{details}

Return:
Subject: [concise subject]

[email body]

Rules:
- Do not invent names, dates, organizations, facts, attachments, or promises.
- Make the email natural, clear, and professional.
- Do not add explanations outside the email.
"""
    if mode == "Improve Email":
        return f"""
You are MailCraft AI, an expert email editor.

Improve this email while preserving its meaning and factual information.

Tone: {tone}
Length: {length}

Original email:
{existing_email}

Additional instructions:
{details if details else "None"}

Return only:
Subject: [subject]

[improved email]

Do not invent facts or add explanations.
"""
    return f"""
You are MailCraft AI, an expert email reply writer.

Write a suitable reply to the received email.

Tone: {tone}
Length: {length}
Additional instructions:
{details if details else "None"}

Received email:
{existing_email}

Return only:
Subject: [subject]

[reply]

Do not invent facts, dates, commitments, or other information.
"""


def generate_email(prompt):
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Groq API key is missing. Add GROQ_API_KEY to Streamlit Secrets.")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You write high-quality professional emails."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.65,
        max_tokens=1200,
    )
    return response.choices[0].message.content.strip()


# ---------------- State ----------------
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

# ---------------- Sidebar ----------------
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
    st.markdown("### Quick Tips")
    st.markdown(
        '<div class="sidebar-tip"><strong>💡 Be specific</strong><br>'
        '<span>Tell MailCraft the purpose and key points. It will handle the structure and wording.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-tip"><strong>🔐 Your privacy</strong><br>'
        '<span>Your Groq API key is loaded from Streamlit Secrets and is not displayed in the app.</span></div>',
        unsafe_allow_html=True,
    )


# ---------------- Hero ----------------
st.markdown("""
<div class="hero">
    <h1>Your words. Better emails.</h1>
    <p>Generate, improve, or reply to emails with a polished AI writing assistant.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- Workspace ----------------
left, right = st.columns([1, 1], gap="large")

# LEFT: input
with left:
    st.markdown(f'<div class="mode-pill">{html.escape(mode)}</div>', unsafe_allow_html=True)

    if mode == "Generate Email":
        st.markdown('<div class="section-title">Create a new email</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Tell AI what you want to say.</div>', unsafe_allow_html=True)

        email_type = st.selectbox(
            "Email type",
            [
                "Job Application", "Internship", "Leave Request", "Meeting Request",
                "Follow-up", "Thank You", "Complaint", "Business Inquiry",
                "Customer Support", "Cold Email", "Other"
            ],
        )

        c1, c2 = st.columns(2)
        with c1:
            tone = st.selectbox(
                "Tone",
                ["Professional", "Formal", "Friendly", "Polite", "Casual", "Apologetic"],
                key="generate_tone",
            )
        with c2:
            length = st.selectbox(
                "Length",
                ["Short", "Medium", "Detailed"],
                key="generate_length",
            )

        details = st.text_area(
            "What do you want to say?",
            height=190,
            placeholder="Example: I want to apply for a Python internship. Mention my AI and Streamlit projects and ask about the application process.",
            key="generate_details",
        )
        existing_email = ""

    else:
        st.markdown(f'<div class="section-title">{html.escape(mode)}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Paste the email and let AI improve the wording.</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            tone = st.selectbox(
                "Tone",
                ["Professional", "Formal", "Friendly", "Polite", "Casual", "Apologetic"],
                key="edit_tone",
            )
        with c2:
            length = st.selectbox(
                "Length",
                ["Short", "Medium", "Detailed"],
                key="edit_length",
            )

        existing_email = st.text_area(
            "Paste email",
            height=185,
            placeholder="Paste the email you received or your draft here...",
            key="existing_email",
        )

        details = st.text_area(
            "Additional instructions (optional)",
            height=95,
            placeholder="Example: Make it more concise and confident.",
            key="additional_instructions",
        )
        email_type = "General"

    generate = st.button(
        "✨ Generate Email",
        type="primary",
        use_container_width=True,
    )


# RIGHT: result
with right:
    st.markdown('<div class="result-label">AI result</div>', unsafe_allow_html=True)
    st.markdown('<div class="result-sub">Your polished email will appear here.</div>', unsafe_allow_html=True)

    if generate:
        valid_input = details.strip() if mode == "Generate Email" else existing_email.strip()

        if not valid_input:
            st.warning("Please provide some content first.")
        else:
            prompt = build_prompt(
                mode,
                email_type,
                tone,
                length,
                details.strip(),
                existing_email.strip(),
            )
            with st.spinner("Crafting your email..."):
                try:
                    st.session_state.generated_email = generate_email(prompt)
                except Exception as e:
                    msg = str(e)
                    if "401" in msg or "authentication" in msg.lower():
                        st.error("Groq authentication failed. Check GROQ_API_KEY in Secrets.")
                    else:
                        st.error(f"Could not generate the email: {msg}")

    result = st.session_state.generated_email

    if result:
        st.text_area(
            "Generated email",
            value=result,
            height=365,
            label_visibility="collapsed",
            key="generated_result",
        )

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
            st.caption("Click the result → Ctrl+A → Ctrl+C")

    else:
        st.markdown("""
        <div class="empty-result">
            <div>
                <div class="icon">✉️</div>
                <strong>No email generated yet</strong>
                <p>Enter your email details on the left and click<br>
                <b>Generate Email</b>.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(
    '<div class="footer">MailCraft AI V1 • Streamlit + Groq</div>',
    unsafe_allow_html=True,
)
