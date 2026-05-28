"""
Career Intelligence Engine — FastAPI Backend v3.1
KEY FIX: Simulator is now fully STATELESS — no in-memory session dict.
         All state lives in the Streamlit frontend. Backend is a pure function.
New:  /api/v1/simulator/decide  (stateless — replaces /simulator/decision)
New:  /api/v1/cutoffs/{branch_code}
New:  /api/v1/roadmap/{branch_code}
Run:  python main.py   or   uvicorn main:app --reload --port 8000
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database_final import (
    Branch, ChatMessage, ChatSession, Assessment,
    SimulationRecord, Student,
    SessionLocal, get_db, init_database, seed_branches,
)
from skill_mapper_final import SkillMapper, run_assessment
from simulator_final import DayInLifeSimulator
from rag_engine_final import RAGEngine

# ─────────────────────────────────────────────────────────────────────────────
# App & singletons
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Career Intelligence Engine",
    description="CSE | CSE-AIML | MECH | ECE | CIVIL | CHEM | BME | AERO counselling API",
    version="3.1.0",
)

# CORS_ORIGINS env var: set to your Render frontend URL in production
# e.g. "https://career-cie-frontend.onrender.com"
# Leave unset locally — defaults to "*" (allow all) for development
_cors_origins = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "*").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

_skill_mapper = SkillMapper()
_simulator    = DayInLifeSimulator()
_rag          = RAGEngine()


@app.on_event("startup")
async def on_startup():
    init_database()
    db = SessionLocal()
    try:
        seed_branches(db)
    finally:
        db.close()
    print("✅  Career Intelligence Engine v3.1 ready")
    print("📚  Swagger docs → http://localhost:8000/docs")


# ─────────────────────────────────────────────────────────────────────────────
# Pydantic models
# ─────────────────────────────────────────────────────────────────────────────

class StudentRegister(BaseModel):
    name:        str
    email:       str
    college:     Optional[str] = ""
    branch_year: Optional[int] = 1

class AssessmentAnswers(BaseModel):
    student_id: Optional[int] = None
    answers:    Dict[str, Any]

class ChatRequest(BaseModel):
    session_id: Optional[int] = None
    student_id: Optional[int] = None
    message:    str

class SimStartRequest(BaseModel):
    student_id:  Optional[int] = None
    branch_code: str

class SimDecideRequest(BaseModel):
    """
    Stateless — no session key needed.
    Frontend sends branch_code + scenario_index + choice_id every time.
    all_decisions is the accumulated list (used for final score on last scenario).
    """
    branch_code:    str
    scenario_index: int                        # 0-based
    choice_id:      str                        # "A" | "B" | "C"
    student_id:     Optional[int] = None
    all_decisions:  Optional[List[Dict]] = []  # [{scenario_index, choice_id, score}]


# ─────────────────────────────────────────────────────────────────────────────
# Health
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "service": "Career Intelligence Engine", "version": "3.1.0"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {
        "status":   "healthy",
        "branches": db.query(Branch).count(),
        "students": db.query(Student).count(),
        "rag_docs": _rag.get_stats()["total_docs"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Students
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/v1/students/register")
def register_student(data: StudentRegister, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == data.email).first()
    if existing:
        return {"student": {"id": existing.id, "name": existing.name,
                            "email": existing.email}, "message": "Welcome back!"}
    s = Student(name=data.name, email=data.email,
                college=data.college or "", branch_year=data.branch_year or 1)
    db.add(s); db.commit(); db.refresh(s)
    return {"student": {"id": s.id, "name": s.name, "email": s.email},
            "message": "Registered successfully!"}

@app.get("/api/v1/students/{student_id}/dashboard")
def student_dashboard(student_id: int, db: Session = Depends(get_db)):
    s = db.query(Student).filter(Student.id == student_id).first()
    if not s:
        raise HTTPException(404, "Student not found")
    return {
        "total_assessments": db.query(Assessment).filter(Assessment.student_id == student_id).count(),
        "total_simulations": db.query(SimulationRecord).filter(SimulationRecord.student_id == student_id).count(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Branches
# ─────────────────────────────────────────────────────────────────────────────

def _bdict(b: Branch) -> Dict:
    return {
        "code": b.code, "name": b.name, "tagline": b.tagline,
        "description": b.description, "core_subjects": b.core_subjects,
        "core_skills": b.core_skills, "career_paths": b.career_paths,
        "top_recruiters": b.top_recruiters, "certifications": b.certifications,
        "higher_studies": b.higher_studies, "future_scope": b.future_scope,
        "entry_salary": b.entry_salary, "mid_salary": b.mid_salary,
        "senior_salary": b.senior_salary, "growth_rate": b.growth_rate,
        "job_openings": b.job_openings, "color": b.color,
    }

@app.get("/api/v1/branches")
def list_branches(db: Session = Depends(get_db)):
    return {"branches": [_bdict(b) for b in db.query(Branch).all()]}

@app.get("/api/v1/branches/{code}")
def get_branch(code: str, db: Session = Depends(get_db)):
    b = db.query(Branch).filter(Branch.code == code.upper()).first()
    if not b:
        raise HTTPException(404, f"Branch '{code}' not found")
    return _bdict(b)


# ─────────────────────────────────────────────────────────────────────────────
# Skill Assessment
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/v1/assessment/questions")
def get_questions():
    qs = _skill_mapper.get_questions()
    return {"questions": qs, "total_questions": len(qs)}

@app.post("/api/v1/assessment/submit")
def submit_assessment(data: AssessmentAnswers, db: Session = Depends(get_db)):
    result = run_assessment(data.answers)
    aid = None
    if data.student_id:
        s = db.query(Student).filter(Student.id == data.student_id).first()
        if s:
            rec = Assessment(
                student_id=data.student_id, raw_answers=data.answers,
                skill_scores=result["skill_scores"],
                recommended_branches=result["recommended_branches"],
                confidence=result["confidence"],
            )
            db.add(rec); db.commit(); db.refresh(rec)
            aid = rec.id
    return {
        "skill_scores":         result["skill_scores"],
        "recommended_branches": result["recommended_branches"],
        "confidence":           result["confidence"],
        "assessment_id":        aid,
    }

@app.get("/api/v1/assessment/history/{student_id}")
def assessment_history(student_id: int, db: Session = Depends(get_db)):
    recs = (db.query(Assessment)
              .filter(Assessment.student_id == student_id)
              .order_by(Assessment.completed_at.desc()).limit(10).all())
    return {"total": len(recs), "sessions": [{
        "id": r.id, "completed_at": r.completed_at.isoformat(),
        "confidence": r.confidence,
        "results": {"skill_scores": r.skill_scores,
                    "recommended_branches": r.recommended_branches,
                    "confidence_score": r.confidence},
    } for r in recs]}


# ─────────────────────────────────────────────────────────────────────────────
# Day-in-Life Simulator  — FULLY STATELESS
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/v1/simulator/branches")
def sim_branches():
    return {"branches": [_simulator.get_branch_info(c)
                         for c in _simulator.get_available_branches()]}

@app.get("/api/v1/simulator/intro/{branch_code}")
def sim_intro(branch_code: str):
    """Return the rich branch intro (daily tasks, tools, video ID) for the pre-sim screen."""
    intro = _simulator.get_intro(branch_code.upper())
    if not intro:
        raise HTTPException(404, f"Intro for '{branch_code}' not found")
    return intro

@app.post("/api/v1/simulator/start")
def sim_start(data: SimStartRequest):
    """Returns first scenario. Zero server-side state stored."""
    code = data.branch_code.upper()
    s = _simulator.get_scenario(code, 0)
    if not s:
        raise HTTPException(400, f"No scenarios for branch '{code}'")
    return {"branch_code": code, "branch_name": s["branch_name"],
            "total_scenarios": s["total"], "scenario": s}

@app.post("/api/v1/simulator/decide")
def sim_decide(data: SimDecideRequest, db: Session = Depends(get_db)):
    """
    Pure-function decision endpoint — no server session required.
    Evaluates choice, returns feedback + next scenario (or final).
    """
    code = data.branch_code.upper()
    fb = _simulator.evaluate_choice(code, data.scenario_index, data.choice_id)
    if "error" in fb:
        raise HTTPException(400, fb["error"])

    response: Dict[str, Any] = {"feedback": fb}

    if fb["is_last"]:
        decisions = list(data.all_decisions or [])
        decisions.append({"scenario_index": data.scenario_index,
                          "choice_id": data.choice_id, "score": fb["score"]})
        final = _simulator.calculate_final_score(decisions)
        response["final"] = final
        if data.student_id:
            try:
                rec = SimulationRecord(
                    student_id=data.student_id, branch_code=code,
                    decisions=decisions, total_score=final["total_score"],
                    max_score=final["max_score"], percentage=final["percentage"],
                    performance=final["level"], is_complete=True,
                    completed_at=datetime.now(),
                )
                db.add(rec); db.commit()
            except Exception:
                pass
    else:
        response["next_scenario"] = _simulator.get_scenario(code, fb["next_index"])

    return response

@app.get("/api/v1/simulator/history/{student_id}")
def sim_history(student_id: int, db: Session = Depends(get_db)):
    recs = (db.query(SimulationRecord)
              .filter(SimulationRecord.student_id == student_id)
              .order_by(SimulationRecord.started_at.desc()).limit(20).all())
    return {"total": len(recs), "records": [{
        "id": r.id, "branch_code": r.branch_code,
        "percentage": r.percentage, "performance": r.performance,
        "started_at": r.started_at.isoformat(),
    } for r in recs]}


# ─────────────────────────────────────────────────────────────────────────────
# RAG Chat
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/v1/chat/start")
def chat_start(student_id: Optional[int] = None, db: Session = Depends(get_db)):
    sess = ChatSession(student_id=student_id)
    db.add(sess); db.commit(); db.refresh(sess)
    return {
        "session_id": sess.id,
        "initial_message": (
            "Hi! 👋 I'm your Career Counsellor. Ask me anything about "
            "CSE, CSE-AIML, Mechanical, or Electronics — placements, "
            "salaries, GATE, Pune college cutoffs, or career paths!"
        ),
    }

@app.post("/api/v1/chat/message")
def chat_message(data: ChatRequest, db: Session = Depends(get_db)):
    sid = data.session_id
    if not sid:
        sess = ChatSession(student_id=data.student_id)
        db.add(sess); db.commit(); db.refresh(sess)
        sid = sess.id
    db.add(ChatMessage(session_id=sid, role="user", content=data.message))
    result = _rag.answer(data.message)
    db.add(ChatMessage(session_id=sid, role="assistant", content=result["answer"]))
    db.commit()
    return {"session_id": sid, "message": result["answer"],
            "sources": result.get("sources", []), "confidence": result.get("confidence", 0.75)}

@app.get("/api/v1/chat/history/{session_id}")
def chat_history(session_id: int, db: Session = Depends(get_db)):
    msgs = (db.query(ChatMessage).filter(ChatMessage.session_id == session_id)
              .order_by(ChatMessage.created_at).all())
    return {"session_id": session_id, "messages": [
        {"role": m.role, "content": m.content, "at": m.created_at.isoformat()}
        for m in msgs
    ]}


# ─────────────────────────────────────────────────────────────────────────────
# College Cutoffs  (Pune / Maharashtra SPPU)
# ─────────────────────────────────────────────────────────────────────────────

CUTOFFS: Dict[str, Dict] = {
    "CSE": {
        "branch": "Computer Science & Engineering",
        "note": "MHT-CET percentile ranges (General/Open category, 2023-24). These change every year.",
        "colleges": [
            {"name": "COEP Technological University",          "location": "Pune",   "percentile": "99.5+",     "fees": "~₹1.2 L/yr", "tier": "Tier 1"},
            {"name": "PICT (Pune Institute of Computer Tech)", "location": "Pune",   "percentile": "99.0–99.5", "fees": "~₹1.5 L/yr", "tier": "Tier 1"},
            {"name": "MIT College of Engineering",             "location": "Pune",   "percentile": "98.5–99.2", "fees": "~₹1.8 L/yr", "tier": "Tier 1"},
            {"name": "VIT Pune",                               "location": "Pune",   "percentile": "97.5–99.0", "fees": "~₹1.6 L/yr", "tier": "Tier 1"},
            {"name": "PCCOE (Pimpri Chinchwad College)",       "location": "Pune",   "percentile": "96.0–98.0", "fees": "~₹1.3 L/yr", "tier": "Tier 2"},
            {"name": "Symbiosis Institute of Technology",      "location": "Pune",   "percentile": "95.0–97.5", "fees": "~₹2.5 L/yr", "tier": "Tier 2"},
            {"name": "Sinhgad College of Engineering",         "location": "Pune",   "percentile": "88.0–93.0", "fees": "~₹1.2 L/yr", "tier": "Tier 2"},
            {"name": "PVPIT Sangli",                           "location": "Sangli", "percentile": "90.0–95.0", "fees": "~₹1.0 L/yr", "tier": "Tier 2"},
            {"name": "GCOE Karad",                             "location": "Karad",  "percentile": "82.0–90.0", "fees": "~₹0.8 L/yr", "tier": "Tier 3"},
        ],
    },
    "CSE-AIML": {
        "branch": "CSE with AI & Machine Learning",
        "note": "Newer branch — typically 0.3–0.5 percentile lower than core CSE at same college.",
        "colleges": [
            {"name": "COEP Technological University",          "location": "Pune", "percentile": "99.2+",     "fees": "~₹1.2 L/yr", "tier": "Tier 1"},
            {"name": "PICT Pune (AI & ML)",                    "location": "Pune", "percentile": "98.0–99.0", "fees": "~₹1.6 L/yr", "tier": "Tier 1"},
            {"name": "MIT College of Engineering (AIML)",      "location": "Pune", "percentile": "98.0–99.0", "fees": "~₹1.9 L/yr", "tier": "Tier 1"},
            {"name": "VIT Pune (AI & Data Science)",           "location": "Pune", "percentile": "97.0–98.5", "fees": "~₹1.8 L/yr", "tier": "Tier 1"},
            {"name": "PCCOE Pune (AI & ML)",                   "location": "Pune", "percentile": "94.0–97.0", "fees": "~₹1.4 L/yr", "tier": "Tier 2"},
            {"name": "Symbiosis Institute of Technology",      "location": "Pune", "percentile": "94.0–97.0", "fees": "~₹2.8 L/yr", "tier": "Tier 2"},
            {"name": "Sinhgad College (AI & ML)",              "location": "Pune", "percentile": "86.0–92.0", "fees": "~₹1.3 L/yr", "tier": "Tier 3"},
        ],
    },
    "MECH": {
        "branch": "Mechanical Engineering",
        "note": "Cutoffs lower than CS branches. Government colleges are highly recommended for placement ROI.",
        "colleges": [
            {"name": "COEP Technological University",  "location": "Pune",   "percentile": "98.5+",     "fees": "~₹1.0 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering",     "location": "Pune",   "percentile": "93.0–97.0", "fees": "~₹1.7 L/yr",  "tier": "Tier 1"},
            {"name": "VIT Pune",                       "location": "Pune",   "percentile": "91.0–95.0", "fees": "~₹1.5 L/yr",  "tier": "Tier 1"},
            {"name": "Sinhgad College of Engineering", "location": "Pune",   "percentile": "82.0–90.0", "fees": "~₹1.1 L/yr",  "tier": "Tier 2"},
            {"name": "PVPIT Sangli",                   "location": "Sangli", "percentile": "78.0–88.0", "fees": "~₹0.9 L/yr",  "tier": "Tier 2"},
            {"name": "GCOE Karad",                     "location": "Karad",  "percentile": "72.0–84.0", "fees": "~₹0.75 L/yr", "tier": "Tier 3"},
            {"name": "DPCOE Pune",                     "location": "Pune",   "percentile": "70.0–82.0", "fees": "~₹1.0 L/yr",  "tier": "Tier 3"},
        ],
    },
    "ECE": {
        "branch": "Electronics & Communication Engineering",
        "note": "Strong VLSI + embedded scope. ISRO/DRDO paths available via GATE.",
        "colleges": [
            {"name": "COEP Technological University",  "location": "Pune",   "percentile": "98.8+",     "fees": "~₹1.1 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering",     "location": "Pune",   "percentile": "94.0–97.5", "fees": "~₹1.8 L/yr",  "tier": "Tier 1"},
            {"name": "VIT Pune",                       "location": "Pune",   "percentile": "92.0–96.0", "fees": "~₹1.6 L/yr",  "tier": "Tier 1"},
            {"name": "PCCOE Pune",                     "location": "Pune",   "percentile": "88.0–93.0", "fees": "~₹1.3 L/yr",  "tier": "Tier 2"},
            {"name": "Sinhgad College of Engineering", "location": "Pune",   "percentile": "82.0–90.0", "fees": "~₹1.2 L/yr",  "tier": "Tier 2"},
            {"name": "PVPIT Sangli",                   "location": "Sangli", "percentile": "76.0–86.0", "fees": "~₹0.9 L/yr",  "tier": "Tier 2"},
            {"name": "GCOE Karad",                     "location": "Karad",  "percentile": "70.0–82.0", "fees": "~₹0.75 L/yr", "tier": "Tier 3"},
        ],
    },

    "CIVIL": {
        "branch": "Civil Engineering",
        "note": "Cutoffs significantly lower than CS branches. Government colleges (COEP, GCOE) offer best placement ROI. GATE is the main route to PSU and IES.",
        "colleges": [
            {"name": "COEP Technological University",          "location": "Pune",       "percentile": "97.0–98.5", "fees": "~₹1.0 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering",             "location": "Pune",       "percentile": "88.0–93.0", "fees": "~₹1.7 L/yr",  "tier": "Tier 1"},
            {"name": "VIT Pune",                               "location": "Pune",       "percentile": "85.0–91.0", "fees": "~₹1.5 L/yr",  "tier": "Tier 1"},
            {"name": "PCCOE (Pimpri Chinchwad College)",       "location": "Pune",       "percentile": "80.0–88.0", "fees": "~₹1.2 L/yr",  "tier": "Tier 2"},
            {"name": "Sinhgad College of Engineering",         "location": "Pune",       "percentile": "75.0–84.0", "fees": "~₹1.1 L/yr",  "tier": "Tier 2"},
            {"name": "PVPIT Sangli",                           "location": "Sangli",     "percentile": "70.0–80.0", "fees": "~₹0.9 L/yr",  "tier": "Tier 2"},
            {"name": "GCOE Karad",                             "location": "Karad",      "percentile": "65.0–76.0", "fees": "~₹0.75 L/yr", "tier": "Tier 3"},
            {"name": "DPCOE Pune",                             "location": "Pune",       "percentile": "62.0–74.0", "fees": "~₹1.0 L/yr",  "tier": "Tier 3"},
            {"name": "Rajarambapu Institute of Technology",    "location": "Sangli",     "percentile": "68.0–78.0", "fees": "~₹0.85 L/yr", "tier": "Tier 3"},
        ],
    },

    "CHEM": {
        "branch": "Chemical Engineering",
        "note": "Niche branch with strong PSU opportunities (ONGC, HPCL, BPCL) via GATE. Pune has a strong pharma and specialty chemical cluster for placement.",
        "colleges": [
            {"name": "ICT Mumbai (Institute of Chemical Technology)", "location": "Mumbai", "percentile": "99.0+",     "fees": "~₹1.1 L/yr",  "tier": "Tier 1"},
            {"name": "UICT Mumbai (Govt)",                            "location": "Mumbai", "percentile": "96.0–98.5", "fees": "~₹0.6 L/yr",  "tier": "Tier 1"},
            {"name": "COEP Technological University",                 "location": "Pune",   "percentile": "95.0–97.5", "fees": "~₹1.0 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering",                    "location": "Pune",   "percentile": "86.0–91.0", "fees": "~₹1.7 L/yr",  "tier": "Tier 2"},
            {"name": "LIT Nagpur (Govt)",                             "location": "Nagpur", "percentile": "82.0–88.0", "fees": "~₹0.7 L/yr",  "tier": "Tier 2"},
            {"name": "SGGSIE&T Nanded (Govt)",                        "location": "Nanded", "percentile": "80.0–87.0", "fees": "~₹0.65 L/yr", "tier": "Tier 2"},
            {"name": "Bharati Vidyapeeth COE Pune",                   "location": "Pune",   "percentile": "72.0–82.0", "fees": "~₹1.1 L/yr",  "tier": "Tier 3"},
            {"name": "PVPIT Sangli",                                  "location": "Sangli", "percentile": "68.0–78.0", "fees": "~₹0.9 L/yr",  "tier": "Tier 3"},
        ],
    },

    "BME": {
        "branch": "Biomedical Engineering",
        "note": "Newer branch — fewer colleges offer it in Maharashtra. ICT Mumbai and a few Pune colleges are the top options. MS abroad (USA) is a very strong path.",
        "colleges": [
            {"name": "ICT Mumbai (Biomedical)",                     "location": "Mumbai", "percentile": "97.0–99.0", "fees": "~₹1.1 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering (Biomedical)",     "location": "Pune",   "percentile": "88.0–93.0", "fees": "~₹1.8 L/yr",  "tier": "Tier 1"},
            {"name": "Symbiosis Institute of Technology",           "location": "Pune",   "percentile": "85.0–91.0", "fees": "~₹2.8 L/yr",  "tier": "Tier 1"},
            {"name": "VIT Pune (Biomedical)",                       "location": "Pune",   "percentile": "82.0–89.0", "fees": "~₹1.6 L/yr",  "tier": "Tier 2"},
            {"name": "Sinhgad College of Engineering",              "location": "Pune",   "percentile": "72.0–82.0", "fees": "~₹1.2 L/yr",  "tier": "Tier 2"},
            {"name": "DYPCOE Akurdi Pune",                          "location": "Pune",   "percentile": "68.0–78.0", "fees": "~₹1.1 L/yr",  "tier": "Tier 3"},
            {"name": "Rajarambapu Institute of Technology",         "location": "Sangli", "percentile": "65.0–75.0", "fees": "~₹0.85 L/yr", "tier": "Tier 3"},
        ],
    },

    "AERO": {
        "branch": "Aerospace Engineering",
        "note": "Very few colleges in Maharashtra offer Aerospace. IIT Bombay (JEE Advanced) and MIT Pune are the top options. GATE is critical for ISRO/HAL/DRDO.",
        "colleges": [
            {"name": "IIT Bombay (Aerospace)",                  "location": "Mumbai", "percentile": "JEE Advanced — top 1000 rank", "fees": "~₹1.0 L/yr",  "tier": "Tier 1"},
            {"name": "MIT College of Engineering (Aerospace)",  "location": "Pune",   "percentile": "92.0–96.0",                   "fees": "~₹1.9 L/yr",  "tier": "Tier 1"},
            {"name": "Symbiosis Institute of Technology",       "location": "Pune",   "percentile": "88.0–93.0",                   "fees": "~₹2.8 L/yr",  "tier": "Tier 1"},
            {"name": "DYPIET Pune",                             "location": "Pune",   "percentile": "78.0–87.0",                   "fees": "~₹1.3 L/yr",  "tier": "Tier 2"},
            {"name": "Sinhgad College of Engineering",          "location": "Pune",   "percentile": "74.0–84.0",                   "fees": "~₹1.2 L/yr",  "tier": "Tier 2"},
            {"name": "SITRC Nashik",                            "location": "Nashik", "percentile": "68.0–78.0",                   "fees": "~₹1.0 L/yr",  "tier": "Tier 3"},
        ],
    },
}

@app.get("/api/v1/cutoffs/{branch_code}")
def get_cutoffs(branch_code: str):
    code = branch_code.upper()
    data = CUTOFFS.get(code)
    if not data:
        raise HTTPException(404, f"Cutoff data for '{code}' not found")
    return data


# ─────────────────────────────────────────────────────────────────────────────
# Semester-wise Study Roadmap
# ─────────────────────────────────────────────────────────────────────────────

ROADMAPS: Dict[str, Dict] = {
    "CSE": {
        "title": "CSE — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Physics", "Basic Electronics", "C Programming", "Engineering Drawing"], "focus": "Build C programming habit. Solve 1 problem daily.", "tip": "C is the foundation of everything. Master pointers now."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Data Structures (C)", "Digital Logic Design", "OOP with Java", "Environmental Science"], "focus": "Data Structures is your most important subject. Start NOW.", "tip": "Code every DS from scratch — don't just read theory."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Discrete Mathematics", "Computer Organisation", "Operating Systems", "Database Management Systems", "Design Patterns"], "focus": "OS + DBMS form the backbone of all tech interviews.", "tip": "Practice SQL queries daily on HackerRank. Understand process scheduling deeply."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Theory of Computation", "Computer Networks", "Microprocessors", "Software Engineering", "Algorithms Analysis"], "focus": "Algorithms + Networks — critical for placements.", "tip": "Solve 200+ LeetCode problems. Study OSI model thoroughly."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Compiler Design", "Advanced Algorithms", "Web Technologies (HTML/CSS/JS)", "System Software", "Mini Project"], "focus": "Build your first full-stack web project.", "tip": "Get your first internship this summer — even 1 month matters a lot."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Machine Learning Intro", "Cloud Computing (AWS/Azure)", "Information Security", "Mobile App Development", "Internship"], "focus": "Internship is the #1 priority in Sem 6.", "tip": "Apply to 50+ companies for internship. Off-campus > waiting for on-campus."},
            {"sem": 7, "label": "Semester 7", "subjects": ["System Design", "DevOps & CI/CD", "Elective (Blockchain / IoT / AI)", "Major Project Phase 1", "Soft Skills"], "focus": "System Design separates SDE from senior SDE.", "tip": "Read 'Designing Data-Intensive Applications'. Practice on Excalidraw."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "Placement Preparation", "Open Source Contribution", "Final Exams"], "focus": "Crack placements. Target product companies over service companies.", "tip": "5 quality LeetCode mediums per day. Mock interviews on Pramp."},
        ],
        "parallel_tracks": [
            "🏆 Competitive Programming: Codeforces / LeetCode (start Sem 2)",
            "🌐 Web Dev: HTML → CSS → JS → React → Node.js (Sem 3–5)",
            "☁️ Cloud Cert: AWS Cloud Practitioner → AWS SAA (Sem 6–7)",
            "🔓 Open Source: Contribute to GitHub projects (Sem 5 onwards)",
        ],
    },
    "CSE-AIML": {
        "title": "CSE-AIML — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Physics", "Python Programming", "C Programming", "Statistics Basics"], "focus": "Python fluency is your #1 goal.", "tip": "Learn Python, NumPy, Matplotlib. Complete Kaggle's free Python course."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Linear Algebra", "Probability & Statistics", "Data Structures", "OOP with Python", "Calculus"], "focus": "Maths is as important as coding for AIML.", "tip": "3Blue1Brown's Linear Algebra videos are better than any textbook."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Database Systems", "Operating Systems", "Machine Learning Fundamentals", "Data Wrangling with Pandas", "Visualisation (Matplotlib/Seaborn)"], "focus": "Your first ML project — do Titanic Survival on Kaggle.", "tip": "Understand bias-variance tradeoff deeply. It comes up in every ML interview."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Deep Learning Fundamentals", "Neural Networks (CNNs, RNNs)", "Computer Networks", "Computer Vision Basics", "Statistics for ML"], "focus": "Build a CNN image classifier project.", "tip": "Fast.ai's Practical Deep Learning course is worth 10x any college lecture."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Natural Language Processing", "Reinforcement Learning", "Big Data (Spark/Hadoop)", "MLOps Introduction", "Mini Project"], "focus": "Build an NLP project + start reading research papers.", "tip": "Read 'Attention Is All You Need' — transformers are the foundation of modern AI."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Generative AI & LLMs", "Data Engineering (dbt/Airflow)", "Cloud ML (AWS SageMaker / GCP Vertex)", "Advanced Computer Vision", "Internship"], "focus": "ML Engineer internship is gold. Kaggle competitions help get interviews.", "tip": "A Kaggle competition medal opens interview doors at top companies."},
            {"sem": 7, "label": "Semester 7", "subjects": ["Production ML Systems", "Responsible AI & Fairness", "Elective (Graph Neural Nets / Federated Learning)", "Major Project Phase 1"], "focus": "Build an end-to-end ML pipeline: data → model → deployed API.", "tip": "MLflow + FastAPI + Docker = production ML portfolio that impresses."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "Placement Prep / MS Applications", "Research Paper Writing", "Final Exams"], "focus": "Placements or MS/PhD applications.", "tip": "For MS abroad: GRE + strong SOP + 1 research publication = strong application."},
        ],
        "parallel_tracks": [
            "📊 Kaggle: Competitions + notebook sharing (start Sem 3)",
            "🤗 Hugging Face: Fine-tune LLMs on custom datasets (Sem 6+)",
            "📝 Research: Read 1 ML paper per week from arXiv (from Sem 5)",
            "☁️ Cloud ML Cert: AWS ML Specialty / GCP Professional ML (Sem 7)",
        ],
    },
    "MECH": {
        "title": "Mechanical Engineering — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Engineering Physics", "Engineering Drawing & CAD", "Workshop Practice", "Basic Electrical Engineering"], "focus": "Engineering Drawing is critical — take it very seriously.", "tip": "AutoCAD basics in Sem 1 gives you a 2-year head start on your peers."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Engineering Mechanics (Statics & Dynamics)", "Manufacturing Processes I", "Thermodynamics I", "Material Science"], "focus": "Thermodynamics + Engineering Mechanics are your two pillars.", "tip": "Visualise force diagrams for every problem. Engineering Mechanics needs spatial thinking."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Fluid Mechanics", "Strength of Materials", "Theory of Machines I", "Thermodynamics II", "Metrology & Quality Control"], "focus": "Strength of Materials + Fluid Mechanics — hardest but most important semesters.", "tip": "Practice SOM problems daily. Draw Free Body Diagrams every single time."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Heat Transfer", "Machine Design I", "Theory of Machines II", "Manufacturing Processes II", "Industrial Engineering"], "focus": "Machine Design: learn to select materials and calculate dimensions.", "tip": "Practice SolidWorks alongside Machine Design — visualise what you design."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Refrigeration & Air Conditioning", "CAD/CAM & CNC Programming", "Finite Element Analysis (FEA)", "Control Systems", "Mini Project"], "focus": "FEA project in ANSYS — extremely valuable for core mechanical jobs.", "tip": "A simple FEA simulation (stress analysis on a bracket) impresses interviewers."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Robotics & Automation", "Power Plant Engineering", "Automobile Engineering", "Operations Research", "Industrial Internship"], "focus": "Core sector internship (auto/HVAC/manufacturing). Skip IT internships.", "tip": "L&T, Tata Motors, Cummins, Bosch internships are 10x more valuable for Mech."},
            {"sem": 7, "label": "Semester 7", "subjects": ["Advanced Manufacturing Technology", "Mechatronics & PLC", "Product Lifecycle Management", "MATLAB/Simulink", "Major Project Phase 1"], "focus": "Major project must have real design + FEA simulation.", "tip": "GATE preparation starts here if you want M.Tech or a PSU job."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "GATE Prep / Core Placements", "Elective (EV Technology / Additive Manufacturing)", "Final Exams"], "focus": "GATE score or core company placement. Both need focused effort.", "tip": "GATE Mechanical: Thermodynamics + SOM + Fluid Mechanics carry the most marks."},
        ],
        "parallel_tracks": [
            "🖥️ CAD: AutoCAD → SolidWorks → CATIA (Sem 1–4, get CSWA cert by Sem 5)",
            "⚙️ Simulation: ANSYS Mechanical (FEA) + ANSYS Fluent (CFD) (Sem 5–7)",
            "🤖 Automation: MATLAB + Arduino + PLC programming basics (Sem 5+)",
            "📋 Certifications: SolidWorks CSWA by Sem 5, Six Sigma Green Belt by Sem 7",
        ],
    },
    "ECE": {
        "title": "Electronics & Communication — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Physics (Semiconductors)", "Basic Electronics", "Programming in C", "Engineering Drawing"], "focus": "Understand how a transistor works — it's the atom of electronics.", "tip": "Build simple LED + resistor circuits on a breadboard. Hands-on from Day 1."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Analog Electronics", "Digital Electronics", "Signals & Systems", "Data Structures"], "focus": "Analog circuits + Digital logic — the absolute heart of ECE.", "tip": "Simulate circuits in LTSpice before building them physically. Saves components."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Electronic Devices & Circuits", "Digital Signal Processing", "Microprocessors (8085/8086)", "Communication Theory", "Electromagnetic Theory"], "focus": "DSP + Communication theory — tough but essential for core jobs.", "tip": "Z-transforms and Fourier analysis: solve 20 problems per chapter minimum."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Analog Communication Systems", "Digital Communication Systems", "VLSI Design I (Verilog/VHDL)", "Microcontrollers (8051/ARM/STM32)", "Control Systems"], "focus": "Start Verilog now — VLSI jobs require 1+ year of HDL experience.", "tip": "Program an Arduino/STM32 project. Hardware + code = your first portfolio piece."},
            {"sem": 5, "label": "Semester 5", "subjects": ["RF & Antenna Design", "Embedded Systems & RTOS", "VLSI Design II (Physical Design)", "Wireless Communication (4G/5G)", "Mini Project (IoT / FPGA)"], "focus": "Embedded Systems project on STM32 or FPGA.", "tip": "STM32 + sensors (temperature, IMU) + display = compelling embedded portfolio."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Satellite & Radar Communication", "PCB Design (KiCAD / Altium)", "Internet of Things Architecture", "Signal Processing Applications", "Internship (Embedded/VLSI/Telecom)"], "focus": "Embedded / VLSI / telecom internship is career-defining.", "tip": "Qualcomm, Texas Instruments, STMicro, ISRO internships — apply 5 months early."},
            {"sem": 7, "label": "Semester 7", "subjects": ["5G NR & Next-Gen Networks", "ML for Signal Processing (Edge AI)", "Low-Power IC Design", "Elective (Image Processing / Radar)", "Major Project Phase 1"], "focus": "Combine ML with ECE — Edge AI on microcontrollers is extremely hot.", "tip": "TensorFlow Lite on STM32 or Raspberry Pi = rare and impressive skill combo."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "Placement Preparation", "GATE Preparation (M.Tech VLSI)", "Final Exams"], "focus": "Core ECE placements or IT roles. GATE for M.Tech VLSI at IITs.", "tip": "For VLSI roles: Verilog + one FPGA project + Cadence Virtuoso basics = interview ready."},
        ],
        "parallel_tracks": [
            "⚡ Electronics Sim: LTSpice → Proteus → KiCAD PCB Design (Sem 2–6)",
            "🔧 Embedded: Arduino → STM32 → FreeRTOS (Sem 4–7)",
            "🖥️ FPGA/VLSI: Verilog on ModelSim / Xilinx Vivado (Sem 4–7)",
            "📡 Networking: Cisco CCNA / Jio 5G certification (Sem 7+)",
        ],
    },

    "CIVIL": {
        "title": "Civil Engineering — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Engineering Physics", "Engineering Drawing & Graphics", "Building Materials & Construction", "Environmental Studies"], "focus": "Engineering Drawing is your most important Sem 1 skill — take it seriously.", "tip": "Practise orthographic and isometric projections daily. Spatial thinking is the core of civil engineering."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Engineering Mechanics (Statics)", "Surveying I", "Fluid Mechanics I", "Basic Electrical Engineering"], "focus": "Engineering Mechanics and Surveying are the two pillars — both need regular practice.", "tip": "Go for actual surveying fieldwork whenever possible. Classroom theory is not enough for surveying."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Strength of Materials", "Fluid Mechanics II", "Concrete Technology", "Geotechnical Engineering I (Soil Mechanics)", "Surveying II (Total Station / GPS)"], "focus": "Strength of Materials is the toughest and most important subject of your degree.", "tip": "Draw shear force and bending moment diagrams for every single problem. Never skip this step."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Structural Analysis I", "Geotechnical Engineering II (Foundation)", "Transportation Engineering I (Highway)", "Hydraulics & Hydraulic Machines", "Construction Materials Testing Lab"], "focus": "Structural Analysis is where civil engineering becomes real — learn it deeply.", "tip": "Start AutoCAD Civil 3D now. Even basic proficiency separates you at internship interviews."},
            {"sem": 5, "label": "Semester 5", "subjects": ["RCC Design (Reinforced Cement Concrete)", "Structural Analysis II", "Transportation Engineering II (Railways & Airports)", "Environmental Engineering I (Water Supply)", "Mini Project + Lab"], "focus": "RCC Design is the most industry-relevant subject — every site job needs it.", "tip": "Design a real G+3 building in STAAD.Pro as a self-project. Share it on LinkedIn — it gets noticed."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Steel Structure Design", "Environmental Engineering II (Sewage Treatment)", "Quantity Surveying & Valuation", "Construction Management", "Site Internship"], "focus": "Site internship is non-negotiable — go to an actual construction site, not an office.", "tip": "L&T Construction, Shapoorji, and MSRDC internships are available via referrals. Your professors often know site engineers."},
            {"sem": 7, "label": "Semester 7", "subjects": ["Pre-stressed Concrete", "Urban Planning & Smart Cities", "Revit BIM (Building Information Modelling)", "Elective (Remote Sensing / Green Buildings / Earthquake Engg)", "Major Project Phase 1"], "focus": "BIM is the future of civil engineering — learn Revit now while others wait.", "tip": "GATE preparation must start Sem 7 if you want IIT M.Tech or PSU. Structures + Soil + Fluid carry the most marks."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "GATE Preparation / Core Placements", "Project Cost Control & Contract Management", "Final Exams"], "focus": "GATE rank for PSU / IES or direct core company placement — choose your path early.", "tip": "GATE Civil: Structural Analysis + RCC + Geotechnical + Fluid Mechanics are the highest-weightage topics."},
        ],
        "parallel_tracks": [
            "🖥️ Software: AutoCAD → STAAD.Pro → ETABS → Revit BIM (Sem 1–7, one tool at a time)",
            "📐 Design Practice: Design one real structure per semester (retaining wall, beam, column, footing, slab)",
            "📋 GATE Prep: Start Sem 7, focus on 5 core subjects — skip attempting all 12",
            "🏙️ Smart Cities: GIS basics (QGIS free), remote sensing, urban mobility planning (Sem 6+)",
        ],
    },

    "CHEM": {
        "title": "Chemical Engineering — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Engineering Chemistry", "Engineering Physics", "C Programming / Python Basics", "Engineering Drawing"], "focus": "Chemistry and Maths together — chemical engineering is more mathematical than you expect.", "tip": "Learn Python basics now. Process simulation tools (HYSYS, Aspen) use Python scripting extensively."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Chemical Process Calculations (Stoichiometry)", "Fluid Mechanics", "Organic Chemistry Fundamentals", "Thermodynamics I"], "focus": "Stoichiometry + Fluid Mechanics are the first real chemical engineering subjects. Master them.", "tip": "Stoichiometry is deceptively simple. Do 30+ numerical problems per chapter — they appear in every placement exam."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Chemical Engineering Thermodynamics II", "Heat Transfer Operations", "Mechanical Operations", "Process Instrumentation & Control Basics", "Material Science"], "focus": "Heat Transfer is used in every plant you will ever work in. Understand it beyond formulas.", "tip": "Connect every heat transfer concept to a real industry application — heat exchangers, boilers, condensers. It helps retention."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Mass Transfer I (Distillation, Absorption)", "Chemical Reaction Engineering I", "Process Control & Instrumentation", "Fluid-Particle Systems", "Numerical Methods for ChE"], "focus": "Chemical Reaction Engineering (CRE) and Mass Transfer are the two hardest and most important subjects of your degree.", "tip": "CRE problems require deep understanding — not formula substitution. Understand residence time distribution physically."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Mass Transfer II (Extraction, Drying, Evaporation)", "Chemical Reaction Engineering II (Catalysis)", "Process Equipment Design", "Safety & Hazard Analysis (HAZOP)", "Mini Project (Process Design)"], "focus": "Process Equipment Design and HAZOP — the two skills plants actually test in interviews.", "tip": "Do a real HAZOP exercise on a simple process (even a heat exchanger). Document it properly. It impresses interviewers enormously."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Petroleum Refining & Petrochemicals", "Polymer Technology", "Environmental Engineering (Effluent Treatment)", "Plant Design & Economics", "Industrial Internship (Refinery / Pharma / Specialty Chemicals)"], "focus": "Industrial internship at a real plant — refinery, pharma, or fertilizer — is the most valuable experience you can get.", "tip": "UPL, Thermax, Reliance, Sun Pharma all take SPPU interns. Apply in Sem 5 itself — Sem 6 is too late."},
            {"sem": 7, "label": "Semester 7", "subjects": ["Process Simulation (Aspen HYSYS / Aspen Plus)", "Biochemical Engineering & Bioreactors", "Elective (Green Chemistry / Pharmaceutical Tech / Petroleum)", "Major Project Phase 1"], "focus": "Aspen HYSYS simulation is the most in-demand ChE tool — build a real distillation column simulation.", "tip": "GATE ChE preparation starts Sem 7. Mass Transfer + CRE + Thermodynamics carry maximum marks."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "GATE Prep / Core Placements", "Process Safety Management (Advanced)", "Final Exams"], "focus": "Core company placements or GATE for PSU (ONGC, HPCL, IOCL) — both require the same deep subject knowledge.", "tip": "GATE ChE cutoffs for PSU are competitive. Start mock tests from Sem 7 itself. 3 months is not enough for ChE GATE."},
        ],
        "parallel_tracks": [
            "💻 Simulation: Aspen HYSYS (free student version) → Aspen Plus → MATLAB for process modelling (Sem 5–7)",
            "🛡️ Safety: HAZOP certification online (AIChE offers courses) — rare skill that plants value immediately",
            "📋 GATE Prep: Mass Transfer + CRE + Thermodynamics + Fluid Mechanics = 65% of GATE ChE marks",
            "🧪 Lab Skills: Every lab experiment should have a proper report with error analysis — recruiters check lab notebooks",
        ],
    },

    "BME": {
        "title": "Biomedical Engineering — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Engineering Physics", "Basic Electronics", "C Programming", "Engineering Drawing"], "focus": "Electronics and programming from Sem 1 — BME is more technical than most students expect.", "tip": "Build a simple LED blink circuit on Arduino. Hardware comfort early sets you apart in BME lab work."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II", "Human Anatomy & Physiology I", "Analog & Digital Electronics", "Signals & Systems", "Biophysics"], "focus": "Anatomy & Physiology is your most unique subject — understand the body as an engineering system.", "tip": "Study physiology with an engineering lens: heart = pump, lungs = gas exchanger, neurons = signal cables. This thinking is what makes a good biomedical engineer."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Human Anatomy & Physiology II", "Medical Instrumentation I", "Biomechanics", "Biomaterials", "Probability & Biostatistics"], "focus": "Medical Instrumentation is your core technical subject — where biology meets electronics.", "tip": "Study how an ECG machine works from first principles: electrodes → amplifier → ADC → signal processing → display. Each step is a separate engineering problem."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Medical Instrumentation II", "Biomedical Signal Processing (ECG / EEG / EMG)", "Microprocessors & Embedded Systems for Medical Devices", "Fluid Mechanics in Biology (Cardiovascular / Respiratory)", "Control Systems in Physiology"], "focus": "Biomedical Signal Processing is the most important technical subject of your degree.", "tip": "Implement ECG filtering in MATLAB — remove baseline wander, powerline interference, and EMG noise. This one project can take you to any placement interview."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Medical Imaging (X-Ray, CT, MRI, Ultrasound)", "Hospital Information Systems & Electronic Health Records", "Rehabilitation Engineering & Prosthetics", "Biomedical Optics & Laser Applications", "Mini Project (Medical Device Prototype)"], "focus": "Medical Imaging is the highest-value subject for placements at GE Healthcare, Philips, Siemens Healthineers.", "tip": "Build a simple SpO2 (blood oxygen) monitor using Arduino + MAX30100 sensor as your mini project. Costs ₹500, teaches you 5 subjects simultaneously."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Regulatory Affairs (FDA 510k / CDSCO MDR)", "Telemedicine & Digital Health", "Biosensors & Wearable Devices", "Clinical Engineering (Hospital Equipment Management)", "Hospital / Medical Device Internship"], "focus": "Hospital internship or medical device company internship — rarer and more valuable than any IT internship.", "tip": "Contact the biomedical engineering department of Ruby Hall, KEM, or Sassoon Hospital in Pune directly for internship. Hospitals usually say yes — almost no students ask."},
            {"sem": 7, "label": "Semester 7", "subjects": ["AI & ML in Medical Imaging", "Drug Delivery Systems & Pharmacokinetics", "Biomedical Nanotechnology", "Elective (Neural Engineering / Cardiovascular Devices / Orthopaedic Implants)", "Major Project Phase 1"], "focus": "AI in Medical Imaging is the hottest skill in BME — combine your signal processing knowledge with ML.", "tip": "Train a CNN on chest X-rays to detect pneumonia (NIH dataset is free). This one project gets interviews at Philips, GE, and AI health startups."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "Placement Preparation", "Clinical Trials & Medical Device Validation", "Final Exams"], "focus": "Core medical device placements or MS abroad applications — both need a strong project portfolio.", "tip": "For MS USA in BME: GRE + 2 strong reference letters + research publication or patent = strong application. Start GRE prep in Sem 7."},
        ],
        "parallel_tracks": [
            "💻 Signal Processing: MATLAB → Python (SciPy / NumPy) for biomedical signals (Sem 3–6)",
            "🤖 Medical AI: Python ML → medical imaging datasets (NIH ChestX-ray14, MIMIC) → deploy model (Sem 6–8)",
            "🔬 Hardware: Arduino → Raspberry Pi → custom PCB for wearable sensor (Sem 3–7)",
            "📜 Regulatory: Study FDA 510(k) process and CDSCO Medical Device Rules 2017 — rare knowledge that gets you hired fast",
        ],
    },

    "AERO": {
        "title": "Aerospace Engineering — 8-Semester Study Roadmap",
        "semesters": [
            {"sem": 1, "label": "Semester 1", "subjects": ["Engineering Maths I", "Engineering Physics", "Engineering Drawing & CAD Basics", "C Programming", "Introduction to Aerospace Engineering"], "focus": "Maths is your most important investment — aerospace has the highest mathematical demands of any engineering branch.", "tip": "If you are not comfortable with differential equations and vectors, fix that now. Everything in aerospace — aerodynamics, structures, propulsion — depends on them."},
            {"sem": 2, "label": "Semester 2", "subjects": ["Engineering Maths II (Differential Equations)", "Engineering Mechanics (Statics & Dynamics)", "Thermodynamics I", "Material Science & Metallurgy", "Engineering Drawing (Aerospace components)"], "focus": "Engineering Mechanics and Thermodynamics together form the foundation of all aerospace propulsion and structures work.", "tip": "Study how an aircraft wing generates lift using Bernoulli + circulation theory. Understanding the physics first makes every derivation meaningful rather than mechanical."},
            {"sem": 3, "label": "Semester 3", "subjects": ["Aerodynamics I (Subsonic — Incompressible Flow)", "Aircraft Structures I (Stress Analysis)", "Propulsion I (Piston Engines & Gas Turbine Basics)", "Fluid Mechanics", "Engineering Maths III (Vector Calculus, Complex Analysis)"], "focus": "Aerodynamics I is the subject that defines aerospace engineering — master it completely.", "tip": "Build a simple aerofoil in OpenFOAM (free CFD software) and validate your Cl vs alpha curve against NACA data. This level of initiative is extremely rare and memorable."},
            {"sem": 4, "label": "Semester 4", "subjects": ["Aerodynamics II (Compressible Flow — Transonic / Supersonic)", "Aircraft Structures II (Thin-Walled Structures, Fatigue)", "Propulsion II (Jet Engines — Turbofan, Turbojet)", "Flight Mechanics I (Static & Dynamic Stability)", "Numerical Methods & Computational Tools"], "focus": "Compressible aerodynamics and jet engine thermodynamics — the two hardest and most important subjects of your degree.", "tip": "Derive the isentropic flow equations yourself. Understanding why M=1 is a critical condition (sonic condition) from first principles is what separates good aerospace engineers from average ones."},
            {"sem": 5, "label": "Semester 5", "subjects": ["Computational Fluid Dynamics (CFD) — Theory & ANSYS Fluent", "Aircraft Structures III (Composite Materials)", "Rocket Propulsion & Spacecraft Systems", "Flight Mechanics II (Performance — Range, Endurance, Climb)", "Mini Project (CFD Analysis / Structural FEA)"], "focus": "CFD is the single most employable skill in aerospace — invest heavily in ANSYS Fluent from Sem 5.", "tip": "Run a complete CFD simulation of a NACA0012 airfoil at multiple angles of attack. Validate against experimental data. Document it properly. This is your first major portfolio piece."},
            {"sem": 6, "label": "Semester 6", "subjects": ["Avionics & Navigation Systems (GPS / INS / Autopilot)", "Spacecraft Mission Design & Orbital Mechanics", "Aircraft Design I (Conceptual Design Methodology)", "Aeroelasticity & Structural Dynamics", "Internship (ISRO / HAL / NAL / DRDO / Aerospace startup)"], "focus": "ISRO / HAL / NAL internship is the most valuable credential in aerospace — apply 6 months in advance.", "tip": "ISRO VSSC and NAL Bangalore take undergraduate interns. Application opens 6 months before. Your Sem 5 CFD project is what gets you shortlisted."},
            {"sem": 7, "label": "Semester 7", "subjects": ["Aircraft Design II (Preliminary & Detail Design)", "Drone / UAV Systems Engineering", "Advanced CFD (Turbulence Models, Multiphase Flow)", "Elective (Hypersonics / Helicopter Aerodynamics / Space Propulsion)", "Major Project Phase 1"], "focus": "UAV / drone systems engineering is the fastest-growing area in Indian aerospace — combine with embedded electronics.", "tip": "Build and fly a fixed-wing drone as your major project. Integrate GPS autopilot (ArduPilot / PX4). This project crosses aerospace + ECE and attracts attention from both ISRO and startups."},
            {"sem": 8, "label": "Semester 8", "subjects": ["Major Project Phase 2", "GATE Preparation / ISRO Scientist Interview Prep", "Aircraft Certification & Airworthiness (DGCA)", "Final Exams"], "focus": "GATE Aerospace (AE) for IIT M.Tech and ISRO / DRDO recruitment — the most important exam for an aerospace engineer.", "tip": "GATE AE syllabus: Aerodynamics (35%) + Structures (25%) + Propulsion (20%) + Flight Mechanics (20%). Aerodynamics alone can make or break your rank."},
        ],
        "parallel_tracks": [
            "💻 CFD: OpenFOAM (free) → ANSYS Fluent (college license) → SU2 (open source, industry-grade) (Sem 3–7)",
            "🚀 Rocketry: Join or start a college rocketry team — Spaceport America Cup (USA) and IROC (India) both accept Indian teams",
            "🛸 Drones: Build a quadcopter (Sem 3) → fixed-wing UAV (Sem 5) → autonomous mission (Sem 7) using ArduPilot / PX4",
            "📐 Structures: CATIA V5 (aircraft-grade CAD) + ABAQUS (composite structure FEA) — both used at HAL and Airbus India",
        ],
    },
}

@app.get("/api/v1/roadmap/{branch_code}")
def get_roadmap(branch_code: str):
    code = branch_code.upper()
    data = ROADMAPS.get(code)
    if not data:
        raise HTTPException(404, f"Roadmap for '{code}' not found")
    return data


# ─────────────────────────────────────────────────────────────────────────────
# Career Tree
# ─────────────────────────────────────────────────────────────────────────────

CAREER_TREES: Dict[str, Dict] = {
    "CSE": {
        "title": "CSE Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",    "skills": ["C / Java / Python basics", "DSA fundamentals", "Mathematics"],      "goal": "Build coding habit, solve easy DSA problems daily"},
            {"label": "Year 3",   "milestone": "Specialise",    "skills": ["OS, DBMS, Networks", "Web Dev / App Dev", "System Design intro"],    "goal": "Build 2 projects, get an internship"},
            {"label": "Year 4",   "milestone": "Placement",     "skills": ["Advanced DSA (LeetCode medium)", "System Design", "Open source"],    "goal": "Crack SDE interviews at product companies"},
            {"label": "0–3 Yrs",  "milestone": "Junior SDE",    "skills": ["Codebase contribution", "Code reviews", "Agile/Scrum"],              "goal": "SDE-1 (6–14 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior SDE",    "skills": ["System architecture", "Team leadership", "Cloud & DevOps"],          "goal": "SDE-2 / Senior Engineer (18–40 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Staff/Principal","skills": ["Cross-team impact", "Technical strategy", "Mentoring"],              "goal": "Staff Engineer / EM / Architect (50–120 LPA)"},
        ],
        "branches_out": ["🎓 MS Abroad → Research Scientist", "🏢 Technical Product Manager", "🚀 Startup Founder / CTO", "🛡️ Cybersecurity Specialist", "☁️ Cloud Architect"],
    },
    "CSE-AIML": {
        "title": "CSE-AIML Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",       "skills": ["Python + NumPy + Pandas", "Linear Algebra & Statistics", "DSA basics"],   "goal": "Kaggle beginner competitions, Python fluency"},
            {"label": "Year 3",   "milestone": "Specialise",       "skills": ["ML (Scikit-learn)", "Deep Learning (PyTorch)", "Data visualisation"],     "goal": "First ML project, Kaggle competition"},
            {"label": "Year 4",   "milestone": "Placement",        "skills": ["NLP / Computer Vision", "MLOps basics", "Research paper reading"],         "goal": "ML Engineer / Data Scientist internship"},
            {"label": "0–3 Yrs",  "milestone": "Junior ML Eng",    "skills": ["Model training pipeline", "Feature engineering", "A/B testing"],           "goal": "ML Engineer / Junior Data Scientist (8–18 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior ML Eng",    "skills": ["MLOps & model serving", "Large-scale pipelines", "Research"],               "goal": "Senior ML Eng / Staff Data Scientist (20–45 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Principal/Research","skills": ["Foundation model training", "AI strategy", "Leadership"],                  "goal": "Research Scientist / AI Lead (60–150 LPA)"},
        ],
        "branches_out": ["🎓 PhD AI/ML → Research Scientist at DeepMind", "🚀 AI Startup Founder", "📊 Head of Data Science", "🤖 Generative AI Engineer", "💡 AI Product Manager"],
    },
    "MECH": {
        "title": "Mechanical Engineering Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",    "skills": ["Engineering Drawing & CAD", "Mechanics & Thermodynamics", "Workshop skills"], "goal": "AutoCAD / SolidWorks basics"},
            {"label": "Year 3",   "milestone": "Specialise",    "skills": ["FEA (ANSYS)", "Manufacturing processes", "MATLAB simulation"],                "goal": "Core sector internship"},
            {"label": "Year 4",   "milestone": "Placement",     "skills": ["SolidWorks / CATIA proficiency", "GATE preparation", "Industry project"],      "goal": "Core job or GATE rank for M.Tech / PSU"},
            {"label": "0–3 Yrs",  "milestone": "GET",           "skills": ["Design software", "Manufacturing standards", "Project execution"],             "goal": "Graduate Engineer Trainee (4–9 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior Eng",    "skills": ["PLM", "Cross-functional lead", "Cost optimisation"],                           "goal": "Senior Engineer / Deputy Manager (12–22 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Manager",       "skills": ["Program management", "Vendor management", "Innovation leadership"],            "goal": "Engineering Manager / Chief Engineer (25–55 LPA)"},
        ],
        "branches_out": ["🎓 M.Tech / MS → Research & Academia", "🏭 Operations / Plant Manager", "🚗 EV Startup", "🛰️ ISRO / DRDO / HAL", "📦 Supply Chain Consulting"],
    },
    "ECE": {
        "title": "Electronics & Communication Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",    "skills": ["Circuit Theory", "Signals & Systems", "Embedded C / Arduino"],                         "goal": "Build circuits, understand analog + digital"},
            {"label": "Year 3",   "milestone": "Specialise",    "skills": ["VLSI / Verilog", "PCB Design", "Communication protocols (SPI/I2C/UART)"],              "goal": "Embedded / VLSI internship, PCB project"},
            {"label": "Year 4",   "milestone": "Placement",     "skills": ["FPGA development", "IoT project portfolio", "GATE prep"],                               "goal": "Core ECE placement or IT sector role"},
            {"label": "0–3 Yrs",  "milestone": "Junior Eng",    "skills": ["Firmware development", "RTOS", "Hardware debugging"],                                   "goal": "Embedded / VLSI Engineer (5–11 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior Hw Eng", "skills": ["SoC design", "RF / mm-wave design", "Silicon validation"],                              "goal": "Senior Engineer at Qualcomm / Intel (14–28 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Principal",     "skills": ["Chip architecture", "Cross-domain leadership", "IP development"],                       "goal": "Principal Engineer / Chip Architect (30–70 LPA)"},
        ],
        "branches_out": ["🎓 M.Tech VLSI / Signal Processing", "🛰️ ISRO / DRDO Space & Defence", "📡 5G Telecom Network Engineer", "💻 IT/Software roles", "🏭 IoT Startup Founder"],
    },

    "CIVIL": {
        "title": "Civil Engineering Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",       "skills": ["Engineering Mechanics", "Engineering Drawing & AutoCAD", "Building Materials"],          "goal": "Learn AutoCAD, understand how structures carry loads"},
            {"label": "Year 3",   "milestone": "Specialise",       "skills": ["Structural Analysis & RCC Design", "Geotechnical Engineering", "STAAD.Pro / ETABS"],     "goal": "Site internship at a construction company or government project"},
            {"label": "Year 4",   "milestone": "Placement / GATE", "skills": ["Construction Management", "Revit BIM", "GATE preparation"],                              "goal": "Core civil job, PSU via GATE, or M.Tech structural engineering"},
            {"label": "0–3 Yrs",  "milestone": "Site / Design Eng","skills": ["RCC detailing", "Site supervision", "Quantity estimation & costing"],                    "goal": "Junior Engineer at L&T / NHAI / PMC (3.5–7 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Project Engineer", "skills": ["Project scheduling (Primavera)", "BIM coordination", "Vendor & contract management"],    "goal": "Project Engineer / Deputy Manager (10–20 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Project Manager",  "skills": ["Programme management", "Cost & risk management", "Client relationship"],                  "goal": "Project / DGM / GM at L&T / Shapoorji / Government (22–50 LPA)"},
        ],
        "branches_out": [
            "🏛️ GATE → IES (Indian Engineering Services) / PWD / NHAI",
            "🏙️ Urban Planner & Smart City Consultant",
            "🎓 M.Tech Structural / Geotechnical → Research & Academia",
            "🌍 MS Abroad (UK / USA / Germany) — Structural / Environmental",
            "🏗️ Construction Startup / Real Estate Developer",
        ],
    },

    "CHEM": {
        "title": "Chemical Engineering Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",        "skills": ["Engineering Chemistry", "Fluid Mechanics", "Thermodynamics & Heat Transfer"],            "goal": "Build strong maths + chemistry fundamentals — tougher than they look"},
            {"label": "Year 3",   "milestone": "Specialise",        "skills": ["Chemical Reaction Engineering", "Mass Transfer", "Process Control & Instrumentation"],    "goal": "Plant visit / internship at a refinery, pharma, or specialty chemical company"},
            {"label": "Year 4",   "milestone": "Placement / GATE",  "skills": ["Aspen HYSYS / Plus simulation", "HAZOP safety analysis", "GATE preparation"],             "goal": "Core process engineering job or GATE rank for M.Tech / PSU (ONGC, HPCL)"},
            {"label": "0–3 Yrs",  "milestone": "Process Engineer",  "skills": ["P&ID reading & plant startup", "Batch / continuous process operation", "Quality control"], "goal": "Graduate Engineer Trainee at Reliance / UPL / Sun Pharma (4–8 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior Process Eng","skills": ["Process optimisation", "HAZOP lead", "Scale-up from lab to plant"],                       "goal": "Senior Engineer / Process Lead (10–22 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Plant Manager",     "skills": ["Operations management", "Safety & compliance", "Capex & budget ownership"],               "goal": "Plant Manager / GM Operations (22–48 LPA)"},
        ],
        "branches_out": [
            "⛽ PSU via GATE → ONGC / HPCL / BPCL / IOCL",
            "💊 Pharmaceutical Process Development (India is the world's pharmacy)",
            "🌿 Green Chemistry & Sustainable Processes",
            "🎓 M.Tech / MS → Petrochemical / Polymer / Pharmaceutical Research",
            "🧪 R&D Scientist at Specialty Chemical / Agrochem company",
        ],
    },

    "BME": {
        "title": "Biomedical Engineering Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",          "skills": ["Human Anatomy & Physiology", "Engineering Physics & Chemistry", "Basic Electronics"],         "goal": "Understand how the human body works as an engineering system"},
            {"label": "Year 3",   "milestone": "Specialise",          "skills": ["Medical Instrumentation", "Biomedical Signal Processing (ECG/EEG)", "Biomaterials"],           "goal": "Hospital internship or medical device company internship — rare and valuable"},
            {"label": "Year 4",   "milestone": "Placement / Higher",  "skills": ["Medical Imaging (MRI / CT / Ultrasound)", "MATLAB biomedical processing", "Regulatory (CDSCO)"],"goal": "Medical device company, hospital clinical engineering, or M.Tech BME"},
            {"label": "0–3 Yrs",  "milestone": "Junior BME",          "skills": ["Device testing & validation", "Clinical documentation", "Biomedical equipment maintenance"],   "goal": "Biomedical Engineer at GE Healthcare / Philips / Medtronic (4–9 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior BME",          "skills": ["Device R&D", "Regulatory submissions (FDA / CDSCO)", "Clinical trials coordination"],           "goal": "Senior Design / R&D Engineer (10–22 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Principal / Manager", "skills": ["Product lifecycle management", "Global regulatory strategy", "Cross-functional leadership"],   "goal": "Principal Engineer / R&D Manager at GE / Siemens / Medtronic (22–50 LPA)"},
        ],
        "branches_out": [
            "🤖 Medical AI Engineer (BME + ML — fastest growing niche in healthcare)",
            "🎓 MS Biomedical Engineering Abroad (USA is the top destination)",
            "🏥 Clinical Engineer at AIIMS / large hospital chain",
            "🧬 PhD Biomedical Sciences → Research & Drug Discovery",
            "🏭 Medical Device Startup (India's PLI scheme is funding this sector)",
        ],
    },

    "AERO": {
        "title": "Aerospace Engineering Career Roadmap",
        "years": [
            {"label": "Year 1–2", "milestone": "Foundation",       "skills": ["Engineering Mechanics & Thermodynamics", "Fluid Mechanics", "Engineering Mathematics"],       "goal": "Master maths — aerospace has the toughest mathematical requirements of any branch"},
            {"label": "Year 3",   "milestone": "Specialise",       "skills": ["Aerodynamics", "Aircraft Structures", "Propulsion (Jet Engines & Rockets)"],                  "goal": "CFD simulation project, apply for ISRO / HAL internship (highly competitive)"},
            {"label": "Year 4",   "milestone": "Placement / GATE", "skills": ["CFD (ANSYS Fluent)", "CATIA aircraft modelling", "Flight mechanics & control systems"],        "goal": "ISRO / HAL / DRDO / aerospace startup placement, or GATE for M.Tech / IIT"},
            {"label": "0–3 Yrs",  "milestone": "Junior Eng",       "skills": ["CFD simulation & post-processing", "Structural FEA for aircraft", "Avionics testing"],         "goal": "Junior Engineer at ISRO / HAL / Airbus India / Tata Advanced Systems (5–12 LPA)"},
            {"label": "3–7 Yrs",  "milestone": "Senior Eng",       "skills": ["Aerodynamic design & optimisation", "Systems integration", "Program management"],              "goal": "Senior / Lead Engineer at HAL / Boeing / Safran (14–28 LPA)"},
            {"label": "7+ Yrs",   "milestone": "Principal / Chief","skills": ["Aircraft / spacecraft system architecture", "R&D leadership", "International standards"],      "goal": "Chief Engineer / Technical Fellow at ISRO / HAL / Boeing India (28–65 LPA)"},
        ],
        "branches_out": [
            "🛰️ ISRO Scientist / Engineer via GATE + Interview (most prestigious AERO destination)",
            "✈️ HAL (Hindustan Aeronautics Limited) — LCA Tejas, helicopters, engines",
            "🚀 Private Space Startups — AgniKul, Skyroot, Pixxel (fast-growing, equity upside)",
            "🎓 MS Aerospace Abroad — TU Munich (Germany), Purdue, Georgia Tech (USA)",
            "🛡️ DRDO Defence Research — missiles, UAVs, radar systems",
        ],
    },
}

@app.get("/api/v1/career-tree/{branch_code}")
def get_career_tree(branch_code: str):
    code = branch_code.upper()
    tree = CAREER_TREES.get(code)
    if not tree:
        raise HTTPException(404, f"Career tree for '{code}' not found")
    return tree


# ─────────────────────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    # Render injects $PORT automatically — never hardcode 8000 in production
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main_final:app", host="0.0.0.0", port=port, reload=False)
