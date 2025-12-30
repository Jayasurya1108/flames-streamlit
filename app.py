import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="FLAMES Calculator", page_icon="🔥", layout="centered")

# ---- Google Sheets Setup ----
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
client = gspread.authorize(creds)
sheet = client.open("Flames_Data").worksheet("Sheet1")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #2193b0, #6dd5ed);
    }
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: white;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #e0e0e0;
        margin-bottom: 30px;
    }
    .result {
        background-color: rgba(255,255,255,0.15);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🔥 FLAMES Calculator 🔥</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Discover your relationship 💙</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    n1 = st.text_input("👤 Enter Name 1")
with col2:
    n2 = st.text_input("👤 Enter Name 2")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Calculate FLAMES ✨", use_container_width=True):
    if not n1.strip() or not n2.strip():
        st.warning("⚠️ Please enter both names")
    else:
        a = list(n1.replace(" ", "").lower())
        b = list(n2.replace(" ", "").lower())

        for i in a.copy():
            if i in b:
                a.remove(i)
                b.remove(i)

        n = len(a + b)
        s = "FLAMES"

        while len(s) > 1:
            i = n % len(s) - 1
            if i == -1:
                s = s[:-1]
            else:
                s = s[i+1:] + s[:i]

        d = {
            'F': '🤝 Friends',
            'L': '❤️ Love',
            'A': '💞 Affection',
            'M': '💍 Marriage',
            'E': '⚔️ Enemy',
            'S': '👫 Sister'
        }

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([n1, n2, d[s], time])

        st.markdown(
            f"<div class='result'>💫 Result: {d[s]}</div>",
            unsafe_allow_html=True
        )
