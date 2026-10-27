import sys
import re
from pathlib import Path

frontend_dir = str(Path(__file__).resolve().parent)
if frontend_dir in sys.path:
    sys.path.remove(frontend_dir)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from app.nlp.parser import extract_resume_text
from app.nlp.extractor import extract_resume_information
from app.scoring.resume_score import calculate_resume_score, get_score_category
from app.jobs.repository import JobRepository
from app.jobs.matcher import JobMatcher
from app.reporting.pdf_generator import PDFGenerator

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeAI — Intelligent Career Platform",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.warning("Warning: This Streamlit app is deprecated. Please use the Next.js frontend.")

# ── HELPER: BULLETPROOF HTML RENDERER ──────────────────────────────────────────
def render_html(html_str: str):
    """
    Strips leading whitespace from every line before passing to st.markdown.
    This guarantees Markdown will NEVER misinterpret indented HTML as a <pre><code> block.
    """
    cleaned = "\n".join(line.lstrip() for line in html_str.strip().split("\n"))
    st.markdown(cleaned, unsafe_allow_html=True)

# ── GLOBAL CSS & DARK THEME REFINEMENT ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

/* Deep Space Glass Canvas */
.stApp {
    background: radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 85% 25%, rgba(139, 92, 246, 0.07) 0%, transparent 40%),
                radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.05) 0%, transparent 50%),
                #060813 !important;
    color: #f1f5f9 !important;
}

.block-container {
    max-width: 1180px !important;
    padding: 2rem 2.5rem 6rem !important;
    margin: 0 auto !important;
}

/* Hide Streamlit default clutter */
#MainMenu, footer, header, .stDeployButton {
    display: none !important;
}

/* Align columns evenly with equal height stretching */
div[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
    gap: 1.25rem !important;
}

div[data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
}

div[data-testid="column"] > div {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Glass border wrapper for native st.container(border=True) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.035) !important;
    backdrop-filter: blur(24px) saturate(150%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(150%) !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
    height: 100% !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 1.5rem !important;
}

/* Streamlit File Uploader Glass Theme */
div[data-testid="stFileUploader"] {
    width: 100% !important;
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

div[data-testid="stFileUploader"] section {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 2px dashed rgba(139, 92, 246, 0.35) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    transition: all 0.25s ease-in-out !important;
    min-height: 160px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

div[data-testid="stFileUploader"] section:hover {
    border-color: rgba(167, 139, 250, 0.75) !important;
    background: rgba(139, 92, 246, 0.07) !important;
    box-shadow: 0 0 30px rgba(139, 92, 246, 0.18), inset 0 0 20px rgba(139, 92, 246, 0.04) !important;
}

div[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.25rem !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}

div[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {
    color: #94a3b8 !important;
    font-size: 0.88rem !important;
}

/* Radio Button Controls */
div[data-testid="stRadio"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    padding: 0.5rem 0.9rem !important;
}

div[data-testid="stRadio"] > label {
    display: none !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 1.5rem !important;
}

div[data-testid="stRadio"] label {
    color: #94a3b8 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
    transition: color 0.2s !important;
}

div[data-testid="stRadio"] label:hover {
    color: #c4b5fd !important;
}

/* Slider Controls */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #8b5cf6 !important;
    box-shadow: 0 0 12px rgba(139, 92, 246, 0.7) !important;
}

.stSlider [data-baseweb="slider"] [data-testid="stSliderTrackFill"] {
    background: linear-gradient(90deg, #6366f1, #a855f7) !important;
}

/* Download Button */
.stDownloadButton button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 2rem !important;
    width: 100% !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25) !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35) !important;
    opacity: 0.95 !important;
}

/* Expander Accordion */
div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 14px !important;
    margin-top: 0.75rem !important;
    overflow: hidden !important;
}

div[data-testid="stExpander"] summary {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.25rem !important;
}

div[data-testid="stExpander"] summary:hover {
    color: #c4b5fd !important;
}

div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 1.25rem !important;
    border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Code & Json Blocks */
div[data-testid="stJson"], pre {
    background: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-size: 0.82rem !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.35); border-radius: 100px; }
::-webkit-scrollbar-thumb:hover { background: rgba(139, 92, 246, 0.6); }

/* Dataframe styling */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)


# ── SECTION HEADER COMPONENT ──────────────────────────────────────────────────
def section_header(step_num: str, title: str, subtitle: str = ""):
    sub_html = f'<p style="font-size:0.8rem;color:#475569;margin:3px 0 0;font-weight:400;">{subtitle}</p>' if subtitle else ""
    render_html(f"""
    <div style="display:flex;align-items:center;gap:0.9rem;margin:2.75rem 0 1.35rem;">
        <div style="width:36px;height:36px;border-radius:10px;flex-shrink:0;
            background:linear-gradient(135deg,rgba(99,102,241,0.2),rgba(139,92,246,0.2));
            border:1px solid rgba(139,92,246,0.35);
            display:flex;align-items:center;justify-content:center;">
            <span style="font-size:0.65rem;font-weight:800;color:#a78bfa;letter-spacing:0.5px;">{step_num}</span>
        </div>
        <div>
            <h2 style="font-size:1.08rem;font-weight:700;color:#f1f5f9;margin:0;letter-spacing:-0.2px;line-height:1.3;">{title}</h2>
            {sub_html}
        </div>
    </div>
    """)


# ── TOP BAR & HERO ─────────────────────────────────────────────────────────────
render_html("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem 0 2rem;border-bottom:1px solid rgba(255,255,255,0.06);">
    <div style="display:flex;align-items:center;gap:0.6rem;">
        <div style="width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,#6366f1,#8b5cf6);
            display:flex;align-items:center;justify-content:center;color:#fff;font-size:1rem;font-weight:900;
            box-shadow:0 0 15px rgba(99,102,241,0.5);">✦</div>
        <div style="font-size:1.15rem;font-weight:800;color:#f8fafc;letter-spacing:-0.3px;">Resume<span style="color:#a855f7;">AI</span></div>
    </div>
    <div style="display:flex;align-items:center;gap:0.5rem;background:rgba(16,185,129,0.08);
        border:1px solid rgba(16,185,129,0.25);border-radius:100px;padding:4px 14px;font-size:0.75rem;font-weight:600;color:#6ee7b7;">
        <span style="width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;"></span>
        ML Engine Active · 3-Class Fit Predictor
    </div>
</div>

<div style="text-align:center;padding:3.5rem 1rem 2.75rem;position:relative;">
    <div style="display:inline-flex;align-items:center;gap:6px;background:linear-gradient(90deg,rgba(99,102,241,0.15),rgba(168,85,247,0.15));
        border:1px solid rgba(139,92,246,0.35);border-radius:100px;padding:6px 18px;font-size:0.72rem;font-weight:700;
        letter-spacing:2px;text-transform:uppercase;color:#c4b5fd;margin-bottom:1.25rem;">
        <span>✦</span> NLP & Supervised Machine Learning Pipeline
    </div>
    <h1 style="font-size:3.2rem;font-weight:900;line-height:1.15;margin:0 auto 1.25rem;max-width:850px;
        background:linear-gradient(135deg,#ffffff 0%,#e2e8f0 40%,#c084fc 80%,#818cf8 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-1px;">
        Intelligent Resume Diagnostics & Precision Job Recommendations
    </h1>
    <p style="font-size:1rem;color:#64748b;max-width:540px;margin:0 auto;line-height:1.7;font-weight:400;">
        Upload your resume to extract candidate intelligence, calculate ATS quality scores, 
        and match against live opportunities using our multi-class supervised ML model.
    </p>
</div>
""")


# ── SECTION: UPLOAD & ENGINE CAPABILITIES ─────────────────────────────────────
col_upload, col_features = st.columns([1, 1], gap="medium")

with col_upload:
    with st.container(border=True):
        render_html("""
        <div>
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.25rem;">Step 1</div>
            <div style="font-size:1.15rem;font-weight:800;color:#f8fafc;">Upload Candidate Resume</div>
            <div style="font-size:0.82rem;color:#64748b;margin-top:2px;margin-bottom:0.75rem;">Accepts PDF or Word documents (.pdf, .docx)</div>
        </div>
        """)
        uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"], label_visibility="collapsed")
        render_html("""
        <div style="font-size:0.75rem;color:#475569;text-align:center;margin-top:0.5rem;">
            🔒 Data processed locally in-memory · Never stored externally
        </div>
        """)

with col_features:
    with st.container(border=True):
        features_list = [
            ("✦", "Contact & Skill Entity Extraction", "Detects emails, phone numbers, education credentials, and core technical skills."),
            ("✦", "ATS Quality Scoring (0–100)", "Evaluates 7 structural criteria including section completeness and content balance."),
            ("✦", "Sentence-Transformer NLP", "Computes high-dimensional semantic embeddings between resume and job profiles."),
            ("✦", "3-Class Supervised ML Model", "Predicts Good Fit, Potential Fit, or No Fit with calibrated probabilities."),
            ("✦", "Skill Gap & Coursera Learning Path", "Highlights missing qualifications and provides direct links to upskill.")
        ]
        features_html = "".join([f"""
        <div style="display:flex;align-items:flex-start;gap:0.85rem;padding:0.35rem 0;">
            <div style="width:20px;height:20px;border-radius:6px;background:rgba(99,102,241,0.15);border:1px solid rgba(139,92,246,0.3);
                display:flex;align-items:center;justify-content:center;color:#a855f7;font-size:0.65rem;flex-shrink:0;margin-top:2px;">{icon}</div>
            <div>
                <div style="font-size:0.85rem;font-weight:700;color:#e2e8f0;">{title}</div>
                <div style="font-size:0.76rem;color:#64748b;line-height:1.4;">{desc}</div>
            </div>
        </div>
        """ for icon, title, desc in features_list])

        render_html(f"""
        <div>
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.25rem;">Intelligence Engine</div>
            <div style="font-size:1.15rem;font-weight:800;color:#f8fafc;margin-bottom:0.85rem;">Analysis Pipeline</div>
            <div style="display:flex;flex-direction:column;gap:0.25rem;">
                {features_html}
            </div>
        </div>
        """)


# ── MAIN ANALYSIS FLOW ────────────────────────────────────────────────────────
if uploaded_file:
    try:
        with st.spinner("Extracting text and running NLP analysis..."):
            text = extract_resume_text(uploaded_file)
            information = extract_resume_information(text)
            score, breakdown = calculate_resume_score(information, text)
            category = get_score_category(score)

        render_html(f"""
        <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);
            border-radius:14px;padding:0.85rem 1.25rem;font-size:0.88rem;color:#6ee7b7;
            margin:1.75rem 0 0.5rem;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:0.6rem;">
                <span style="font-size:1.1rem;">✓</span>
                <span><b>Resume processed successfully:</b> <code>{uploaded_file.name}</code> ({len(text.split())} words parsed)</span>
            </div>
            <span style="font-size:0.75rem;background:rgba(16,185,129,0.2);padding:3px 10px;border-radius:100px;font-weight:700;">READY FOR MATCHING</span>
        </div>
        """)

        # ── 1. ATS RESUME ANALYSIS ────────────────────────────────────────────
        section_header("01", "ATS Resume Compatibility & Diagnostics", "Structural evaluation against automated applicant tracking systems")

        col_score, col_breakdown = st.columns([1, 2], gap="medium")

        # Color token selection based on score
        if score >= 75:
            sc_color, sc_glow, sc_badge_bg, sc_badge_txt = "#10b981", "rgba(16,185,129,0.3)", "rgba(16,185,129,0.15)", "#34d399"
            sc_status = "Excellent Structure · ATS Ready"
        elif score >= 55:
            sc_color, sc_glow, sc_badge_bg, sc_badge_txt = "#6366f1", "rgba(99,102,241,0.3)", "rgba(99,102,241,0.15)", "#818cf8"
            sc_status = "Good Potential · Minor Gaps"
        elif score >= 40:
            sc_color, sc_glow, sc_badge_bg, sc_badge_txt = "#f59e0b", "rgba(245,158,11,0.3)", "rgba(245,158,11,0.15)", "#fbbf24"
            sc_status = "Average · Needs Optimization"
        else:
            sc_color, sc_glow, sc_badge_bg, sc_badge_txt = "#ef4444", "rgba(239,68,68,0.3)", "rgba(239,68,68,0.15)", "#f87171"
            sc_status = "Critical Sections Missing"

        with col_score:
            skills_count = len(information.get("skills", []))
            word_count = len(text.split())
            render_html(f"""
            <div style="background:rgba(255,255,255,0.03);backdrop-filter:blur(24px) saturate(150%);
                border:1px solid rgba(255,255,255,0.09);border-radius:20px;padding:2rem 1.5rem;
                height:100%;display:flex;flex-direction:column;justify-content:space-between;text-align:center;
                box-shadow:0 4px 24px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.06);">
                <div>
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.5rem;">Overall ATS Score</div>
                    <div style="font-size:4.5rem;font-weight:900;line-height:1;margin:0.5rem 0 0.25rem;
                        background:linear-gradient(135deg,#ffffff,{sc_color});
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{score}</div>
                    <div style="font-size:0.8rem;color:#64748b;font-weight:600;">out of 100 possible points</div>
                    
                    <div style="display:inline-block;margin:1rem 0;padding:6px 16px;border-radius:100px;
                        font-size:0.82rem;font-weight:700;background:{sc_badge_bg};color:{sc_badge_txt};
                        border:1px solid {sc_color}40;">{category}</div>
                    
                    <div style="height:6px;background:rgba(255,255,255,0.08);border-radius:100px;overflow:hidden;margin:0.75rem 1rem 1.25rem;">
                        <div style="height:100%;width:{score}%;background:linear-gradient(90deg,{sc_color}99,{sc_color});border-radius:100px;"></div>
                    </div>
                    <div style="font-size:0.8rem;color:#94a3b8;">{sc_status}</div>
                </div>

                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin-top:1.5rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,0.06);">
                    <div style="background:rgba(255,255,255,0.02);padding:0.6rem;border-radius:10px;border:1px solid rgba(255,255,255,0.05);">
                        <div style="font-size:1.15rem;font-weight:800;color:#f8fafc;">{skills_count}</div>
                        <div style="font-size:0.68rem;color:#64748b;font-weight:600;text-transform:uppercase;">Skills Found</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:0.6rem;border-radius:10px;border:1px solid rgba(255,255,255,0.05);">
                        <div style="font-size:1.15rem;font-weight:800;color:#f8fafc;">{word_count}</div>
                        <div style="font-size:0.68rem;color:#64748b;font-weight:600;text-transform:uppercase;">Word Count</div>
                    </div>
                </div>
            </div>
            """)

        with col_breakdown:
            max_points = {
                "Contact Information": 10,
                "Skills": 25,
                "Education": 15,
                "Experience": 20,
                "Projects": 15,
                "Certifications": 10,
                "Resume Content": 5
            }
            breakdown_rows = ""
            for comp, pts in breakdown.items():
                total = max_points.get(comp, 10)
                pct = int((pts / total) * 100) if total else 0
                bar_color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"
                breakdown_rows += f"""
                <div style="margin-bottom:0.9rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                        <span style="font-size:0.85rem;color:#cbd5e1;font-weight:600;">{comp}</span>
                        <span style="font-size:0.82rem;font-weight:700;color:#f8fafc;">{pts} <span style="color:#64748b;font-weight:400;">/ {total} pts</span></span>
                    </div>
                    <div style="height:6px;background:rgba(255,255,255,0.07);border-radius:100px;overflow:hidden;">
                        <div style="height:100%;width:{pct}%;background:{bar_color};border-radius:100px;transition:width 0.5s ease;"></div>
                    </div>
                </div>
                """

            render_html(f"""
            <div style="background:rgba(255,255,255,0.03);backdrop-filter:blur(24px) saturate(150%);
                border:1px solid rgba(255,255,255,0.09);border-radius:20px;padding:1.75rem 2rem;
                height:100%;display:flex;flex-direction:column;justify-content:space-between;
                box-shadow:0 4px 24px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.06);">
                <div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem;">
                        <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;">Structural Scoring</div>
                        <div style="font-size:0.75rem;color:#64748b;">7 Evaluation Criteria</div>
                    </div>
                    {breakdown_rows}
                </div>
            </div>
            """)

        # ── 2. EXTRACTED CANDIDATE PROFILE ─────────────────────────────────────
        section_header("02", "Extracted Candidate Profile", "Information parsed by entity recognition and rule-based NLP extractors")

        col_p1, col_p2 = st.columns(2, gap="medium")

        with col_p1:
            email = information.get("email") or "Not detected"
            phone = information.get("phone") or "Not detected"
            render_html(f"""
            <div style="background:rgba(255,255,255,0.03);backdrop-filter:blur(24px) saturate(150%);
                border:1px solid rgba(255,255,255,0.09);border-radius:18px;padding:1.5rem;min-height:175px;
                display:flex;flex-direction:column;justify-content:space-between;
                box-shadow:0 4px 20px rgba(0,0,0,0.35),inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.75rem;">Contact Information</div>
                <div style="display:flex;flex-direction:column;gap:0.75rem;">
                    <div style="display:flex;align-items:center;gap:0.75rem;">
                        <div style="width:28px;height:28px;border-radius:8px;background:rgba(99,102,241,0.15);border:1px solid rgba(139,92,246,0.3);
                            display:flex;align-items:center;justify-content:center;color:#a855f7;font-size:0.8rem;">✉</div>
                        <div>
                            <div style="font-size:0.68rem;color:#64748b;text-transform:uppercase;font-weight:700;">Email</div>
                            <div style="font-size:0.92rem;color:#f1f5f9;font-weight:600;">{email}</div>
                        </div>
                    </div>
                    <div style="display:flex;align-items:center;gap:0.75rem;">
                        <div style="width:28px;height:28px;border-radius:8px;background:rgba(99,102,241,0.15);border:1px solid rgba(139,92,246,0.3);
                            display:flex;align-items:center;justify-content:center;color:#a855f7;font-size:0.8rem;">📞</div>
                        <div>
                            <div style="font-size:0.68rem;color:#64748b;text-transform:uppercase;font-weight:700;">Phone Number</div>
                            <div style="font-size:0.92rem;color:#f1f5f9;font-weight:600;">{phone}</div>
                        </div>
                    </div>
                </div>
            </div>
            """)

        with col_p2:
            skills = information.get("skills", [])
            if skills:
                skill_badges = "".join([f"""
                <span style="display:inline-block;background:rgba(139,92,246,0.12);border:1px solid rgba(139,92,246,0.3);
                    border-radius:100px;padding:3px 12px;margin:2px 3px;font-size:0.78rem;font-weight:600;color:#c4b5fd;">
                    {s}
                </span>""" for s in skills])
            else:
                skill_badges = '<span style="color:#64748b;font-size:0.85rem;">No technical skills detected.</span>'

            render_html(f"""
            <div style="background:rgba(255,255,255,0.03);backdrop-filter:blur(24px) saturate(150%);
                border:1px solid rgba(255,255,255,0.09);border-radius:18px;padding:1.5rem;min-height:175px;
                display:flex;flex-direction:column;justify-content:space-between;
                box-shadow:0 4px 20px rgba(0,0,0,0.35),inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                    <div style="font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;">Extracted Skills</div>
                    <span style="font-size:0.72rem;color:#a855f7;font-weight:700;">{len(skills)} Identified</span>
                </div>
                <div style="line-height:1.9;max-height:115px;overflow-y:auto;">
                    {skill_badges}
                </div>
            </div>
            """)

        col_p3, col_p4 = st.columns(2, gap="medium")

        with col_p3:
            edu = (information.get("education") or "No explicit education section found.")[:320]
            render_html(f"""
            <div style="background:rgba(255,255,255,0.03);backdrop-filter:blur(24px) saturate(150%);
                border:1px solid rgba(255,255,255,0.09);border-radius:18px;padding:1.5rem;min-height:150px;
                box-shadow:0 4px 20px rgba(0,0,0,0.35),inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.65rem;">Education Profile</div>
                <div style="font-size:0.85rem;color:#cbd5e1;line-height:1.65;">{edu}</div>
            </div>
            """)

        with col_p4:
            exp = (information.get("experience") or "No explicit experience section found.")[:320]
            render_html(f"""
            <div style="background:rgba(255,255,255,0.03);backdrop-filter:blur(24px) saturate(150%);
                border:1px solid rgba(255,255,255,0.09);border-radius:18px;padding:1.5rem;min-height:150px;
                box-shadow:0 4px 20px rgba(0,0,0,0.35),inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.65rem;">Experience Profile</div>
                <div style="font-size:0.85rem;color:#cbd5e1;line-height:1.65;">{exp}</div>
            </div>
            """)

        with st.expander("🔍 View Raw Parsed Resume Text"):
            st.text(text)

        # ── 3. SUPERVISED ML JOB MATCHING ─────────────────────────────────────
        section_header("03", "AI Job Matching & Multi-Class ML Ranking", "Matching candidate profile against job dataset using supervised ML predictions")

        with st.container(border=True):
            render_html("""
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.75rem;">Match Configuration</div>
            """)
            col_ctrl1, col_ctrl2 = st.columns([1, 1], gap="large")
            with col_ctrl1:
                job_pref = st.radio("Target Job Market", ["🌍 Remote (Global via Remotive)", "🏢 In-Office (India API)"], horizontal=True)
            with col_ctrl2:
                n_show_target = st.slider("Positions to display", min_value=1, max_value=15, value=5)

        all_jobs = []
        if "Remote" in job_pref:
            with st.spinner("Fetching live remote positions from Remotive API..."):
                from app.jobs.api_client import RemotiveClient
                live_jobs = RemotiveClient().fetch_jobs(limit=15)
            if live_jobs:
                render_html(f"""
                <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.1);
                    border:1px solid rgba(16,185,129,0.25);border-radius:100px;padding:4px 14px;font-size:0.78rem;color:#6ee7b7;margin:1rem 0 1.25rem;">
                    ✓ &nbsp;<b>{len(live_jobs)} live remote openings</b> fetched and synchronized
                </div>
                """)
                all_jobs = live_jobs
            else:
                st.warning("Live remote API unavailable — falling back to local job dataset.")
                repo = JobRepository()
                repo.load_jobs()
                all_jobs = repo.get_all_jobs()
        else:
            with st.spinner("Connecting to IndianAPI job feed..."):
                from app.jobs.api_client import IndianApiClient
                try:
                    from dotenv import load_dotenv
                    load_dotenv()
                    live_jobs = IndianApiClient().fetch_jobs(limit=15)
                    if live_jobs:
                        render_html(f"""
                        <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.1);
                            border:1px solid rgba(16,185,129,0.25);border-radius:100px;padding:4px 14px;font-size:0.78rem;color:#6ee7b7;margin:1rem 0 1.25rem;">
                            ✓ &nbsp;<b>{len(live_jobs)} verified Indian positions</b> fetched
                        </div>
                        """)
                        all_jobs = live_jobs
                    else:
                        st.error("Failed to fetch jobs from IndianAPI. Using local fallback.")
                        repo = JobRepository()
                        repo.load_jobs()
                        all_jobs = repo.get_all_jobs()
                except Exception as e:
                    st.error(f"API Error: {e}. Using local fallback.")
                    repo = JobRepository()
                    repo.load_jobs()
                    all_jobs = repo.get_all_jobs()

        if all_jobs:
            with st.spinner("Calculating semantic embeddings, feature vectors, and ML predictions..."):
                matcher = JobMatcher()
                ml_ranked_jobs = matcher.rank_jobs_with_ml(text, information, score, all_jobs)

            n_show = min(n_show_target, len(ml_ranked_jobs))

            # Ranking explanation banner
            render_html(f"""
            <div style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.2);
                border-radius:12px;padding:0.75rem 1.25rem;font-size:0.82rem;color:#cbd5e1;margin-bottom:1.75rem;
                display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
                <div style="display:flex;align-items:center;gap:0.6rem;">
                    <span style="color:#a855f7;font-size:1rem;">✦</span>
                    <span>Ranking Criterion: <code style="color:#c4b5fd;background:rgba(139,92,246,0.15);padding:2px 8px;border-radius:6px;">Score = P(Good Fit) + 0.5 × P(Potential Fit)</code></span>
                </div>
                <div style="color:#64748b;font-weight:600;">{len(ml_ranked_jobs)} Candidates Evaluated · Showing Top {n_show}</div>
            </div>
            """)

            # ── JOB CARDS ─────────────────────────────────────────────────────
            for i, job in enumerate(ml_ranked_jobs[:n_show]):
                prediction = job.get("ml_prediction", "Unknown")
                probs = job.get("ml_probabilities", {})
                ranking_score = round(job.get("ranking_score", 0.0) * 100, 1)

                p_good = round(probs.get("Good Fit", 0.0) * 100, 1)
                p_potential = round(probs.get("Potential Fit", 0.0) * 100, 1)
                p_no = round(probs.get("No Fit", 0.0) * 100, 1)

                # Prediction Colors & Badges
                if prediction == "Good Fit":
                    card_accent = "#10b981"
                    badge_bg = "rgba(16,185,129,0.15)"
                    badge_border = "rgba(16,185,129,0.35)"
                    badge_color = "#34d399"
                    badge_dot = "#10b981"
                elif prediction == "Potential Fit":
                    card_accent = "#f59e0b"
                    badge_bg = "rgba(245,158,11,0.15)"
                    badge_border = "rgba(245,158,11,0.35)"
                    badge_color = "#fbbf24"
                    badge_dot = "#f59e0b"
                else:
                    card_accent = "#ef4444"
                    badge_bg = "rgba(239,68,68,0.15)"
                    badge_border = "rgba(239,68,68,0.35)"
                    badge_color = "#f87171"
                    badge_dot = "#ef4444"

                # Skills Comparison
                delim = ';' if ';' in job.get('required_skills', '') else ','
                job_skills = [s.strip().lower() for s in job.get('required_skills', '').split(delim) if s.strip()]
                user_skills = [s.lower() for s in information.get("skills", [])]
                matched_skills = [s for s in job_skills if s in user_skills]
                missing_skills = [s for s in job_skills if s not in user_skills]

                sem_score = round(job["feature_dict"]["semantic_similarity"] * 100, 1)
                tfidf_score = round(job["feature_dict"]["tfidf_similarity"] * 100, 1)
                skill_ratio = round(job["feature_dict"]["skill_match_ratio"] * 100, 1)
                
                # Meaningful explanation
                raw_expl = job.get("explanation", "")
                if raw_expl and raw_expl.strip():
                    explanation = raw_expl.strip()
                else:
                    if prediction == "Good Fit":
                        explanation = f"High alignment across candidate profile with {sem_score}% semantic relevance and {skill_ratio}% skill coverage."
                    elif prediction == "Potential Fit":
                        explanation = f"Moderate match with {sem_score}% semantic relevance. Candidate shows strong potential with targeted skill upskilling."
                    else:
                        explanation = f"Low correlation with role requirements ({sem_score}% semantic match). Essential skill prerequisites are missing."

                # Matched & Missing Badges
                matched_html = "".join([f'<span style="display:inline-block;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);border-radius:100px;padding:3px 10px;margin:2px 3px;font-size:0.75rem;font-weight:600;color:#6ee7b7;">✓ {s.title()}</span>' for s in matched_skills]) or '<span style="color:#64748b;font-size:0.8rem;">None detected</span>'
                missing_html = "".join([f'<span style="display:inline-block;background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);border-radius:100px;padding:3px 10px;margin:2px 3px;font-size:0.75rem;font-weight:600;color:#fca5a5;">✕ {s.title()}</span>' for s in missing_skills]) or '<span style="color:#6ee7b7;font-size:0.8rem;">No skill gaps</span>'

                coursera_html = ""
                if missing_skills:
                    c_links = [f'<a href="https://www.coursera.org/search?query={s.replace(" ", "%20")}" target="_blank" style="color:#a855f7;text-decoration:none;font-weight:600;">{s.title()}</a>' for s in missing_skills[:4]]
                    coursera_html = f"""
                    <div style="font-size:0.76rem;color:#64748b;margin-top:0.5rem;">
                        📚 Recommended Courses: {", ".join(c_links)}
                    </div>
                    """

                # Render entire unified card
                render_html(f"""
                <div style="background:rgba(255,255,255,0.03);backdrop-filter:blur(24px);
                    border:1px solid rgba(255,255,255,0.08);border-top:3px solid {card_accent};
                    border-radius:20px;padding:1.75rem 2rem;margin-bottom:1.5rem;
                    box-shadow:0 8px 30px rgba(0,0,0,0.35);">
                    
                    <!-- Card Header -->
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
                        <div style="flex:1;min-width:240px;">
                            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                                <span style="background:rgba(139,92,246,0.18);color:#c4b5fd;font-size:0.7rem;font-weight:800;letter-spacing:1.5px;padding:2px 8px;border-radius:6px;">MATCH #{i+1}</span>
                                <span style="color:#64748b;font-size:0.8rem;">·</span>
                                <span style="color:#94a3b8;font-size:0.85rem;font-weight:500;">{job.get('company','Unknown Company')}</span>
                            </div>
                            <div style="font-size:1.35rem;font-weight:800;color:#f8fafc;line-height:1.25;margin-bottom:0.35rem;">{job.get('job_title','Position')}</div>
                            <div style="font-size:0.82rem;color:#64748b;display:flex;align-items:center;gap:0.4rem;">
                                <span>📍</span> {job.get('location','Remote / Global')}
                            </div>
                        </div>

                        <div style="display:flex;align-items:center;gap:1.5rem;flex-shrink:0;">
                            <div style="text-align:right;">
                                <div style="font-size:0.68rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#8b5cf6;">Match Score</div>
                                <div style="font-size:2.4rem;font-weight:900;color:#f8fafc;line-height:1;">{ranking_score}<span style="font-size:1.1rem;color:#64748b;font-weight:500;">%</span></div>
                            </div>
                            <div style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;
                                border-radius:100px;font-size:0.82rem;font-weight:700;
                                background:{badge_bg};color:{badge_color};border:1px solid {badge_border};">
                                <span style="width:7px;height:7px;border-radius:50%;background:{badge_dot};box-shadow:0 0 8px {badge_dot};"></span>
                                {prediction}
                            </div>
                        </div>
                    </div>

                    <!-- Inner Grid: Probabilities & Signal Tiles -->
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.25rem;">
                        <!-- Left: Class Probabilities -->
                        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:1.15rem 1.25rem;">
                            <div style="font-size:0.68rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.85rem;">ML Model Fit Probabilities</div>
                            
                            <div style="margin-bottom:0.6rem;">
                                <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:3px;">
                                    <span style="color:#94a3b8;font-weight:600;">Good Fit</span>
                                    <span style="color:#6ee7b7;font-weight:700;">{p_good}%</span>
                                </div>
                                <div style="height:5px;background:rgba(255,255,255,0.06);border-radius:100px;overflow:hidden;">
                                    <div style="height:100%;width:{p_good}%;background:linear-gradient(90deg,#059669,#10b981);border-radius:100px;"></div>
                                </div>
                            </div>

                            <div style="margin-bottom:0.6rem;">
                                <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:3px;">
                                    <span style="color:#94a3b8;font-weight:600;">Potential Fit</span>
                                    <span style="color:#fbbf24;font-weight:700;">{p_potential}%</span>
                                </div>
                                <div style="height:5px;background:rgba(255,255,255,0.06);border-radius:100px;overflow:hidden;">
                                    <div style="height:100%;width:{p_potential}%;background:linear-gradient(90deg,#d97706,#f59e0b);border-radius:100px;"></div>
                                </div>
                            </div>

                            <div>
                                <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:3px;">
                                    <span style="color:#94a3b8;font-weight:600;">No Fit</span>
                                    <span style="color:#f87171;font-weight:700;">{p_no}%</span>
                                </div>
                                <div style="height:5px;background:rgba(255,255,255,0.06);border-radius:100px;overflow:hidden;">
                                    <div style="height:100%;width:{p_no}%;background:linear-gradient(90deg,#dc2626,#ef4444);border-radius:100px;"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Right: NLP Signal Tiles -->
                        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:1.15rem 1.25rem;display:flex;flex-direction:column;justify-content:space-between;">
                            <div style="font-size:0.68rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#8b5cf6;margin-bottom:0.5rem;">Core NLP Signals</div>
                            
                            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.5rem;align-items:center;">
                                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:0.75rem 0.25rem;text-align:center;">
                                    <div style="font-size:1.25rem;font-weight:800;color:#f8fafc;">{sem_score}%</div>
                                    <div style="font-size:0.65rem;font-weight:700;color:#8b5cf6;text-transform:uppercase;margin-top:2px;">Semantic</div>
                                </div>

                                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:0.75rem 0.25rem;text-align:center;">
                                    <div style="font-size:1.25rem;font-weight:800;color:#f8fafc;">{tfidf_score}%</div>
                                    <div style="font-size:0.65rem;font-weight:700;color:#8b5cf6;text-transform:uppercase;margin-top:2px;">TF-IDF</div>
                                </div>

                                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:0.75rem 0.25rem;text-align:center;">
                                    <div style="font-size:1.25rem;font-weight:800;color:#f8fafc;">{skill_ratio}%</div>
                                    <div style="font-size:0.65rem;font-weight:700;color:#8b5cf6;text-transform:uppercase;margin-top:2px;">Skill Ratio</div>
                                </div>
                            </div>

                            <div style="font-size:0.74rem;color:#64748b;line-height:1.3;margin-top:0.5rem;">
                                Features extracted from SBERT dense embeddings & TF-IDF n-grams.
                            </div>
                        </div>
                    </div>

                    <!-- AI Explanation -->
                    <div style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.18);
                        border-radius:12px;padding:0.85rem 1.15rem;font-size:0.82rem;color:#c7d2fe;line-height:1.6;margin-bottom:1rem;">
                        🤖 &nbsp;<b>Model Rationale:</b> {explanation}
                    </div>

                    <!-- Skills 2-col Grid -->
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:0.85rem 1rem;">
                            <div style="font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#10b981;margin-bottom:6px;">Matched</div>
                            <div>{matched_html}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:0.85rem 1rem;">
                            <div style="font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#ef4444;margin-bottom:6px;">Missing</div>
                            <div>{missing_html}</div>
                            {coursera_html}
                        </div>
                    </div>
                </div>
                """)

                with st.expander(f"⚙ Technical Details & Feature Vector — #{i+1} {job.get('job_title','')}"):
                    st.json(job["feature_dict"])

            # ── 4. EXPORT REPORT ──────────────────────────────────────────────
            section_header("04", "Export Intelligence Report", "Download full candidate evaluation as a professional PDF summary")

            pdf_bytes = PDFGenerator().generate_report(information, score, ml_ranked_jobs)
            st.download_button(
                "📥 Download Candidate Career Intelligence Report (PDF)",
                pdf_bytes,
                "ResumeAI_Intelligence_Report.pdf",
                "application/pdf"
            )

        else:
            render_html("""
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
                border-radius:16px;padding:2.5rem;text-align:center;color:#64748b;">
                No matching opportunities found for the selected criteria.
            </div>
            """)

    except Exception as e:
        render_html(f"""
        <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);
            border-radius:14px;padding:1.25rem 1.5rem;color:#fca5a5;margin:1.5rem 0;">
            <div style="font-weight:700;font-size:0.95rem;margin-bottom:0.25rem;">✕ Error processing resume</div>
            <div style="font-size:0.85rem;color:#fecaca;">{str(e)}</div>
        </div>
        """)
        import traceback
        with st.expander("View Diagnostic Traceback"):
            st.code(traceback.format_exc())


# ── 5. ALL AVAILABLE POSITIONS (LOCAL REPOSITORY) ─────────────────────────────
section_header("05", "Local Benchmark Job Repository", "Curated baseline roles used for model validation and local indexing")

try:
    repo = JobRepository()
    repo.load_jobs()
    bench_jobs = repo.get_all_jobs()
    if bench_jobs:
        df_jobs = pd.DataFrame(bench_jobs)[["job_id", "job_title", "company", "location", "required_skills"]]
        df_jobs.columns = ["ID", "Title", "Company", "Location", "Required Skills"]
        st.dataframe(df_jobs, use_container_width=True, hide_index=True)
    else:
        render_html('<div style="color:#64748b;font-size:0.85rem;">No local jobs indexed.</div>')
except Exception as e:
    st.error(f"Error loading job repository: {e}")