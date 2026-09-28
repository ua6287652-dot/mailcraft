# ✦ MailCraft AI — V1

MailCraft AI is a Streamlit-based AI email writing assistant powered by Groq.

## V1 Features

- Generate professional emails
- Improve existing emails
- Generate replies
- Email type selection
- Tone selection
- Length selection
- Custom modern Streamlit UI
- Download generated email as `.txt`
- Groq API integration
- Streamlit Cloud ready
- No database required in V1

## Project files

```text
mailcraft-ai-v1/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 1. Get a Groq API key

Create a Groq API key from the Groq Console.

Do not put the API key directly inside `app.py`.

## 2. Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## 3. GitHub

Create a new GitHub repository and upload:

- `app.py`
- `requirements.txt`
- `README.md`
- `.gitignore`

## 4. Streamlit Cloud deployment

1. Open Streamlit Community Cloud.
2. Sign in with GitHub.
3. Click **Create app**.
4. Select your GitHub repository.
5. Select `app.py` as the main file.
6. Deploy.

### Add your Groq API key

After creating the app:

**App settings → Secrets**

Add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Save the secret and reboot/redeploy the app.

## Important

V1 does not use Supabase. Generated emails are not permanently stored.

Supabase can be added in V2 for:

- Login/signup
- User profiles
- Saved emails
- Email history
- Search history
- Dashboard
- Permanent user data

## Groq model

The V1 code uses:

```text
openai/gpt-oss-20b
```

If Groq changes model availability, update the `model=` value in `app.py`.


## V1.1 UI fixes

- Text typed into email text areas is now clearly visible in white.
- Quick Tips text in the dark sidebar is visible.
- The large blank white boxes caused by raw HTML wrappers were fixed.
- The left card now contains the email controls/input.
- The right card now contains the AI result and download action.
- Generated results use a readable editable text area for easy copying.
