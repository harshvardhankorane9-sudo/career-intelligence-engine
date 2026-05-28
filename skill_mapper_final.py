"""
Skill Mapper — Career Intelligence Engine v3.3
10 questions → 8 skill dimension scores → ranked branch recommendations (8 branches)
Question order: q4 → q5 → q8 → q7 → q2 → q3 → q1 → q6 → q10 → q9
Branches: CSE | CSE-AIML | MECH | ECE | CIVIL | CHEM | BME | AERO
"""

from typing import Dict, List, Any
from datetime import datetime

# ---------------------------------------------------------------------------
# Question definitions
# ---------------------------------------------------------------------------

_Q = {}

_Q["q1"] = {
    "id": "q1",
    "question": "How comfortable are you with writing code / programming?",
    "type": "scale", "min": 1, "max": 10,
    "hint": "1 = Never tried  |  5 = Know the basics  |  10 = Build projects independently",
    "maps": {"coding": 1.0}
}

_Q["q2"] = {
    "id": "q2",
    "question": "How much do you enjoy Mathematics (calculus, algebra, probability)?",
    "type": "scale", "min": 1, "max": 10,
    "hint": "1 = I avoid it  |  10 = I genuinely enjoy solving maths problems",
    "maps": {"mathematics": 1.0}
}

_Q["q3"] = {
    "id": "q3",
    "question": "How comfortable are you with electronics — circuits, breadboards, soldering?",
    "type": "scale", "min": 1, "max": 10,
    "hint": "1 = No experience at all  |  10 = I build circuits from scratch",
    "maps": {"hardware": 1.0}
}

# q4: 8 options — one per branch
_Q["q4"] = {
    "id": "q4",
    "question": "Which of these activities excites you the most?",
    "type": "choice",
    "hint": "Pick the one that genuinely interests you — there is no wrong answer",
    "options": [
        {"value": "software",
         "text": "💻  Building apps, websites, or software systems",
         "maps": {"coding": 3, "analytical": 1}},
        {"value": "aiml",
         "text": "🤖  Training AI models and finding patterns in data",
         "maps": {"coding": 2, "mathematics": 2, "analytical": 2, "research": 1}},
        {"value": "machines",
         "text": "⚙️  Designing mechanical systems, engines, or robots",
         "maps": {"hardware": 2, "creativity": 2, "mathematics": 1}},
        {"value": "circuits",
         "text": "🔌  Designing circuits, embedded systems, or IoT devices",
         "maps": {"hardware": 3, "coding": 1, "mathematics": 1}},
        {"value": "infrastructure",
         "text": "🏗️  Designing buildings, bridges, roads, or city infrastructure",
         "maps": {"communication": 3, "creativity": 2, "mathematics": 1}},
        {"value": "chemical",
         "text": "⚗️  Designing chemical, pharmaceutical, or material processes",
         "maps": {"research": 3, "mathematics": 2}},
        {"value": "medical",
         "text": "🏥  Applying engineering to solve medical and healthcare problems",
         "maps": {"research": 3, "communication": 2, "creativity": 1}},
        {"value": "aerospace",
         "text": "🚀  Designing aircraft, rockets, drones, or spacecraft",
         "maps": {"mathematics": 3, "analytical": 2}},
    ]
}

# q5: 5 options — chemistry and biology split for CHEM vs BME differentiation
_Q["q5"] = {
    "id": "q5",
    "question": "Which subject did you enjoy the most in 11th / 12th standard?",
    "type": "choice",
    "hint": "The one you actually looked forward to studying",
    "options": [
        {"value": "cs",
         "text": "💻  Computer Science / IT",
         "maps": {"coding": 3, "analytical": 1}},
        {"value": "maths",
         "text": "📐  Mathematics / Statistics",
         "maps": {"mathematics": 3, "analytical": 2}},
        {"value": "physics",
         "text": "⚡  Physics (electronics, mechanics, electromagnetism)",
         "maps": {"hardware": 2, "mathematics": 1, "analytical": 1}},
        {"value": "chemistry",
         "text": "🧪  Chemistry / Material Science / Chemical processes",
         "maps": {"research": 2, "mathematics": 1, "analytical": 1}},
        {"value": "biology",
         "text": "🧬  Biology / Life Sciences / Medicine",
         "maps": {"research": 2, "communication": 1, "creativity": 1}},
        {"value": "design",
         "text": "🎨  Design / Engineering Drawing / Workshop / Construction",
         "maps": {"creativity": 3, "communication": 1}},
    ]
}

_Q["q6"] = {
    "id": "q6",
    "question": "Are you interested in research, experiments, and finding patterns in data?",
    "type": "choice",
    "hint": "Think: do experiments, data analysis, or discovering new things excite you?",
    "options": [
        {"value": "yes",
         "text": "Yes — I love experimenting and discovering new things",
         "maps": {"research": 3, "analytical": 2, "mathematics": 1}},
        {"value": "maybe",
         "text": "Somewhat — I can do it but it is not my strongest passion",
         "maps": {"research": 1, "analytical": 1}},
        {"value": "no",
         "text": "Not really — I prefer building or designing physical things",
         "maps": {"creativity": 1, "hardware": 1}},
    ]
}

# q7: 4 options covering all branch work environments
_Q["q7"] = {
    "id": "q7",
    "question": "What kind of work environment appeals to you most?",
    "type": "choice",
    "hint": "Think about where you would genuinely enjoy spending your working day",
    "options": [
        {"value": "software",
         "text": "💻  Office / remote — writing code, analysing data, solving logic problems",
         "maps": {"coding": 2}},
        {"value": "hardware",
         "text": "🔧  Lab / workshop — building, testing, and debugging physical things",
         "maps": {"hardware": 2, "creativity": 1}},
        {"value": "field",
         "text": "🏗️  Field / site / plant — large-scale construction, infrastructure, or industrial facilities",
         "maps": {"communication": 3, "creativity": 1}},
        {"value": "clinical",
         "text": "🏥  Hospital / clinic / research lab — working with medical teams and patients",
         "maps": {"research": 2, "communication": 3}},
    ]
}

_Q["q8"] = {
    "id": "q8",
    "question": "How strong is your logical / analytical problem-solving ability?",
    "type": "scale", "min": 1, "max": 10,
    "hint": "Think: puzzles, maths, debugging, or process troubleshooting — how natural does this feel?",
    "maps": {"analytical": 1.0}
}

_Q["q9"] = {
    "id": "q9",
    "question": "After B.E., would you prefer higher studies, industry, or government / PSU?",
    "type": "choice",
    "hint": "Honest answer — all are valid and respected paths",
    "options": [
        {"value": "research",
         "text": "🎓  Higher studies / research — M.Tech, MS, or PhD",
         "maps": {"research": 3}},
        {"value": "industry",
         "text": "🏢  Private industry right away — product company, startup, or MNC",
         "maps": {"coding": 1, "entrepreneurship": 1}},
        {"value": "startup",
         "text": "🚀  Start my own company or build my own product",
         "maps": {"entrepreneurship": 3, "creativity": 2}},
        {"value": "government",
         "text": "🏛️  Government / PSU — ISRO, DRDO, ONGC, PWD, NHAI, MSEDCL",
         "maps": {"mathematics": 1, "research": 1, "communication": 1}},
        {"value": "unsure",
         "text": "🤷  Not sure yet — keeping all options open",
         "maps": {"research": 1}},
    ]
}

_Q["q10"] = {
    "id": "q10",
    "question": "What is your primary goal for choosing an engineering branch?",
    "type": "choice",
    "hint": "Be honest — all goals are completely valid",
    "options": [
        {"value": "salary",
         "text": "💰  Highest salary and long-term job security",
         "maps": {"coding": 1, "analytical": 1}},
        {"value": "passion",
         "text": "❤️  Work I am genuinely passionate about every day",
         "maps": {"creativity": 1, "research": 1}},
        {"value": "impact",
         "text": "🌍  Real-world impact — infrastructure, healthcare, or environment",
         "maps": {"research": 1, "entrepreneurship": 1, "communication": 1}},
        {"value": "abroad",
         "text": "✈️  MS / PhD abroad and build a global career",
         "maps": {"research": 2, "mathematics": 1}},
    ]
}

# ---------------------------------------------------------------------------
# QUESTION ORDER
# ---------------------------------------------------------------------------
QUESTIONS: List[Dict] = [
    _Q["q4"],   # 1. What excites you most?         (broad interest — best opener)
    _Q["q5"],   # 2. Favourite 12th subject?         (school background signal)
    _Q["q8"],   # 3. Analytical ability?             (logical scale)
    _Q["q7"],   # 4. Work environment?               (environment preference)
    _Q["q2"],   # 5. Enjoy maths?                    (maths scale)
    _Q["q3"],   # 6. Electronics comfort?            (hardware scale)
    _Q["q1"],   # 7. Coding comfort?                 (coding scale)
    _Q["q6"],   # 8. Research interest?              (research aptitude)
    _Q["q10"],  # 9. Primary career goal?            (motivation)
    _Q["q9"],   # 10. Higher studies or industry?    (future path — natural closer)
]

# ---------------------------------------------------------------------------
# Branch profiles — 8 dimensions × 8 branches
# Each weight reflects how critical that skill is for the branch
# ---------------------------------------------------------------------------

BRANCH_PROFILES = {
    # Unique signal: highest coding (0.95)
    "CSE": {
        "coding": 0.95, "mathematics": 0.70, "analytical": 0.85,
        "hardware": 0.20, "creativity": 0.60, "research": 0.50,
        "communication": 0.55, "entrepreneurship": 0.60
    },
    # Unique signal: highest analytical (0.95), very high maths + coding
    "CSE-AIML": {
        "coding": 0.90, "mathematics": 0.92, "analytical": 0.95,
        "hardware": 0.15, "creativity": 0.65, "research": 0.72,
        "communication": 0.55, "entrepreneurship": 0.55
    },
    # Unique signal: highest creativity (0.85), highest hardware after ECE
    "MECH": {
        "coding": 0.38, "mathematics": 0.80, "analytical": 0.75,
        "hardware": 0.85, "creativity": 0.85, "research": 0.55,
        "communication": 0.62, "entrepreneurship": 0.58
    },
    # Unique signal: highest hardware (0.95)
    "ECE": {
        "coding": 0.65, "mathematics": 0.80, "analytical": 0.80,
        "hardware": 0.95, "creativity": 0.55, "research": 0.60,
        "communication": 0.55, "entrepreneurship": 0.45
    },
    # Unique signal: highest communication (0.90), highest entrepreneurship (0.68)
    "CIVIL": {
        "coding": 0.15, "mathematics": 0.82, "analytical": 0.78,
        "hardware": 0.65, "creativity": 0.80, "research": 0.50,
        "communication": 0.90, "entrepreneurship": 0.68
    },
    # Unique signal: very high maths (0.92) + high research (0.85), very low coding (0.18)
    "CHEM": {
        "coding": 0.18, "mathematics": 0.92, "analytical": 0.82,
        "hardware": 0.60, "creativity": 0.58, "research": 0.85,
        "communication": 0.68, "entrepreneurship": 0.45
    },
    # Unique signal: highest research (0.93), high communication (0.82), lowest maths (0.62)
    "BME": {
        "coding": 0.55, "mathematics": 0.62, "analytical": 0.78,
        "hardware": 0.72, "creativity": 0.76, "research": 0.93,
        "communication": 0.82, "entrepreneurship": 0.52
    },
    # Unique signal: highest maths (0.95), highest analytical after AIML (0.92)
    "AERO": {
        "coding": 0.52, "mathematics": 0.95, "analytical": 0.92,
        "hardware": 0.82, "creativity": 0.68, "research": 0.80,
        "communication": 0.58, "entrepreneurship": 0.42
    },
}

BRANCH_NAMES = {
    "CSE":      "Computer Science & Engineering",
    "CSE-AIML": "CSE with AI & Machine Learning",
    "MECH":     "Mechanical Engineering",
    "ECE":      "Electronics & Communication Engineering",
    "CIVIL":    "Civil Engineering",
    "CHEM":     "Chemical Engineering",
    "BME":      "Biomedical Engineering",
    "AERO":     "Aerospace Engineering",
}

# ---------------------------------------------------------------------------
# SkillMapper
# ---------------------------------------------------------------------------

class SkillMapper:
    def get_questions(self) -> List[Dict]:
        return QUESTIONS

    def calculate_scores(self, answers: Dict[str, Any]) -> Dict[str, float]:
        scores = {d: 0.0 for d in
                  ["coding","mathematics","analytical","hardware",
                   "creativity","research","communication","entrepreneurship"]}
        for q in QUESTIONS:
            answer = answers.get(q["id"])
            if answer is None:
                continue
            if q["type"] == "scale":
                val = float(answer)
                for dim, w in q["maps"].items():
                    scores[dim] += val * w
            elif q["type"] == "choice":
                for opt in q["options"]:
                    if opt["value"] == answer:
                        for dim, pts in opt["maps"].items():
                            scores[dim] += pts
                        break
        for d in scores:
            scores[d] = round(min(10.0, max(0.0, scores[d])), 2)
        return scores

    def rank_branches(self, scores: Dict[str, float]) -> List[Dict]:
        results = []
        for code, weights in BRANCH_PROFILES.items():
            total = sum(scores.get(d, 0.0) * w for d, w in weights.items())
            max_p = sum(10.0 * w for w in weights.values())
            pct   = round(total / max_p * 100, 1) if max_p else 0
            results.append({
                "code":        code,
                "name":        BRANCH_NAMES[code],
                "match_pct":   pct,
                "explanation": self._explain(code, scores, pct)
            })
        results.sort(key=lambda x: x["match_pct"], reverse=True)
        return results

    def _explain(self, code: str, scores: Dict[str, float], pct: float) -> str:
        weights   = BRANCH_PROFILES[code]
        top_dims  = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:2]
        strengths = [d for d, w in top_dims if scores.get(d, 0) >= 6]
        label     = ("Excellent" if pct >= 75 else "Good" if pct >= 60
                     else "Moderate" if pct >= 45 else "Low")
        text = f"{label} match ({pct:.1f}%). "
        if strengths:
            text += (f"Your strength in "
                     f"{' & '.join(d.replace('_',' ') for d in strengths)} aligns well. ")
        else:
            text += "Building core skills in this area will be important. "
        advice = {
            "CSE":      "Focus on DSA and system design to excel.",
            "CSE-AIML": "Strong maths + Python are your keys to success.",
            "MECH":     "CAD skills and core sector internships help a lot.",
            "ECE":      "Hands-on embedded labs and FPGA projects set you apart.",
            "CIVIL":    "STAAD.Pro + site internship is what core recruiters want.",
            "CHEM":     "Process simulation (Aspen HYSYS) and plant internship are critical.",
            "BME":      "A medical device prototype + hospital internship opens all doors.",
            "AERO":     "Strong maths + CFD portfolio is your path to ISRO and HAL.",
        }
        text += advice.get(code, "")
        return text


# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------

def run_assessment(answers: Dict[str, Any]) -> Dict[str, Any]:
    mapper       = SkillMapper()
    skill_scores = mapper.calculate_scores(answers)
    ranked       = mapper.rank_branches(skill_scores)
    confidence   = min(1.0, ranked[0]["match_pct"] / 100 + 0.05) if ranked else 0.5
    return {
        "skill_scores":         skill_scores,
        "recommended_branches": ranked,
        "confidence":           round(confidence, 3),
        "timestamp":            datetime.now().isoformat()
    }


# ---------------------------------------------------------------------------
# Smoke tests — one clear profile per new branch
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Question order:")
    for i, q in enumerate(QUESTIONS, 1):
        print(f"  {i}. [{q['id']}] {q['question'][:65]}...")

    tests = {
        "CIVIL (loves infrastructure, site work, low coding)": {
            "q4": "infrastructure", "q5": "design",   "q8": 6,
            "q7": "field",          "q2": 7,           "q3": 3,
            "q1": 2,                "q6": "no",        "q10": "impact",
            "q9": "government"
        },
        "CHEM (loves chemistry, plant work, high maths)": {
            "q4": "chemical",       "q5": "chemistry", "q8": 8,
            "q7": "field",          "q2": 9,           "q3": 3,
            "q1": 3,                "q6": "yes",       "q10": "passion",
            "q9": "government"
        },
        "BME (loves medicine, biology, clinical work)": {
            "q4": "medical",        "q5": "biology",   "q8": 6,
            "q7": "clinical",       "q2": 5,           "q3": 5,
            "q1": 5,                "q6": "yes",       "q10": "impact",
            "q9": "research"
        },
        "AERO (loves rockets, very high maths, aerospace)": {
            "q4": "aerospace",      "q5": "physics",   "q8": 9,
            "q7": "hardware",       "q2": 9,           "q3": 6,
            "q1": 5,                "q6": "yes",       "q10": "abroad",
            "q9": "research"
        },
    }

    for label, answers in tests.items():
        print(f"\n--- {label} ---")
        r = run_assessment(answers)
        for b in r["recommended_branches"]:
            marker = " ◄" if b["code"] == label.split()[0] else ""
            print(f"  {b['code']:12} {b['match_pct']:5.1f}%{marker}")

    print("\n✅ skill_mapper.py OK — 8 branches, 10 questions")
