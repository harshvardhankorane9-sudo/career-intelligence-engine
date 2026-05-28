"""
Career Intelligence Engine — Streamlit Frontend v3.3
Run: streamlit run app.py  (backend must be running: python main.py)
"""

import os
import streamlit as st
import requests
from datetime import datetime
from pdf_report import generate_report_pdf

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────

# Cloud deployment: set API_URL env var on Render to your backend URL
# Local dev: defaults to localhost
API = os.getenv("API_URL", "http://localhost:8000/api/v1").rstrip("/")

st.set_page_config(
    page_title="Career Intelligence Engine",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def api_get(path: str, params: dict = None):
    try:
        r = requests.get(f"{API}/{path}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Backend not running. Start it with: `python main.py`")
        return {}
    except Exception as e:
        st.error(f"API error ({path}): {e}")
        return {}

def api_post(path: str, data: dict = None, params: dict = None):
    try:
        r = requests.post(f"{API}/{path}", json=data or {}, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Backend not running. Start it with: `python main.py`")
        return {}
    except Exception as e:
        st.error(f"API error ({path}): {e}")
        return {}

def hex_rgba(hex_color: str, alpha: float = 0.08) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

BRANCH_COLOR = {
    "CSE": "#4f46e5", "CSE-AIML": "#7c3aed",
    "MECH": "#d97706", "ECE": "#0891b2",
    "CIVIL": "#059669", "CHEM": "#dc2626",
    "BME": "#db2777", "AERO": "#6d28d9",
}
BRANCH_EMOJI = {
    "CSE": "💻", "CSE-AIML": "🤖", "MECH": "⚙️", "ECE": "🔌",
    "CIVIL": "🏗️", "CHEM": "⚗️", "BME": "🏥", "AERO": "🚀",
}
BRANCH_NAMES = {
    "CSE": "Computer Science & Engineering",
    "CSE-AIML": "CSE with AI & Machine Learning",
    "MECH": "Mechanical Engineering",
    "ECE": "Electronics & Communication Engineering",
    "CIVIL": "Civil Engineering",
    "CHEM": "Chemical Engineering",
    "BME": "Biomedical Engineering",
    "AERO": "Aerospace Engineering",
}
BRANCH_OPTIONS = {
    "💻  Computer Science & Engineering": "CSE",
    "🤖  CSE with AI & Machine Learning": "CSE-AIML",
    "⚙️  Mechanical Engineering":          "MECH",
    "🔌  Electronics & Communication":     "ECE",
    "🏗️  Civil Engineering":               "CIVIL",
    "⚗️  Chemical Engineering":            "CHEM",
    "🏥  Biomedical Engineering":           "BME",
    "🚀  Aerospace Engineering":            "AERO",
}

def branch_select(label="Select branch:", key="bs"):
    sel = st.selectbox(label, list(BRANCH_OPTIONS.keys()), key=key)
    return BRANCH_OPTIONS[sel]

# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────

DEFAULTS = {
    "student_id": None, "student_name": "", "student_email": "",
    "asmt_questions": [], "asmt_q_index": 0,
    "asmt_answers": {}, "asmt_results": None,
    "sim_phase": "select",
    "sim_branch_code": None, "sim_branch_name": None,
    "sim_intro": None, "sim_scenario": None,
    "sim_decisions": [], "sim_feedback": None,
    "sim_finished": False, "sim_final": None,
    "chat_session_id": None, "chat_messages": [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🎓 Career Intelligence")
    st.caption("8-branch engineering counsellor — Pune & Maharashtra")
    st.divider()

    if not st.session_state.student_id:
        st.subheader("👤 Get Started")
        name    = st.text_input("Your name",          key="reg_name")
        email   = st.text_input("Email address",      key="reg_email")
        college = st.text_input("College (optional)", key="reg_college")
        year    = st.selectbox("Current year", [1, 2, 3, 4], key="reg_year")
        if st.button("Continue →", type="primary", use_container_width=True):
            if name and email:
                resp = api_post("students/register", {
                    "name": name, "email": email,
                    "college": college, "branch_year": year
                })
                if resp and "student" in resp:
                    s = resp["student"]
                    st.session_state.student_id   = s["id"]
                    st.session_state.student_name  = s["name"]
                    st.session_state.student_email = s["email"]
                    st.rerun()
            else:
                st.warning("Please fill in name and email.")
    else:
        st.subheader(f"👤 {st.session_state.student_name}")
        st.caption(st.session_state.student_email)
        dash = api_get(f"students/{st.session_state.student_id}/dashboard")
        if dash:
            c1, c2 = st.columns(2)
            c1.metric("Assessments", dash.get("total_assessments", 0))
            c2.metric("Simulations", dash.get("total_simulations", 0))
        if st.button("Sign Out", use_container_width=True):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.rerun()

    st.divider()
    page = st.radio("Navigate", [
        "🏠  Home",
        "🎯  Skill Assessment",
        "🎮  Day-in-Life Simulator",
        "🌳  Career Tree",
        "📅  Study Roadmap",
        "🏫  College Cutoffs",
        "⚖️  Compare Branches",
        "🔍  Explore Branches",
        "💬  Ask the Counsellor",
    ])


# ═════════════════════════════════════════════════════════════════════════════
# HOME
# ═════════════════════════════════════════════════════════════════════════════

if page == "🏠  Home":
    st.title("Career Intelligence Engine 🚀")
    st.caption("Discover your ideal engineering branch through skill assessment, simulations, and AI-powered guidance.")

    c1, c2, c3, c4 = st.columns(4)
    c1.info("**🎯 Assessment**\nDiscover your branch in 10 questions.")
    c2.success("**🎮 Simulator**\nLive a real day as an engineer.")
    c3.warning("**📅 Roadmap**\nSemester-wise study plan.")
    c4.error("**🏫 Cutoffs**\nPune college MHT-CET ranges.")

    st.divider()
    st.subheader("The 4 Branches")
    data = api_get("branches")
    if data and "branches" in data:
        cols = st.columns(2)
        for i, b in enumerate(data["branches"]):
            color = b.get("color", "#4f46e5")
            emoji = BRANCH_EMOJI.get(b["code"], "🎓")
            with cols[i % 2]:
                st.markdown(
                    f"<div style='border-left:4px solid {color};padding:12px 16px;"
                    f"background:{hex_rgba(color)};border-radius:8px;margin-bottom:10px'>"
                    f"<b style='font-size:15px'>{emoji} {b['name']}</b><br>"
                    f"<span style='color:#6b7280;font-size:13px'>{b.get('tagline','')}</span><br>"
                    f"<span style='font-size:12px'>💰 {b.get('entry_salary','')} entry &nbsp;·&nbsp; "
                    f"📈 {b.get('growth_rate','')} growth</span>"
                    f"</div>", unsafe_allow_html=True
                )

    st.divider()
    if not st.session_state.student_id:
        st.info("👆 Register in the sidebar to track your results across sessions.")
    else:
        if st.button("🎯 Start Skill Assessment", type="primary", use_container_width=True):
            for k in ["asmt_questions", "asmt_q_index", "asmt_answers", "asmt_results"]:
                st.session_state[k] = DEFAULTS[k]
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# SKILL ASSESSMENT
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🎯  Skill Assessment":
    st.title("🎯 Skill Assessment")

    # Past results banner
    if st.session_state.student_id and not st.session_state.asmt_results:
        hist = api_get(f"assessment/history/{st.session_state.student_id}")
        if hist and hist.get("total", 0) > 0:
            with st.expander(f"📋 {hist['total']} past assessment(s) — click to view"):
                for sess in hist["sessions"][:3]:
                    top = sess.get("results", {}).get("recommended_branches", [{}])[0]
                    st.caption(
                        f"{sess['completed_at'][:10]}  ·  "
                        f"Top match: **{top.get('name','?')}** ({top.get('match_pct',0):.0f}%)"
                    )

    # ── Results ──────────────────────────────────────────────────────────────
    if st.session_state.asmt_results:
        results = st.session_state.asmt_results
        st.success("✅ Assessment Complete!")

        conf = results.get("confidence", 0)
        st.metric("Confidence Score", f"{conf*100:.0f}%")

        # Radar chart
        skills = {k: v for k, v in results.get("skill_scores", {}).items() if v > 0}
        if skills:
            try:
                import plotly.graph_objects as go
                labels = [k.replace("_", " ").title() for k in skills]
                values = list(skills.values())
                fig = go.Figure(go.Scatterpolar(
                    r=values + [values[0]], theta=labels + [labels[0]],
                    fill="toself", line_color="#4f46e5",
                    fillcolor="rgba(79,70,229,0.15)"
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                    showlegend=False, height=360,
                    margin=dict(l=40, r=40, t=10, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)
            except ImportError:
                cols = st.columns(4)
                for i, (k, v) in enumerate(skills.items()):
                    cols[i % 4].metric(k.replace("_", " ").title(), f"{v:.0f}/10")

        st.divider()
        st.subheader("Your Branch Matches")
        for i, b in enumerate(results.get("recommended_branches", [])):
            code  = b.get("code", "")
            color = BRANCH_COLOR.get(code, "#4f46e5")
            emoji = BRANCH_EMOJI.get(code, "🎓")
            pct   = b.get("match_pct", 0)
            medal = ["🥇", "🥈", "🥉", "4️⃣"][i] if i < 4 else f"#{i+1}"

            with st.expander(
                f"{medal}  {emoji} {b['name']}  —  {pct:.0f}% match",
                expanded=(i == 0)
            ):
                # Match bar
                st.markdown(
                    f"<div style='background:{hex_rgba(color,0.15)};border-radius:999px;height:8px;margin-bottom:10px'>"
                    f"<div style='background:{color};width:{pct}%;height:8px;border-radius:999px'></div>"
                    f"</div>", unsafe_allow_html=True
                )
                st.write(b.get("explanation", ""))

                # Salary quick-view from branch result itself
                bd = api_get(f"branches/{code}")
                if bd:
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Entry", bd.get("entry_salary", "N/A"))
                    col_b.metric("Mid",   bd.get("mid_salary", "N/A"))
                    col_c.metric("Senior",bd.get("senior_salary", "N/A"))
                    st.caption(f"🔭 {bd.get('future_scope','')[:120]}...")

        if results.get("assessment_id"):
            st.caption(f"✅ Saved as Assessment #{results['assessment_id']}")

        # ── PDF Download ──────────────────────────────────────────────────────
        st.divider()
        st.subheader("📄 Download Your Analysis Report")
        st.caption("A full PDF with your skill profile, branch matches, salary outlook, and next steps.")

        col_pdf1, col_pdf2 = st.columns([3, 1])
        with col_pdf1:
            sim_done = (
                st.session_state.get("sim_final") is not None and
                st.session_state.get("sim_branch_code") is not None
            )
            if sim_done:
                st.info(f"✅ Your {st.session_state.get('sim_branch_name','')} simulator results will be included.")
            else:
                st.caption("💡 Tip: Complete the Day-in-Life Simulator first to include your simulation score in the PDF.")

        with col_pdf2:
            if st.button("⚙️ Generate PDF", type="primary", use_container_width=True, key="gen_pdf_btn"):
                with st.spinner("Building your personalised report…"):
                    try:
                        # Fetch branch details for all recommended branches
                        bd_map = {}
                        for b in results.get("recommended_branches", []):
                            code = b.get("code", "")
                            if code:
                                detail = api_get(f"branches/{code}")
                                if detail:
                                    bd_map[code] = detail

                        # Assemble simulator payload only if simulator was completed
                        sim_payload = None
                        if st.session_state.get("sim_final") and st.session_state.get("sim_branch_code"):
                            final_sim = st.session_state.sim_final
                            sim_payload = {
                                "branch_name": st.session_state.get("sim_branch_name", ""),
                                "branch_code": st.session_state.get("sim_branch_code", ""),
                                "total_score": final_sim.get("total_score", 0),
                                "max_score":   final_sim.get("max_score", 0),
                                "percentage":  final_sim.get("percentage", 0),
                                "level":       final_sim.get("level", ""),
                                "message":     final_sim.get("message", ""),
                                "decisions":   list(st.session_state.get("sim_decisions", [])),
                            }

                        student_info = {
                            "name":        st.session_state.get("student_name", ""),
                            "email":       st.session_state.get("student_email", ""),
                            "college":     st.session_state.get("reg_college", ""),
                            "branch_year": st.session_state.get("reg_year", ""),
                        }

                        pdf_bytes = generate_report_pdf(
                            student=student_info,
                            asmt_results=results,
                            sim_results=sim_payload,
                            branch_details=bd_map,
                        )
                        st.session_state["_pdf_bytes"] = pdf_bytes
                        st.success("✅ Report ready!")
                    except Exception as e:
                        st.error(f"PDF generation failed: {e}")

        if st.session_state.get("_pdf_bytes"):
            student_slug = st.session_state.get("student_name", "student").lower().replace(" ", "_")
            filename = f"CIE_Report_{student_slug}_{datetime.now().strftime('%Y%m%d')}.pdf"
            st.download_button(
                label="⬇️ Download PDF Report",
                data=st.session_state["_pdf_bytes"],
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                key="dl_pdf_btn",
            )
        # ── End PDF Download ──────────────────────────────────────────────────

        if st.button("🔄 Retake Assessment", use_container_width=True):
            for k in ["asmt_results", "asmt_q_index", "asmt_answers", "asmt_questions"]:
                st.session_state[k] = DEFAULTS[k]
            st.rerun()
        st.stop()

    # ── Question flow ─────────────────────────────────────────────────────────
    if not st.session_state.asmt_questions:
        data = api_get("assessment/questions")
        if data and "questions" in data:
            st.session_state.asmt_questions = data["questions"]
        else:
            st.warning("Could not load questions. Is the backend running?")
            st.stop()

    questions = st.session_state.asmt_questions
    idx       = st.session_state.asmt_q_index

    st.progress(idx / len(questions), text=f"Question {idx + 1} of {len(questions)}")

    q = questions[idx]
    st.subheader(f"Q{idx + 1}:  {q['question']}")
    if q.get("hint"):
        st.caption(f"💡 {q['hint']}")
    st.markdown("")

    answer = None
    if q["type"] == "scale":
        answer = st.slider(
            "Your rating",
            min_value=q.get("min", 1), max_value=q.get("max", 10),
            value=st.session_state.asmt_answers.get(q["id"], 5),
            key=f"sl_{idx}"
        )
    elif q["type"] == "choice":
        opts  = q["options"]
        prev  = st.session_state.asmt_answers.get(q["id"])
        defi  = next((j for j, o in enumerate(opts) if o["value"] == prev), 0)
        chosen = st.radio("Choose one:", [o["text"] for o in opts], index=defi, key=f"rad_{idx}")
        answer = next((o["value"] for o in opts if o["text"] == chosen), None)

    st.divider()
    cp, cn = st.columns(2)
    with cp:
        if idx > 0 and st.button("← Previous"):
            st.session_state.asmt_q_index -= 1
            st.rerun()
    with cn:
        label = "Next →" if idx < len(questions) - 1 else "Submit & See Results 🎯"
        if st.button(label, type="primary"):
            st.session_state.asmt_answers[q["id"]] = answer
            if idx < len(questions) - 1:
                st.session_state.asmt_q_index += 1
                st.rerun()
            else:
                with st.spinner("Analysing your profile…"):
                    resp = api_post("assessment/submit", {
                        "student_id": st.session_state.student_id,
                        "answers":    st.session_state.asmt_answers
                    })
                if resp:
                    st.session_state.asmt_results = resp
                    st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# DAY-IN-LIFE SIMULATOR
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🎮  Day-in-Life Simulator":
    st.title("🎮 Day-in-the-Life Simulator")

    def _reset_sim():
        for k in ["sim_phase", "sim_branch_code", "sim_branch_name", "sim_intro",
                  "sim_scenario", "sim_decisions", "sim_feedback", "sim_finished", "sim_final"]:
            st.session_state[k] = DEFAULTS[k]

    phase = st.session_state.sim_phase

    # ── Phase 1: Branch selection ─────────────────────────────────────────────
    if phase == "select":
        st.caption("Pick a branch to explore. You'll learn what the job is like, then tackle 4 real scenarios.")
        st.divider()

        resp = api_get("simulator/branches")
        bl   = resp.get("branches", []) if resp else []
        if not bl:
            st.warning("Could not load branches. Is the backend running?")
            st.stop()

        cols = st.columns(len(bl))
        for i, b in enumerate(bl):
            code  = b["code"]
            emoji = BRANCH_EMOJI.get(code, "🎓")
            color = BRANCH_COLOR.get(code, "#4f46e5")
            with cols[i]:
                st.markdown(
                    f"<div style='border:2px solid {color};border-radius:12px;"
                    f"padding:20px;text-align:center;background:{hex_rgba(color)}'>"
                    f"<div style='font-size:36px'>{emoji}</div>"
                    f"<b style='color:{color};font-size:13px'>{b['name']}</b><br>"
                    f"<span style='font-size:12px;color:#6b7280'>{b['total_scenarios']} scenarios</span>"
                    f"</div>", unsafe_allow_html=True
                )
                st.markdown("")
                if st.button(f"Choose {code}", key=f"sel_{code}", use_container_width=True):
                    intro_resp = api_get(f"simulator/intro/{code}") or {}
                    st.session_state.sim_branch_code = code
                    st.session_state.sim_branch_name = b["name"]
                    st.session_state.sim_intro       = intro_resp
                    st.session_state.sim_phase       = "intro"
                    st.rerun()

    # ── Phase 2: Branch intro ─────────────────────────────────────────────────
    elif phase == "intro":
        code  = st.session_state.sim_branch_code
        intro = st.session_state.sim_intro
        color = BRANCH_COLOR.get(code, "#4f46e5")
        emoji = BRANCH_EMOJI.get(code, "🎓")

        if not intro:
            st.warning("Intro not available — jumping to simulation.")
            resp = api_post("simulator/start", {
                "student_id": st.session_state.student_id, "branch_code": code
            })
            if resp and "scenario" in resp:
                st.session_state.sim_branch_name = resp["branch_name"]
                st.session_state.sim_scenario    = resp["scenario"]
                st.session_state.sim_decisions   = []
                st.session_state.sim_feedback    = None
                st.session_state.sim_phase       = "active"
                st.rerun()
            st.stop()

        # Banner
        st.markdown(
            f"<div style='background:{hex_rgba(color,0.12)};border:1.5px solid {color};"
            f"border-radius:12px;padding:16px 22px;margin-bottom:8px'>"
            f"<span style='font-size:28px'>{emoji}</span>"
            f"<span style='font-size:19px;font-weight:500;color:{color};margin-left:10px'>"
            f"Before the simulation — know the job first</span><br>"
            f"<span style='font-size:13px;color:#374151'>{intro.get('tagline','')}</span>"
            f"</div>", unsafe_allow_html=True
        )

        # 4 tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📱  Apps you use",
            "📚  Your 12th knowledge",
            "🔧  Real problems solved",
            "🎬  Watch it in action",
        ])

        # Tab 1: Apps + personality fit
        with tab1:
            st.markdown(f"#### {BRANCH_NAMES.get(code,'')} engineers built parts of these")
            st.caption("You interact with this branch's work every day — you just didn't know it.")
            for app in intro.get("real_apps", []):
                ci, cb = st.columns([1, 9])
                with ci:
                    st.markdown(
                        f"<div style='font-size:38px;text-align:center;padding-top:6px'>"
                        f"{app['emoji']}</div>", unsafe_allow_html=True
                    )
                with cb:
                    st.markdown(f"**{app['app']}**")
                    st.markdown(
                        f"<div style='border-left:3px solid {color};padding:8px 12px;"
                        f"background:{hex_rgba(color,0.06)};border-radius:0 8px 8px 0;"
                        f"font-size:13px;line-height:1.6'>{app['what_they_built']}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<span style='background:{color};color:white;font-size:11px;"
                        f"padding:2px 10px;border-radius:999px'>💡 {app['cool_fact']}</span>",
                        unsafe_allow_html=True
                    )
                st.markdown("")

            st.divider()
            st.markdown("#### You'd enjoy this branch if...")
            for fit in intro.get("personality_fit", []):
                st.markdown(
                    f"<div style='display:flex;gap:10px;margin-bottom:8px'>"
                    f"<span style='color:{color};font-size:17px;flex-shrink:0'>✓</span>"
                    f"<span style='font-size:13px'>{fit}</span>"
                    f"</div>", unsafe_allow_html=True
                )

        # Tab 2: 12th knowledge bridge
        with tab2:
            st.markdown("#### What you studied in 12th → what it becomes in engineering")
            st.caption("Engineering is not starting from scratch. You already have the foundations.")
            st.markdown("")
            for bridge in intro.get("bridge_12th", []):
                st.markdown(
                    f"<div style='display:grid;grid-template-columns:1fr 36px 1fr;"
                    f"gap:0;margin-bottom:12px;align-items:stretch'>"
                    f"<div style='background:#f3f4f6;border-radius:10px 0 0 10px;padding:12px 14px'>"
                    f"<div style='font-size:10px;color:#9ca3af;margin-bottom:3px'>IN 12TH</div>"
                    f"<div style='font-size:13px;font-weight:500'>{bridge['knew_in_12th']}</div>"
                    f"</div>"
                    f"<div style='background:{color};display:flex;align-items:center;"
                    f"justify-content:center;font-size:16px;color:white'>→</div>"
                    f"<div style='background:{hex_rgba(color,0.1)};border-radius:0 10px 10px 0;"
                    f"padding:12px 14px;border:1px solid {hex_rgba(color,0.25)}'>"
                    f"<div style='font-size:10px;color:{color};font-weight:500;margin-bottom:3px'>"
                    f"IN ENGINEERING {bridge['emoji']}</div>"
                    f"<div style='font-size:13px'>{bridge['becomes_in_engineering']}</div>"
                    f"</div></div>",
                    unsafe_allow_html=True
                )

        # Tab 3: Real problems + day timeline
        with tab3:
            st.markdown("#### Real problems this branch solved")
            st.caption("No jargon. The actual problem, why it happened, and how engineers fixed it.")
            for prob in intro.get("real_problems", []):
                with st.expander(f"{prob['emoji']}  {prob['problem'][:75]}..."):
                    st.error(f"**Problem:** {prob['problem']}")
                    st.markdown(
                        f"<div style='background:#fffbeb;border-left:3px solid #f59e0b;"
                        f"padding:10px 14px;border-radius:0 6px 6px 0;font-size:13px;margin:6px 0'>"
                        f"<b>Why it happened:</b> {prob['why_it_happened']}</div>",
                        unsafe_allow_html=True
                    )
                    st.success(f"**Fix:** {prob['how_engineers_fixed_it']}")
                    st.caption(f"📌 What you'd learn: {prob['lesson']}")

            st.divider()
            st.markdown("#### A typical engineer's day")
            MOOD_COLORS = {
                "detective": "#7c3aed", "research": "#0891b2", "focus": "#059669",
                "break": "#6b7280", "team": "#d97706", "creative": "#ec4899", "win": "#16a34a"
            }
            MOOD_LABELS = {
                "detective": "🔍 Debugging", "research": "📊 Research", "focus": "⚡ Deep Work",
                "break": "☕ Break", "team": "👥 Team", "creative": "💡 Design", "win": "🏆 Done"
            }
            for entry in intro.get("day_timeline", []):
                mc = MOOD_COLORS.get(entry.get("mood", "focus"), color)
                ml = MOOD_LABELS.get(entry.get("mood", "focus"), "")
                with st.expander(f"**{entry['time']}** — {entry['task']}"):
                    st.markdown(
                        f"<div style='display:flex;gap:10px;align-items:flex-start'>"
                        f"<span style='background:{mc};color:white;padding:2px 9px;"
                        f"border-radius:999px;font-size:11px;white-space:nowrap;flex-shrink:0'>"
                        f"{ml}</span>"
                        f"<span style='font-size:13px;line-height:1.6'>{entry['detail']}</span>"
                        f"</div>", unsafe_allow_html=True
                    )

        # Tab 4: YouTube search
        with tab4:
            yt_search = intro.get("youtube_search", "day in the life engineer")
            yt_url    = "https://www.youtube.com/results?search_query=" + yt_search.replace(" ", "+")
            st.markdown("#### Watch real engineers describe their day")
            st.caption("Opens a YouTube search — pick any video that looks relevant.")
            st.markdown("")
            st.link_button("▶  Open YouTube — real engineer vlogs", yt_url, use_container_width=True)
            st.caption("No login needed · Filter by upload date · Look for 50k+ views")

        # Reality check + salary + tools (below tabs, above CTA)
        st.divider()
        col_l, col_r = st.columns(2)
        with col_l:
            st.warning(f"💬 **Reality check:** {intro.get('reality_check','')}")
        with col_r:
            st.info(f"💰 **Salary:** {intro.get('salary_snapshot','')}")
            st.markdown("**🛠️ Tools you'll use:**")
            tool_text = "  ·  ".join(
                t.split(" (")[0].split(" —")[0]
                for t in intro.get("tools", [])
            )
            st.caption(tool_text)

        st.divider()
        col_back, col_go = st.columns([1, 2])
        with col_back:
            if st.button("← Change Branch", use_container_width=True):
                _reset_sim(); st.rerun()
        with col_go:
            if st.button(
                f"{emoji}  I'm Ready — Start the {code} Simulation",
                type="primary", use_container_width=True
            ):
                resp = api_post("simulator/start", {
                    "student_id": st.session_state.student_id, "branch_code": code
                })
                if resp and "scenario" in resp:
                    st.session_state.sim_branch_name = resp["branch_name"]
                    st.session_state.sim_scenario    = resp["scenario"]
                    st.session_state.sim_decisions   = []
                    st.session_state.sim_feedback    = None
                    st.session_state.sim_finished    = False
                    st.session_state.sim_final       = None
                    st.session_state.sim_phase       = "active"
                    st.rerun()

    # ── Phase 3: Active simulation ────────────────────────────────────────────
    elif phase == "active":
        code     = st.session_state.sim_branch_code
        color    = BRANCH_COLOR.get(code, "#4f46e5")
        emoji    = BRANCH_EMOJI.get(code, "🎓")
        scenario = st.session_state.sim_scenario

        if not scenario:
            st.warning("Session lost. Please restart.")
            _reset_sim(); st.rerun(); st.stop()

        done   = len(st.session_state.sim_decisions)
        run_sc = sum(d["score"] for d in st.session_state.sim_decisions)

        col_h, col_sc = st.columns([3, 1])
        with col_h:
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:10px'>"
                f"<span style='font-size:24px'>{emoji}</span>"
                f"<b style='font-size:17px;color:{color}'>{st.session_state.sim_branch_name}</b>"
                f"<span style='background:#f3f4f6;padding:2px 10px;border-radius:999px;"
                f"font-size:13px'>Scenario {scenario['index']+1} of {scenario['total']}</span>"
                f"</div>", unsafe_allow_html=True
            )
        with col_sc:
            if done > 0:
                st.metric("Score so far", f"{run_sc}/{done*10}")

        st.progress(scenario["index"] / scenario["total"])

        # Feedback from previous choice
        fb = st.session_state.sim_feedback
        if fb:
            sc  = fb["score"]
            bc  = "#22c55e" if sc >= 8 else "#f59e0b" if sc >= 5 else "#ef4444"
            bg  = "#f0fdf4" if sc >= 8 else "#fffbeb" if sc >= 5 else "#fef2f2"
            st.markdown(
                f"<div style='border-left:4px solid {bc};background:{bg};"
                f"padding:12px 16px;border-radius:8px;margin-bottom:16px'>"
                f"<b>Previous — Score: {sc}/10</b><br>"
                f"{fb['feedback']}<br><br>"
                f"<span style='font-size:13px'><b>Why:</b> {fb['explanation']}</span><br>"
                f"<span style='font-size:13px;color:#374151'><b>💡 Lesson:</b> {fb['learning']}</span>"
                f"</div>", unsafe_allow_html=True
            )

        # Current scenario
        st.subheader(scenario["title"])
        st.markdown(
            f"<div style='background:{hex_rgba(color)};border-radius:8px;"
            f"padding:12px 16px;margin-bottom:14px;font-size:14px;line-height:1.7'>"
            f"<b>Context:</b> {scenario['context']}"
            f"</div>", unsafe_allow_html=True
        )
        st.markdown(f"**{scenario['situation']}**")
        st.markdown("")

        chosen_label = st.radio(
            "Your decision:",
            [f"**{o['id']}.**  {o['text']}" for o in scenario["options"]],
            key=f"sc_{scenario['index']}"
        )
        chosen_id = chosen_label.split(".")[0].replace("**", "").strip()

        col_sub, col_quit = st.columns([2, 1])
        with col_sub:
            if st.button("Submit →", type="primary", use_container_width=True):
                resp = api_post("simulator/decide", {
                    "branch_code":    code,
                    "scenario_index": scenario["index"],
                    "choice_id":      chosen_id,
                    "student_id":     st.session_state.student_id,
                    "all_decisions":  list(st.session_state.sim_decisions),
                })
                if resp:
                    fb_data = resp["feedback"]
                    st.session_state.sim_decisions.append({
                        "scenario_index": scenario["index"],
                        "choice_id":      chosen_id,
                        "score":          fb_data["score"],
                    })
                    st.session_state.sim_feedback = fb_data
                    if fb_data.get("is_last"):
                        st.session_state.sim_final    = resp.get("final", {})
                        st.session_state.sim_finished = True
                        st.session_state.sim_scenario = None
                        st.session_state.sim_phase    = "done"
                    else:
                        st.session_state.sim_scenario = resp.get("next_scenario")
                    st.rerun()
        with col_quit:
            if st.button("Abandon", use_container_width=True):
                _reset_sim(); st.rerun()

    # ── Phase 4: Final results ────────────────────────────────────────────────
    elif phase == "done":
        final = st.session_state.sim_final or {}
        code  = st.session_state.sim_branch_code
        color = BRANCH_COLOR.get(code, "#4f46e5")
        emoji = BRANCH_EMOJI.get(code, "🎓")
        pct   = final.get("percentage", 0)
        bar_c = "#22c55e" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"

        st.subheader(f"{final.get('emoji','🎓')} Simulation Complete")
        st.markdown(f"{emoji} **{st.session_state.sim_branch_name}**")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score",      f"{final.get('total_score',0)}/{final.get('max_score',0)}")
        c2.metric("Percentage", f"{pct:.0f}%")
        c3.metric("Level",      final.get("level",""))

        st.markdown(
            f"<div style='background:#f3f4f6;border-radius:999px;height:12px;margin:8px 0 4px'>"
            f"<div style='background:{bar_c};width:{pct}%;height:12px;border-radius:999px'></div>"
            f"</div>", unsafe_allow_html=True
        )
        st.info(f"💬 {final.get('message','')}")

        # Per-decision summary
        with st.expander("📋 Decision breakdown"):
            for d in st.session_state.sim_decisions:
                sc  = d.get("score", 0)
                dc  = "#22c55e" if sc >= 8 else "#f59e0b" if sc >= 5 else "#ef4444"
                st.markdown(
                    f"Scenario **{d['scenario_index']+1}** — Choice **{d['choice_id']}** — "
                    f"<span style='color:{dc};font-weight:600'>{sc}/10</span>",
                    unsafe_allow_html=True
                )

        if st.button("🔄 Try Another Branch", use_container_width=True):
            _reset_sim(); st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# CAREER TREE
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🌳  Career Tree":
    st.title("🌳 Career Roadmap")
    st.caption("4 years in college → 20-year career path")

    code  = branch_select("Select a branch:", key="ct_sel")
    color = BRANCH_COLOR[code]
    tree  = api_get(f"career-tree/{code}")
    if not tree:
        st.stop()

    st.markdown(f"<h3 style='color:{color};margin-top:16px'>{tree['title']}</h3>", unsafe_allow_html=True)

    for i, stage in enumerate(tree.get("years", [])):
        is_college = i < 3
        bc   = color if is_college else ("#10b981" if i < 5 else "#f59e0b")
        icon = "🎓" if is_college else ("💼" if i < 5 else "🏆")
        ci, cc = st.columns([1, 8])
        with ci:
            st.markdown(
                f"<div style='text-align:center;font-size:26px;padding-top:8px'>{icon}</div>",
                unsafe_allow_html=True
            )
        with cc:
            st.markdown(
                f"<div style='border-left:4px solid {bc};background:{hex_rgba(bc)};"
                f"border-radius:8px;padding:11px 15px;margin-bottom:8px'>"
                f"<b style='color:{bc}'>{stage['label']}</b>  ·  "
                f"<span style='font-weight:600'>{stage['milestone']}</span><br>"
                f"<span style='color:#6b7280;font-size:12px'>{' · '.join(stage['skills'])}</span><br>"
                f"<span style='font-size:13px'>🎯 {stage['goal']}</span>"
                f"</div>", unsafe_allow_html=True
            )
        if i < len(tree["years"]) - 1:
            _, ca = st.columns([1, 8])
            with ca:
                st.markdown(
                    f"<div style='text-align:center;color:{bc};font-size:20px;margin:-4px 0'>↓</div>",
                    unsafe_allow_html=True
                )

    st.divider()
    st.subheader("Where can you go from here?")
    bouts = tree.get("branches_out", [])
    cols  = st.columns(min(len(bouts), 3))
    for i, b in enumerate(bouts):
        with cols[i % 3]:
            st.markdown(
                f"<div style='border:1px solid {color};border-radius:8px;"
                f"padding:9px 13px;font-size:13px;background:{hex_rgba(color)};margin-bottom:8px'>"
                f"{b}</div>", unsafe_allow_html=True
            )

    # Salary chart
    try:
        import plotly.graph_objects as go
        bd = api_get(f"branches/{code}")
        if bd:
            def parse_sal(s):
                nums = [int(x) for x in
                        s.replace(" LPA","").replace("~","").replace("–","-").split("-")
                        if x.strip().isdigit()]
                return sum(nums)//len(nums) if nums else 0
            fig = go.Figure(go.Bar(
                x=["Entry (0–3 yr)", "Mid (3–7 yr)", "Senior (7+ yr)"],
                y=[parse_sal(bd.get("entry_salary","")),
                   parse_sal(bd.get("mid_salary","")),
                   parse_sal(bd.get("senior_salary",""))],
                marker_color=color,
                text=[bd.get("entry_salary",""), bd.get("mid_salary",""), bd.get("senior_salary","")],
                textposition="outside"
            ))
            fig.update_layout(
                yaxis_title="Average LPA", showlegend=False, height=280,
                margin=dict(t=10, b=10), plot_bgcolor="rgba(0,0,0,0)"
            )
            st.divider()
            st.subheader("💰 Salary Progression")
            st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        pass


# ═════════════════════════════════════════════════════════════════════════════
# STUDY ROADMAP
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📅  Study Roadmap":
    st.title("📅 Study Roadmap")
    st.caption("Semester-by-semester subjects + what to build alongside college.")

    code  = branch_select("Select a branch:", key="rm_sel")
    color = BRANCH_COLOR[code]
    data  = api_get(f"roadmap/{code}")
    if not data:
        st.stop()

    st.markdown(f"<h3 style='color:{color};margin-top:16px'>{data['title']}</h3>", unsafe_allow_html=True)

    for sem in data.get("semesters", []):
        with st.expander(f"**{sem['label']}**", expanded=(sem["sem"] <= 2)):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown("**📚 Subjects**")
                for sub in sem["subjects"]:
                    st.caption(f"• {sub}")
            with c2:
                st.info(sem["focus"])
                st.success(sem["tip"])

    st.divider()
    st.subheader("🚀 Parallel Tracks")
    st.caption("Build these skills alongside your semester coursework — not instead of it.")
    for track in data.get("parallel_tracks", []):
        st.markdown(
            f"<div style='border-left:4px solid {color};padding:7px 13px;"
            f"background:{hex_rgba(color)};border-radius:6px;margin-bottom:7px;"
            f"font-size:13px'>{track}</div>",
            unsafe_allow_html=True
        )


# ═════════════════════════════════════════════════════════════════════════════
# COLLEGE CUTOFFS
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🏫  College Cutoffs":
    st.title("🏫 College Cutoffs")
    st.caption("MHT-CET percentile reference ranges — Pune & Maharashtra (2023-24)")
    st.warning(
        "⚠️ Cutoffs change every year. Always verify on the official "
        "[MHT-CET CAP website](https://cetcell.mahacet.org/) before applying."
    )

    code  = branch_select("Select a branch:", key="co_sel")
    color = BRANCH_COLOR[code]
    data  = api_get(f"cutoffs/{code}")
    if not data:
        st.stop()

    st.caption(data.get("note", ""))

    colleges   = data.get("colleges", [])
    tiers      = sorted(set(c["tier"] for c in colleges))
    sel_tier   = st.multiselect("Filter by tier:", tiers, default=tiers)
    filtered   = [c for c in colleges if c["tier"] in sel_tier]
    tier_color = {"Tier 1": "#22c55e", "Tier 2": "#f59e0b", "Tier 3": "#6b7280"}

    for c in filtered:
        tc = tier_color.get(c["tier"], "#6b7280")
        st.markdown(
            f"<div style='border:1px solid #e5e7eb;border-radius:10px;"
            f"padding:12px 16px;margin-bottom:8px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center'>"
            f"<b>{c['name']}</b>"
            f"<span style='background:{tc};color:white;padding:2px 10px;"
            f"border-radius:999px;font-size:11px'>{c['tier']}</span>"
            f"</div>"
            f"<div style='color:#6b7280;font-size:12px;margin-top:3px'>"
            f"📍 {c['location']} &nbsp;·&nbsp; "
            f"📊 <b style='color:#111'>{c['percentile']}</b> &nbsp;·&nbsp; "
            f"💰 {c['fees']}"
            f"</div></div>", unsafe_allow_html=True
        )

    try:
        import plotly.graph_objects as go
        def mid_pct(s):
            s = s.replace("+", "").replace("–", "-")
            parts = [float(x) for x in s.split("-") if x.strip().replace(".", "").isdigit()]
            return sum(parts) / len(parts) if parts else 95.0
        fig = go.Figure(go.Bar(
            x=[mid_pct(c["percentile"]) for c in filtered],
            y=[c["name"].split("(")[0].strip()[:28] for c in filtered],
            orientation="h",
            marker_color=[tier_color.get(c["tier"], "#6b7280") for c in filtered],
            text=[c["percentile"] for c in filtered],
            textposition="outside",
        ))
        fig.update_layout(
            xaxis=dict(title="MHT-CET Percentile", range=[60, 100]),
            height=max(300, len(filtered) * 42),
            margin=dict(l=10, r=70, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.divider()
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        pass


# ═════════════════════════════════════════════════════════════════════════════
# COMPARE BRANCHES
# ═════════════════════════════════════════════════════════════════════════════

elif page == "⚖️  Compare Branches":
    st.title("⚖️ Compare Branches")
    st.caption("Side-by-side view of any two branches.")

    all_opts = list(BRANCH_OPTIONS.keys())
    sel_cols = st.columns(2)
    with sel_cols[0]:
        sel1  = st.selectbox("Branch A:", all_opts, index=0, key="cmp_a")
        code1 = BRANCH_OPTIONS[sel1]
    with sel_cols[1]:
        sel2  = st.selectbox("Branch B:", all_opts, index=2, key="cmp_b")
        code2 = BRANCH_OPTIONS[sel2]

    if code1 == code2:
        st.warning("Please select two different branches.")
        st.stop()

    b1 = api_get(f"branches/{code1}")
    b2 = api_get(f"branches/{code2}")
    if not b1 or not b2:
        st.stop()

    # FIX: create columns once and pass them to the function
    def branch_card(b, col):
        code  = b["code"]
        color = BRANCH_COLOR.get(code, "#4f46e5")
        emoji = BRANCH_EMOJI.get(code, "🎓")
        with col:
            st.markdown(
                f"<div style='border-top:4px solid {color};padding:12px 0'>"
                f"<h3 style='margin:0'>{emoji} {b['name']}</h3>"
                f"<p style='color:#6b7280;font-size:13px;margin:3px 0 0'>{b.get('tagline','')}</p>"
                f"</div>", unsafe_allow_html=True
            )
            c1, c2, c3 = st.columns(3)
            c1.metric("Entry",  b.get("entry_salary",  "N/A"))
            c2.metric("Mid",    b.get("mid_salary",    "N/A"))
            c3.metric("Senior", b.get("senior_salary", "N/A"))
            c1.metric("Growth", b.get("growth_rate",   "N/A"))
            c2.metric("Jobs",   b.get("job_openings",  "N/A"))
            st.markdown("**🔭 Future Scope**")
            st.caption(b.get("future_scope", "")[:200] + "...")
            st.markdown("**🛠️ Core Skills**")
            for sk in b.get("core_skills", []):
                st.markdown(
                    f"<span style='background:{color};color:white;padding:2px 8px;"
                    f"border-radius:999px;font-size:11px;margin:2px;display:inline-block'>"
                    f"{sk}</span>", unsafe_allow_html=True
                )
            st.markdown("")
            st.markdown("**🚀 Career Paths**")
            for cp in b.get("career_paths", []): st.caption(f"• {cp}")

    card_cols = st.columns(2)
    branch_card(b1, card_cols[0])
    branch_card(b2, card_cols[1])

    # Radar chart
    try:
        import plotly.graph_objects as go
        from skill_mapper_final import BRANCH_PROFILES
        dims   = list(BRANCH_PROFILES[code1].keys())
        labels = [d.replace("_", " ").title() for d in dims]
        v1     = [BRANCH_PROFILES[code1].get(d, 0) * 10 for d in dims]
        v2     = [BRANCH_PROFILES[code2].get(d, 0) * 10 for d in dims]
        fig    = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=v1 + [v1[0]], theta=labels + [labels[0]], fill="toself",
            name=b1["name"], line_color=BRANCH_COLOR[code1],
            fillcolor=hex_rgba(BRANCH_COLOR[code1], 0.15)
        ))
        fig.add_trace(go.Scatterpolar(
            r=v2 + [v2[0]], theta=labels + [labels[0]], fill="toself",
            name=b2["name"], line_color=BRANCH_COLOR[code2],
            fillcolor=hex_rgba(BRANCH_COLOR[code2], 0.15)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True, height=400,
            margin=dict(l=30, r=30, t=10, b=10)
        )
        st.divider()
        st.subheader("Skill Requirements Comparison")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        pass


# ═════════════════════════════════════════════════════════════════════════════
# EXPLORE BRANCHES
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🔍  Explore Branches":
    st.title("🔍 Explore Branches")

    data = api_get("branches")
    if not data or "branches" not in data:
        st.error("Could not load branches. Is the backend running?")
        st.stop()

    for b in data["branches"]:
        code  = b["code"]
        color = b.get("color", "#4f46e5")
        emoji = BRANCH_EMOJI.get(code, "🎓")

        st.markdown(
            f"<div style='border-left:5px solid {color};padding:6px 14px;margin-bottom:4px'>"
            f"<h3 style='margin:0'>{emoji} {b['name']}</h3>"
            f"<p style='color:#6b7280;font-size:13px;margin:2px 0 0'>{b.get('tagline','')}</p>"
            f"</div>", unsafe_allow_html=True
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Entry Salary",  b.get("entry_salary",  ""))
        c2.metric("Senior Salary", b.get("senior_salary", ""))
        c3.metric("Growth",        b.get("growth_rate",   ""))
        c4.metric("Job Openings",  b.get("job_openings",  ""))

        with st.expander("Full Details"):
            st.write(b.get("description", ""))
            ca, cb = st.columns(2)
            with ca:
                st.markdown("**📚 Core Subjects**")
                for s in b.get("core_subjects", []):   st.caption(f"• {s}")
                st.markdown("**🛠️ Core Skills**")
                for s in b.get("core_skills", []):     st.caption(f"• {s}")
                st.markdown("**🎓 Higher Studies**")
                for s in b.get("higher_studies", []):  st.caption(f"• {s}")
            with cb:
                st.markdown("**🚀 Career Paths**")
                for cp in b.get("career_paths", []):   st.caption(f"• {cp}")
                st.markdown("**🏢 Top Recruiters**")
                for r in b.get("top_recruiters", []):  st.caption(f"• {r}")
                st.markdown("**📜 Certifications**")
                for c in b.get("certifications", []):  st.caption(f"• {c}")
            st.markdown("**🔭 Future Scope**")
            st.write(b.get("future_scope", ""))
        st.divider()


# ═════════════════════════════════════════════════════════════════════════════
# ASK THE COUNSELLOR
# ═════════════════════════════════════════════════════════════════════════════

elif page == "💬  Ask the Counsellor":
    st.title("💬 Ask the Counsellor")
    st.caption("Built-in knowledge base covers CSE, AIML, Mechanical, Electronics — placements, GATE, salaries, Pune colleges.")

    if not st.session_state.chat_session_id:
        resp = api_post("chat/start", params={"student_id": st.session_state.student_id})
        if resp:
            st.session_state.chat_session_id = resp.get("session_id")
            st.session_state.chat_messages   = [{
                "role": "assistant",
                "content": resp.get("initial_message", "Hi! How can I help?")
            }]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                with st.expander("Sources"):
                    for src in msg["sources"]: st.caption(f"• {src}")

    if len(st.session_state.chat_messages) <= 1:
        suggestions = [
            "What is the salary of a CSE engineer in India?",
            "Which branch is best for AI and machine learning?",
            "What are career options in electronics?",
            "How do I prepare for GATE?",
            "What is the future of mechanical engineering?",
            "Difference between CSE and CSE-AIML?",
        ]
        cols = st.columns(2)
        for i, s in enumerate(suggestions):
            if cols[i % 2].button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state["_pending"] = s
                st.rerun()

    pending = st.session_state.pop("_pending", None)
    prompt  = st.chat_input("Ask anything about engineering branches…") or pending

    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                resp = api_post("chat/message", {
                    "session_id": st.session_state.chat_session_id,
                    "student_id": st.session_state.student_id,
                    "message":    prompt,
                })
            if resp:
                ans = resp.get("message", "")
                src = resp.get("sources", [])
                st.write(ans)
                if src:
                    with st.expander("Sources"):
                        for s in src: st.caption(f"• {s}")
                st.session_state.chat_messages.append({
                    "role": "assistant", "content": ans, "sources": src
                })

# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption("🎓 Career Intelligence Engine  |  CSE · CSE-AIML · MECH · ECE · CIVIL · CHEM · BME · AERO")
