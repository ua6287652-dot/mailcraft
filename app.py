import os
import html
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="MailCraft AI V2",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM CSS
# =========================================================
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

/* Titles */
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

/* Textareas */
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

/* Selects */
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
    transition: none !important;
}
div.stButton > button:hover {
    filter: none !important;
    transform: none !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #5b35d5, #7c3aed) !important;
    color: #ffffff !important;
    border: 0 !important;
}

/* Download button */
[data-testid="stDownloadButton"] button,
[data-testid="stDownloadButton"] button:hover,
[data-testid="stDownloadButton"] button:focus,
[data-testid="stDownloadButton"] button:active {
    background: #111827 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #111827 !important;
    box-shadow: none !important;
    transition: none !important;
}
[data-testid="stDownloadButton"] button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Hide keyboard shortcut control */
button[aria-label*="Keyboard"],
button[title*="Keyboard"],
button[aria-label*="keyboard"],
button[title*="keyboard"],
[data-testid*="Keyboard"],
[data-testid*="keyboard"] {
    display: none !important;
}

/* Cards */
.feature-card {
    background: #ffffff;
    border: 1px solid #e7e9f0;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}
.feature-card-title {
    color: #172033;
    font-weight: 700;
    font-size: 15px;
}
.feature-card-text {
    color: #667085;
    font-size: 13px;
    line-height: 1.5;
}

/* Result empty state */
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


# =========================================================
# GROQ
# =========================================================
def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")


def build_prompt(
    action,
    tone,
    language,
    purpose,
    length,
    audience,
    extra_instructions,
    email_text,
):
    if action == "Generate Email":
        task = f"""
Create a new email based on the user's information.

User's information:
{email_text}
"""
    elif action == "Improve Email":
        task = f"""
Improve the following email while preserving its meaning and factual information.

Original email:
{email_text}
"""
    else:
        task = f"""
Edit and rewrite the following email according to the user's customization settings.

Original email:
{email_text}
"""

    return f"""
You are MailCraft AI, a professional email writing assistant.

ACTION: {action}

CUSTOMIZATION:
- Tone: {tone}
- Language: {language}
- Purpose: {purpose}
- Length: {length}
- Audience: {audience}
- Additional instructions: {extra_instructions if extra_instructions else "None"}

{task}

OUTPUT RULES:
1. Start with: Subject: [clear subject]
2. Then provide only the complete email.
3. Respect the selected language.
4. Match the requested tone, purpose, audience, and length.
5. Preserve user-provided facts.
6. Do not invent names, dates, companies, attachments, promises, or other facts.
7. Do not explain what you changed.
"""


def call_groq(prompt):
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in Streamlit Cloud → Settings → Secrets."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are MailCraft AI. Write polished, natural and useful emails. "
                    "Follow all customization settings exactly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.65,
        max_tokens=1400,
    )

    return response.choices[0].message.content.strip()


# =========================================================
# SESSION STATE
# =========================================================
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

if "last_action" not in st.session_state:
    st.session_state.last_action = ""


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown('<div class="brand">✦ MailCraft AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline">Write better emails, your way.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Workspace")

    action = st.radio(
        "Choose an action",
        ["Generate Email", "Improve Email", "Edit Email"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown("### V2 Features")

    st.markdown(
        '<div class="sidebar-tip"><strong>🎯 Customize</strong><br>'
        '<span>Choose tone, language, purpose, length and audience before generating.</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-tip"><strong>✏️ Edit</strong><br>'
        '<span>Manually edit the generated email and download your final version.</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-tip"><strong>✨ Improve</strong><br>'
        '<span>Turn a rough draft into a clearer, more polished email.</span></div>',
        unsafe_allow_html=True,
    )


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <h1>Write emails your way.</h1>
    <p>Customize the tone, language, purpose and length — then generate, improve or edit.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MAIN LAYOUT
# =========================================================
left, right = st.columns([1, 1], gap="large")


# ---------------- LEFT ----------------
with left:
    st.markdown(
        f'<div class="mode-pill">{html.escape(action)}</div>',
        unsafe_allow_html=True,
    )

    if action == "Generate Email":
        st.markdown(
            '<div class="section-title">Create your email</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-subtitle">Customize the email before AI writes it.</div>',
            unsafe_allow_html=True,
        )

        purpose = st.selectbox(
            "Purpose",
            [
                "Job Application",
                "Internship Application",
                "Leave Request",
                "Meeting Request",
                "Follow-up",
                "Thank You",
                "Complaint",
                "Business Inquiry",
                "Customer Support",
                "Cold Outreach",
                "Apology",
                "Other",
            ],
        )

    else:
        st.markdown(
            f'<div class="section-title">{html.escape(action)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-subtitle">Paste your email and customize how you want it rewritten.</div>',
            unsafe_allow_html=True,
        )

        purpose = st.selectbox(
            "Purpose",
            [
                "Keep the same purpose",
                "Make it more professional",
                "Make it more persuasive",
                "Make it clearer",
                "Make it shorter",
                "Make it more friendly",
                "Make it more formal",
            ],
        )

    # Customization controls
    c1, c2 = st.columns(2)

    with c1:
        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Formal",
                "Friendly",
                "Polite",
                "Casual",
                "Persuasive",
                "Confident",
                "Apologetic",
                "Warm",
            ],
        )

    with c2:
        language = st.selectbox(
            "Language",
            [
                "English",
                "Urdu",
                "Roman Urdu",
                "Arabic",
                "French",
                "Spanish",
                "German",
                "Other",
            ],
        )

    c3, c4 = st.columns(2)

    with c3:
        length = st.selectbox(
            "Length",
            ["Very Short", "Short", "Medium", "Detailed", "Very Detailed"],
            index=2,
        )

    with c4:
        audience = st.selectbox(
            "Audience",
            [
                "Manager / Supervisor",
                "HR / Recruiter",
                "Client / Customer",
                "Teacher / Professor",
                "Colleague",
                "Friend / Personal",
                "Business Partner",
                "General",
            ],
        )

    if action == "Generate Email":
        input_label = "What do you want to say?"
        input_placeholder = (
            "Example: I want to apply for a Python internship. "
            "Mention my AI and Streamlit projects and ask about the next steps."
        )
    elif action == "Improve Email":
        input_label = "Paste your email"
        input_placeholder = "Paste your draft email here..."
    else:
        input_label = "Email to edit"
        input_placeholder = "Paste or write the email you want to edit here..."

    email_text = st.text_area(
        input_label,
        height=205,
        placeholder=input_placeholder,
        key="main_email_input",
    )

    extra_instructions = st.text_area(
        "Additional instructions (optional)",
        height=95,
        placeholder="Example: Keep the greeting, make the request more direct, and sound confident.",
        key="extra_instructions",
    )

    generate_button = st.button(
        "✨ Generate / Apply Changes",
        type="primary",
        use_container_width=True,
    )


# ---------------- RIGHT ----------------
with right:
    st.markdown(
        '<div class="section-title">AI Result</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Review and edit your final email before downloading it.</div>',
        unsafe_allow_html=True,
    )

    if generate_button:
        if not email_text.strip():
            st.warning("Please enter or paste some email content first.")
        else:
            prompt = build_prompt(
                action=action,
                tone=tone,
                language=language,
                purpose=purpose,
                length=length,
                audience=audience,
                extra_instructions=extra_instructions.strip(),
                email_text=email_text.strip(),
            )

            with st.spinner("MailCraft is working on your email..."):
                try:
                    st.session_state.generated_email = call_groq(prompt)
                    st.session_state.last_action = action
                except Exception as e:
                    error = str(e)

                    if "401" in error or "authentication" in error.lower():
                        st.error("Groq authentication failed. Check your GROQ_API_KEY.")
                    elif "model" in error.lower() and "not found" in error.lower():
                        st.error(
                            "The selected Groq model is unavailable. "
                            "Update the model name in app.py."
                        )
                    else:
                        st.error(f"Could not process the email: {error}")

    result = st.session_state.generated_email

    if result:
        st.markdown(
            f'<div class="mode-pill">Editable result • {html.escape(st.session_state.last_action)}</div>',
            unsafe_allow_html=True,
        )

        # The result itself is editable, so the user can make final changes.
        edited_result = st.text_area(
            "Final email",
            value=result,
            height=365,
            label_visibility="collapsed",
            key="editable_result",
        )

        # Keep session state synchronized with manual edits.
        st.session_state.generated_email = edited_result

        b1, b2 = st.columns(2)

        with b1:
            st.download_button(
                "📥 Download .txt",
                data=edited_result,
                file_name="mailcraft_email.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with b2:
            if st.button("↻ Clear result", use_container_width=True):
                st.session_state.generated_email = ""
                st.rerun()

        st.caption(
            "✏️ You can directly edit the email above before downloading it."
        )

    else:
        st.markdown("""
        <div class="empty-result">
            <div>
                <div class="icon">✉️</div>
                <strong>Your customized email will appear here</strong>
                <p>Set your preferences on the left and click<br>
                <b>Generate / Apply Changes</b>.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    '<div class="footer">MailCraft AI V2 • Streamlit + Groq</div>',
    unsafe_allow_html=True,
)
