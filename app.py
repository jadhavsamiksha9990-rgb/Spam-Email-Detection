import streamlit as st
import tempfile
import os
import time
from src.pipeline.prediction_pipeline import PredictionPipeline

# Page configuration
st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #0b1220;
            --panel: rgba(15, 23, 42, 0.85);
            --panel-strong: #111827;
            --primary: #38bdf8;
            --primary-soft: rgba(56, 189, 248, 0.18);
            --success: #34d399;
            --danger: #f87171;
            --warning: #fbbf24;
            --text: #e5eefb;
            --muted: #9fb3c8;
            --border: rgba(148, 163, 184, 0.2);
        }

        .stApp {
            background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 28%),
                        radial-gradient(circle at bottom right, rgba(52, 211, 153, 0.12), transparent 28%),
                        var(--bg);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(15, 23, 42, 0.9));
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1.5rem 1.6rem;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.25);
            margin-bottom: 1.25rem;
        }

        .hero-badge {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: var(--primary-soft);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: var(--primary);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }

        h1 {
            color: var(--text) !important;
            margin: 0 !important;
            font-size: 2.5rem !important;
            line-height: 1.1 !important;
        }

        .hero p {
            color: var(--muted) !important;
            font-size: 1rem !important;
            margin-top: 0.6rem !important;
            margin-bottom: 0 !important;
        }

        .stat-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 0.9rem 1rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.2);
            height: 100%;
        }

        .stat-label {
            color: var(--muted);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .stat-value {
            color: var(--text);
            font-size: 1.55rem;
            font-weight: 700;
            margin-top: 0.4rem;
        }

        .panel {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.15rem 1.1rem 1.25rem;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.6rem;
        }

        .subtle {
            color: var(--muted);
            font-size: 0.9rem;
        }

        .result-box {
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-top: 1rem;
            border: 1px solid var(--border);
            font-size: 1.05rem;
            font-weight: 600;
        }

        .result-box.spam {
            background: rgba(248, 113, 113, 0.12);
            border-color: rgba(248, 113, 113, 0.35);
            color: #fecaca;
        }

        .result-box.ham {
            background: rgba(52, 211, 153, 0.12);
            border-color: rgba(52, 211, 153, 0.35);
            color: #bbf7d0;
        }

        .confidence-pill {
            display: inline-block;
            margin-top: 0.8rem;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(56, 189, 248, 0.28);
            color: var(--primary);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .stButton > button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            padding: 0.75rem 1.15rem !important;
            border: none !important;
            background: linear-gradient(135deg, var(--primary), #2563eb) !important;
            color: white !important;
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25) !important;
        }

        .stButton > button:hover {
            filter: brightness(1.05);
        }

        .stFileUploader > div {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border);
            border-radius: 16px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
        }

        .stTextArea textarea {
            background: rgba(15, 23, 42, 0.7);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize pipeline
@st.cache_resource
def get_pipeline():
    return PredictionPipeline(load_models=True)

try:
    pipeline = get_pipeline()
except Exception as e:
    st.error(f"Error loading models: {str(e)}")
    st.stop()

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI Security</div>
        <h1>Spam Email Classifier</h1>
        <p>Classify incoming emails as spam or legitimate mail using a trained machine learning pipeline.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">Mode</div>
            <div class="stat-value">Live</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">Focus</div>
            <div class="stat-value">Spam / Ham</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">Support</div>
            <div class="stat-value">MBOX</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Tabs for different modes
tab1, tab2 = st.tabs(["Single Email", "Batch MBOX Processing"])

with tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Check a Single Email</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Paste any message and get a quick spam prediction.</div>', unsafe_allow_html=True)
    email_text = st.text_area(
        "Paste the email content here:",
        height=220,
        placeholder="Dear friend, I have a business proposal...",
        label_visibility="collapsed",
    )

    if st.button("Classify Email", type="primary"):
        if email_text.strip():
            with st.spinner("Analyzing message..."):
                try:
                    result = pipeline.predict_single_email(email_text)
                    prediction = result['prediction']
                    confidence = result.get('confidence', 0)

                    result_class = "spam" if prediction == "Spam" else "ham"
                    result_icon = "🚨" if prediction == "Spam" else "✅"
                    result_text = "This email is SPAM" if prediction == "Spam" else "This email is HAM (Safe)"

                    st.markdown(
                        f'<div class="result-box {result_class}">{result_icon} {result_text}</div>',
                        unsafe_allow_html=True,
                    )

                    if confidence:
                        st.markdown(f'<div class="confidence-pill">Confidence: {confidence:.1f}%</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error analyzing email: {str(e)}")
        else:
            st.warning("Please enter some text to classify.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Process MBOX File</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Upload an mbox archive to scan multiple emails in one pass.</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an MBOX file", type=['mbox', 'txt'])

    if uploaded_file is not None:
        if st.button("Process File"):
            with st.spinner("Processing file... this may take a moment"):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mbox') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    try:
                        df = pipeline.predict_mbox_file(tmp_path)
                        spam_count = len(df[df['Prediction'] == 'Spam'])
                        ham_count = len(df[df['Prediction'] == 'Ham'])

                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("Total Emails", len(df))
                        col_b.metric("Spam Found", spam_count, delta_color="inverse")
                        col_c.metric("Ham Found", ham_count)

                        st.subheader("Results Preview")
                        st.dataframe(df[['Time', 'Subject', 'Prediction']].head(10), use_container_width=True)

                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Full Results (CSV)",
                            data=csv,
                            file_name=f"predictions_{int(time.time())}.csv",
                            mime="text/csv",
                        )
                    finally:
                        if os.path.exists(tmp_path):
                            try:
                                os.unlink(tmp_path)
                            except:
                                pass
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)
