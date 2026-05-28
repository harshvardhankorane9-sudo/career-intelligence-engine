"""
RAG Engine — Career Intelligence Engine
Built-in knowledge base about CSE | CSE-AIML | Mechanical | Electronics.
Keyword + TF-IDF style retrieval. No external API required for basic Q&A.
Optional: set GEMINI_API_KEY in .env for richer LLM-generated answers.
"""

import os
import re
import json
import math
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter

# ---------------------------------------------------------------------------
# Built-in knowledge base
# ---------------------------------------------------------------------------

KNOWLEDGE_BASE = [
    # ---- CSE ---------------------------------------------------------------
    {
        "id": "cse_overview",
        "text": (
            "Computer Science & Engineering (CSE) is the study of computation, programming, "
            "algorithms, data structures, operating systems, computer networks, and software engineering. "
            "It is the broadest and most versatile engineering discipline in the IT sector. "
            "CSE graduates build software applications, design databases, develop cloud infrastructure, "
            "and create everything from mobile apps to enterprise systems."
        ),
        "tags": ["cse", "computer science", "overview", "software"]
    },
    {
        "id": "cse_salary",
        "text": (
            "CSE salary in India: Entry level (0-3 years) 6-14 LPA at product companies, 3-6 LPA at service companies. "
            "Mid level (3-7 years) 18-40 LPA. Senior level (7+ years) 50-120 LPA. "
            "Top MNC packages (Google, Microsoft, Meta) range from 1 to 3 crore annually at senior positions. "
            "CSE offers the highest average salary among all engineering branches in India."
        ),
        "tags": ["cse", "salary", "package", "lpa", "placement"]
    },
    {
        "id": "cse_subjects",
        "text": (
            "Key subjects in CSE B.E./B.Tech: Data Structures and Algorithms (DSA), Operating Systems (OS), "
            "Database Management Systems (DBMS), Computer Networks, Software Engineering, "
            "Theory of Computation, Compiler Design, Object Oriented Programming, Web Technologies, "
            "Discrete Mathematics, and Computer Organisation and Architecture. "
            "DSA is the most important subject for placement preparation."
        ),
        "tags": ["cse", "subjects", "syllabus", "curriculum", "dsa"]
    },
    {
        "id": "cse_careers",
        "text": (
            "Career paths in CSE: Software Development Engineer (SDE) at product companies, "
            "Backend / Frontend / Full-Stack Developer, DevOps and Cloud Engineer, "
            "Cybersecurity Analyst, Database Administrator, Technical Product Manager. "
            "Top recruiters: Google, Microsoft, Amazon, Adobe, Flipkart, Atlassian, Zomato, Swiggy, "
            "Infosys, TCS, Wipro, Cognizant. CSE graduates are hired across all industries."
        ),
        "tags": ["cse", "career", "jobs", "recruiters", "placement"]
    },
    {
        "id": "cse_higher_studies",
        "text": (
            "Higher studies after CSE: M.Tech in Computer Science, MS abroad (USA, Germany, Canada, UK), "
            "MBA in Technology Management, PhD in Computer Science. "
            "Top colleges for MS: MIT, Stanford, CMU, UC Berkeley, Georgia Tech, UIUC. "
            "GATE exam is required for M.Tech at IITs and NITs. GRE is required for MS abroad. "
            "CSE students have very high acceptance rates in top global universities."
        ),
        "tags": ["cse", "ms", "mtech", "higher studies", "gate", "gre", "abroad"]
    },

    # ---- CSE-AIML ----------------------------------------------------------
    {
        "id": "aiml_overview",
        "text": (
            "CSE with AI & Machine Learning (CSE-AIML) is a specialised branch that combines core "
            "computer science with artificial intelligence, machine learning, deep learning, "
            "natural language processing (NLP), and computer vision. "
            "Students build intelligent systems that learn from data — recommendation engines, "
            "language models, image classifiers, and autonomous systems."
        ),
        "tags": ["aiml", "cse aiml", "machine learning", "deep learning", "ai", "overview"]
    },
    {
        "id": "aiml_salary",
        "text": (
            "AI/ML engineer salary in India: Entry level 8-18 LPA, mid level 20-45 LPA, "
            "senior level 60-150 LPA. AI is the highest-paying tech specialisation globally. "
            "AI Research Scientists at top companies earn 2-5 crore+ annually. "
            "The demand for ML engineers is growing 40% year-on-year, making it the fastest-growing "
            "tech job category. India has a 4X more demand than supply for ML engineers."
        ),
        "tags": ["aiml", "salary", "package", "lpa", "placement", "machine learning"]
    },
    {
        "id": "aiml_subjects",
        "text": (
            "Key subjects in CSE-AIML: Machine Learning (supervised, unsupervised, reinforcement), "
            "Deep Learning (CNNs, RNNs, Transformers), Natural Language Processing (NLP), "
            "Computer Vision, Data Science and Analytics, Big Data Engineering, "
            "Probability and Statistics, Python Programming, and all CSE core subjects. "
            "Important frameworks: TensorFlow, PyTorch, Scikit-learn, Keras, Hugging Face."
        ),
        "tags": ["aiml", "subjects", "syllabus", "machine learning", "python", "pytorch"]
    },
    {
        "id": "aiml_careers",
        "text": (
            "Career paths in CSE-AIML: Machine Learning Engineer, Data Scientist, "
            "AI Research Scientist, NLP Engineer, Computer Vision Engineer, "
            "MLOps/AI Platform Engineer, Generative AI Engineer, Data Engineer. "
            "Top recruiters: Google DeepMind, OpenAI, Microsoft AI, Meta AI, Amazon, NVIDIA, "
            "Anthropic, Zomato, PhonePe, Meesho, Fractal Analytics, Mu Sigma."
        ),
        "tags": ["aiml", "career", "jobs", "data scientist", "ml engineer", "placement"]
    },
    {
        "id": "aiml_vs_cse",
        "text": (
            "Difference between CSE and CSE-AIML: CSE is broader — covers all aspects of software engineering. "
            "CSE-AIML is more focused on data-driven intelligent systems. "
            "CSE is better for SDE roles, DevOps, and system design. "
            "CSE-AIML is better for ML Engineer, Data Scientist, and AI researcher roles. "
            "Both branches have similar core subjects in the first two years. "
            "Students who love mathematics and statistics prefer CSE-AIML."
        ),
        "tags": ["aiml", "cse", "difference", "comparison", "which is better"]
    },

    # ---- Mechanical --------------------------------------------------------
    {
        "id": "mech_overview",
        "text": (
            "Mechanical Engineering (MECH) is one of the oldest and broadest engineering disciplines. "
            "It covers thermodynamics, fluid mechanics, solid mechanics, manufacturing processes, "
            "material science, robotics, and CAD/CAM. Mechanical engineers design and build "
            "physical systems — from engines and turbines to robots and spacecraft."
        ),
        "tags": ["mechanical", "mech", "overview", "engineering"]
    },
    {
        "id": "mech_salary",
        "text": (
            "Mechanical engineering salary in India: Entry level 4-9 LPA (core sector), "
            "mid level 12-22 LPA, senior level 25-55 LPA. "
            "Government sector (ISRO, DRDO, PSUs like BHEL) offers 7-12 LPA with great job security. "
            "Mechanical engineers who cross-skill into programming, simulation (FEA/CFD), "
            "or automation command significantly higher salaries. "
            "In automotive (Tata Motors, Mahindra), HVAC, and aerospace, senior engineers earn 30-60 LPA."
        ),
        "tags": ["mechanical", "mech", "salary", "package", "placement"]
    },
    {
        "id": "mech_subjects",
        "text": (
            "Key subjects in Mechanical Engineering: Engineering Mechanics (Statics & Dynamics), "
            "Thermodynamics, Fluid Mechanics, Strength of Materials, Manufacturing Processes, "
            "Theory of Machines, Heat Transfer, Refrigeration & Air Conditioning, "
            "CAD/CAM, Robotics, Industrial Engineering, and Material Science. "
            "Important software: AutoCAD, SolidWorks, CATIA, ANSYS, MATLAB, Abaqus."
        ),
        "tags": ["mechanical", "subjects", "syllabus", "cad", "thermodynamics"]
    },
    {
        "id": "mech_careers",
        "text": (
            "Career paths in Mechanical Engineering: Design Engineer, Manufacturing Engineer, "
            "Automotive Engineer, Aerospace Engineer, Robotics & Automation Engineer, "
            "HVAC Engineer, Thermal Systems Engineer, Production Manager, R&D Scientist. "
            "Top recruiters: Tata Motors, Mahindra, L&T, ISRO, DRDO, Bosch, Cummins India, "
            "Siemens, John Deere, Eaton, Thermax, Godrej. PSU recruitment via GATE."
        ),
        "tags": ["mechanical", "career", "jobs", "recruiters", "automotive", "isro"]
    },
    {
        "id": "mech_future",
        "text": (
            "Future scope of Mechanical Engineering: EV (Electric Vehicle) revolution is creating "
            "massive demand for mechanical engineers skilled in battery thermal management, "
            "lightweight materials, and powertrain design. "
            "Industry 4.0 and smart manufacturing require mechatronics knowledge. "
            "Additive manufacturing (3D printing) is transforming prototyping. "
            "Defense modernisation (DRDO, HAL) and space sector (ISRO, private space startups) "
            "are growing rapidly in India."
        ),
        "tags": ["mechanical", "future", "ev", "robotics", "industry 4.0", "scope"]
    },

    # ---- ECE ---------------------------------------------------------------
    {
        "id": "ece_overview",
        "text": (
            "Electronics & Communication Engineering (ECE) covers analog electronics, digital electronics, "
            "signal processing, communication systems, embedded systems, VLSI design, "
            "antenna theory, RF engineering, and control systems. "
            "ECE engineers design chips, build wireless communication systems, "
            "create IoT devices, and work on 5G, satellite, and radar systems."
        ),
        "tags": ["ece", "electronics", "communication", "overview", "embedded"]
    },
    {
        "id": "ece_salary",
        "text": (
            "ECE salary in India: Entry level 5-11 LPA at semiconductor and telecom companies, "
            "mid level 14-28 LPA, senior level 30-70 LPA. "
            "VLSI engineers are the highest-paid hardware professionals — "
            "senior chip designers at Intel, Qualcomm, NVIDIA earn 50-150 LPA. "
            "Government sector: ISRO, DRDO, BEL offer 6-12 LPA with stability. "
            "ECE graduates entering software roles earn similar to CSE graduates."
        ),
        "tags": ["ece", "electronics", "salary", "package", "vlsi", "placement"]
    },
    {
        "id": "ece_subjects",
        "text": (
            "Key subjects in ECE: Analog Electronics, Digital Electronics, Signals and Systems, "
            "Digital Signal Processing (DSP), Communication Systems (analog + digital), "
            "Microprocessors and Microcontrollers, Embedded Systems, VLSI Design (Verilog/VHDL), "
            "Antenna Theory, RF Engineering, Control Systems, and Electromagnetic Theory. "
            "Important tools: MATLAB, Simulink, Keil, Arduino, Raspberry Pi, Cadence, Xilinx Vivado."
        ),
        "tags": ["ece", "subjects", "syllabus", "vlsi", "embedded", "signal processing"]
    },
    {
        "id": "ece_careers",
        "text": (
            "Career paths in ECE: Embedded Systems Engineer, VLSI/Chip Design Engineer, "
            "RF/Communication Engineer, IoT Solutions Architect, Signal Processing Engineer, "
            "Telecom Network Engineer, Hardware Design Engineer, Satellite Systems Engineer. "
            "Top recruiters: Intel, Qualcomm, Texas Instruments, Samsung Semiconductor, "
            "STMicroelectronics, NXP, MediaTek, ISRO, DRDO, Airtel, Jio. "
            "ECE graduates also enter IT sector (Infosys, TCS) and banking sector."
        ),
        "tags": ["ece", "career", "jobs", "vlsi", "embedded", "isro", "qualcomm"]
    },
    {
        "id": "ece_iot_5g",
        "text": (
            "ECE and the 5G/IoT revolution: India's Semiconductor Mission and 5G rollout "
            "are creating unprecedented demand for ECE professionals. "
            "The IoT market is expected to reach $1 trillion globally by 2030, "
            "with billions of connected devices needing embedded engineers to design them. "
            "VLSI demand is exploding as India aims to produce its own chips domestically. "
            "Companies like Tata Electronics, Foxconn, and Apple suppliers are building chip plants in India."
        ),
        "tags": ["ece", "5g", "iot", "vlsi", "semiconductor", "future", "scope"]
    },


    # ---- CIVIL ---------------------------------------------------------------
    {
        "id": "civil_overview",
        "text": (
            "Civil Engineering designs and builds infrastructure — roads, bridges, dams, buildings, "
            "water supply networks, drainage systems, and smart cities. It is the oldest engineering "
            "discipline and has the most direct visible impact on society. In India, massive "
            "infrastructure spending under the National Infrastructure Pipeline (NIP) is creating "
            "unprecedented demand for civil engineers."
        ),
        "tags": ["civil", "infrastructure", "overview", "construction"]
    },
    {
        "id": "civil_salary",
        "text": (
            "Civil engineering salary in India: Fresher at L&T or government: ₹3.5–7 LPA. "
            "Mid level (5–8 years): ₹12–22 LPA. Senior project manager (12+ years): ₹30–60 LPA. "
            "Government engineers (PWD, NHAI, MSRDC) earn ₹6–10 LPA with excellent job security and benefits. "
            "GATE score is essential for PSU jobs (NHAI, RVNL, CPWD) and IES (Indian Engineering Services)."
        ),
        "tags": ["civil", "salary", "package", "lpa", "placement", "government"]
    },
    {
        "id": "civil_careers",
        "text": (
            "Career paths in Civil Engineering: Structural Design Engineer, Site/Project Engineer, "
            "Transportation and Highway Engineer, Geotechnical Engineer, Urban Planner, "
            "Government Engineer (PWD/NHAI/Municipal Corporation). "
            "Top recruiters: L&T Construction, Shapoorji Pallonji, Afcons, NHAI, NMRC/Metro Rail, "
            "Pune Municipal Corporation, MSRDC. GATE is the primary route for PSU and government jobs."
        ),
        "tags": ["civil", "career", "jobs", "recruiters", "government", "placement"]
    },
    {
        "id": "civil_future",
        "text": (
            "Future scope of Civil Engineering: India's National Infrastructure Pipeline targets "
            "₹111 lakh crore investment in roads, railways, airports, and smart cities. "
            "Pune Metro Phase 2, Mumbai coastal road, and Navi Mumbai airport are active projects. "
            "BIM (Building Information Modelling) and smart city planning are premium skills. "
            "Civil engineers who learn AutoCAD, STAAD.Pro, and ETABS have the best placement outcomes."
        ),
        "tags": ["civil", "future", "scope", "infrastructure", "smart city"]
    },

    # ---- CHEM ---------------------------------------------------------------
    {
        "id": "chem_overview",
        "text": (
            "Chemical Engineering designs industrial processes to convert raw materials into useful products — "
            "fuels, medicines, plastics, fertilizers, and specialty chemicals. "
            "Chemical engineers work in refineries, pharmaceutical plants, fertilizer factories, "
            "water treatment facilities, and specialty chemical companies. "
            "India's pharmaceutical and specialty chemicals sectors are among the fastest-growing globally."
        ),
        "tags": ["chemical", "chem", "overview", "process engineering"]
    },
    {
        "id": "chem_salary",
        "text": (
            "Chemical engineering salary in India: Fresher at Reliance/UPL/Sun Pharma: ₹4–8 LPA. "
            "Mid level (5–8 years): ₹12–25 LPA. Senior/plant manager: ₹25–50 LPA. "
            "PSU via GATE (ONGC, HPCL, BPCL, IOCL): ₹8–12 LPA with excellent benefits and job security. "
            "Chemical engineers with process simulation skills (Aspen HYSYS) earn significant premiums."
        ),
        "tags": ["chemical", "chem", "salary", "package", "placement", "psu"]
    },
    {
        "id": "chem_careers",
        "text": (
            "Career paths in Chemical Engineering: Process Engineer, Production Engineer, "
            "R&D/Process Development Engineer, Environmental/Safety Engineer, Quality Engineer, "
            "Petroleum/Refinery Engineer. "
            "Top recruiters: Reliance Industries, ONGC, HPCL, BPCL, UPL Pune, Thermax Pune, "
            "Sun Pharma, Dr Reddy's, BASF India, Asian Paints, Pidilite. "
            "GATE opens PSU doors — ONGC, HPCL, BPCL, IOCL all hire chemical engineers."
        ),
        "tags": ["chemical", "chem", "career", "jobs", "pharma", "refinery", "placement"]
    },
    {
        "id": "chem_future",
        "text": (
            "Future scope of Chemical Engineering: India's specialty chemicals market grows at 12% annually "
            "driven by global supply chain shifts from China. "
            "India is the world's pharmacy — pharmaceutical manufacturing employs thousands of chemical engineers. "
            "Green chemistry, bio-based materials, and green hydrogen are emerging high-growth areas. "
            "Pune's pharmaceutical cluster (Bhosari, Pimpri-Chinchwad) and Pune MIDC are major employers."
        ),
        "tags": ["chemical", "chem", "future", "scope", "pharma", "specialty chemicals"]
    },

    # ---- BME ---------------------------------------------------------------
    {
        "id": "bme_overview",
        "text": (
            "Biomedical Engineering combines engineering with medicine to design medical devices, "
            "diagnostic equipment, prosthetics, and healthcare information systems. "
            "BME engineers work at companies like GE Healthcare, Philips, Siemens Healthineers, "
            "Medtronic, and Stryker, as well as in hospitals and medical AI startups. "
            "India's medical device market is projected to reach $50 billion by 2030."
        ),
        "tags": ["bme", "biomedical", "medical devices", "overview", "healthcare"]
    },
    {
        "id": "bme_salary",
        "text": (
            "Biomedical engineering salary in India: Fresher at GE Healthcare/Philips/Medtronic: ₹4–9 LPA. "
            "Mid level (5–7 years): ₹12–25 LPA. Senior R&D engineer: ₹22–45 LPA. "
            "Medical AI engineers combining BME and ML: ₹20–50 LPA — the fastest growing niche. "
            "MS abroad (USA) is a very strong path — top universities include Johns Hopkins, Duke, and Northwestern."
        ),
        "tags": ["bme", "biomedical", "salary", "package", "placement", "medical ai"]
    },
    {
        "id": "bme_careers",
        "text": (
            "Career paths in Biomedical Engineering: Medical Device Design Engineer, "
            "Biomedical/Clinical Engineer (Hospital), Medical Imaging Specialist, "
            "Regulatory Affairs Engineer, Biomedical Data Scientist, Prosthetics Engineer. "
            "Top recruiters: Philips Healthcare, GE Healthcare, Siemens Healthineers, Medtronic, "
            "Stryker, Trivitron Healthcare, Skanray Technologies, Wipro GE Healthcare."
        ),
        "tags": ["bme", "biomedical", "career", "jobs", "medical devices", "placement"]
    },
    {
        "id": "bme_future",
        "text": (
            "Future scope of Biomedical Engineering: India's PLI scheme for medical devices "
            "is attracting global manufacturers to produce in India. "
            "AI-based medical imaging — cancer detection, radiology AI, pathology AI — "
            "is the fastest-growing BME niche combining biomedical knowledge with machine learning. "
            "Wearable health monitors, point-of-care diagnostics for rural India, "
            "and affordable prosthetics are high-impact areas unique to Indian BME."
        ),
        "tags": ["bme", "biomedical", "future", "scope", "medical ai", "wearable"]
    },

    # ---- AERO ---------------------------------------------------------------
    {
        "id": "aero_overview",
        "text": (
            "Aerospace Engineering covers the design, development, and testing of aircraft, "
            "helicopters, rockets, satellites, drones, and space vehicles. "
            "It combines aerodynamics, structural analysis, propulsion, avionics, and control systems. "
            "India's space economy is booming — ISRO, private space startups (AgniKul, Skyroot, Pixxel), "
            "and defence modernisation (Tejas, AMCA) are creating significant aerospace demand."
        ),
        "tags": ["aerospace", "aero", "overview", "isro", "rockets", "aircraft"]
    },
    {
        "id": "aero_salary",
        "text": (
            "Aerospace engineering salary in India: Fresher at ISRO/HAL: ₹5–8 LPA with excellent benefits. "
            "Private space startup: ₹8–15 LPA with equity potential. "
            "Senior engineer after 7 years: ₹18–35 LPA. "
            "International positions at Airbus/Boeing/SpaceX: ₹40–120 LPA. "
            "GATE Aerospace (AE) is the primary route to ISRO, HAL, NAL, and DRDO."
        ),
        "tags": ["aerospace", "aero", "salary", "package", "isro", "placement"]
    },
    {
        "id": "aero_careers",
        "text": (
            "Career paths in Aerospace Engineering: Aerodynamics/CFD Engineer, "
            "Aircraft Structural Design Engineer, Propulsion Engineer, "
            "Avionics/Flight Systems Engineer, Spacecraft Engineer, Drone/UAV Engineer. "
            "Top recruiters: ISRO, HAL, DRDO (ADE/GTRE), NAL, Mahindra Defence, "
            "Tata Advanced Systems, Safran India, Boeing India, Airbus India, "
            "AgniKul Cosmos, Skyroot Aerospace (private space startups)."
        ),
        "tags": ["aerospace", "aero", "career", "isro", "hal", "drdo", "placement"]
    },
    {
        "id": "aero_future",
        "text": (
            "Future scope of Aerospace Engineering: India's space economy targets $44 billion by 2033. "
            "IN-SPACe policy opened private space — AgniKul, Skyroot, Pixxel all hiring aerospace engineers. "
            "Defence indigenisation — LCA Tejas Mk2, AMCA stealth fighter, DRDO missiles — "
            "and drone manufacturing PLI scheme are creating 50,000+ aerospace jobs. "
            "GATE AE is critical: Aerodynamics (35%) + Structures (25%) + Propulsion (20%) weightage."
        ),
        "tags": ["aerospace", "aero", "future", "scope", "space", "defence", "drone"]
    },

    # ---- General / comparison ---------------------------------------------
    {
        "id": "which_branch",
        "text": (
            "Choosing the right engineering branch depends on your interests and strengths. "
            "Choose CSE for software, apps, and cloud systems. "
            "Choose CSE-AIML for machine learning, data science, and AI research. "
            "Choose Mechanical for physical systems, engines, manufacturing, and EVs. "
            "Choose ECE for circuits, embedded systems, VLSI, and wireless communication. "
            "Choose Civil if you want to build infrastructure — roads, bridges, buildings, smart cities. "
            "Choose Chemical if chemistry and industrial processes interest you — pharma, refinery, specialty chemicals. "
            "Choose Biomedical if you want to combine engineering with medicine and healthcare technology. "
            "Choose Aerospace if you dream of rockets, aircraft, satellites, and working at ISRO or HAL. "
            "The best branch matches your genuine interests, not just salary expectations."
        ),
        "tags": ["comparison", "which branch", "choose", "all branches", "cse vs ece", "civil vs cse"]
    },
    {
        "id": "gate_exam",
        "text": (
            "GATE (Graduate Aptitude Test in Engineering) is the key exam for M.Tech admission "
            "at IITs, NITs, and PSU jobs. "
            "CSE GATE syllabus: Algorithms, Data Structures, OS, DBMS, Computer Networks, TOC, Discrete Math. "
            "ECE GATE syllabus: Analog/Digital Circuits, Signals, Communication, Control Systems. "
            "Mechanical GATE syllabus: Thermodynamics, Fluid Mechanics, Strength of Materials, Manufacturing. "
            "GATE score is also used by PSUs like BHEL, NTPC, ONGC, ISRO, DRDO for direct hiring."
        ),
        "tags": ["gate", "mtech", "psu", "exam", "preparation"]
    },
    {
        "id": "placement_tips",
        "text": (
            "Placement preparation tips: "
            "CSE/CSE-AIML: Focus on DSA (LeetCode, Codeforces), system design, and one full-stack project. "
            "ECE: Learn embedded C, one PCB project, and optionally Python/ML for IT companies. "
            "Mechanical: SolidWorks/AutoCAD certification, FEA project, core company preparation. "
            "All branches: Communication skills, resume building, and mock interviews matter. "
            "Internships after 3rd year significantly improve placement chances."
        ),
        "tags": ["placement", "tips", "preparation", "interview", "internship"]
    }
]


# ---------------------------------------------------------------------------
# Simple TF-IDF + keyword retriever
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> List[str]:
    return re.findall(r'\b[a-z0-9]+\b', text.lower())


def _build_idf(docs: List[str]) -> Dict[str, float]:
    N = len(docs)
    df: Counter = Counter()
    for doc in docs:
        for word in set(_tokenize(doc)):
            df[word] += 1
    return {w: math.log((N + 1) / (freq + 1)) + 1 for w, freq in df.items()}


_ALL_TEXTS = [d["text"] + " " + " ".join(d["tags"]) for d in KNOWLEDGE_BASE]
_IDF = _build_idf(_ALL_TEXTS)


def _score_doc(query_tokens: List[str], doc_text: str, doc_tags: List[str]) -> float:
    combined = (doc_text + " " + " ".join(doc_tags)).lower()
    tokens   = _tokenize(combined)
    tf       = Counter(tokens)
    total    = len(tokens) or 1
    score    = 0.0
    for qt in query_tokens:
        if qt in tf:
            tf_val  = tf[qt] / total
            idf_val = _IDF.get(qt, 1.0)
            score  += tf_val * idf_val
    return score


class RAGEngine:
    def __init__(self, extra_docs_file: str = "./rag_extra.json"):
        self.extra_docs_file = extra_docs_file
        self.extra_docs: List[Dict] = self._load_extra()

    def _load_extra(self) -> List[Dict]:
        if os.path.exists(self.extra_docs_file):
            try:
                with open(self.extra_docs_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_extra(self):
        with open(self.extra_docs_file, "w", encoding="utf-8") as f:
            json.dump(self.extra_docs, f, indent=2, ensure_ascii=False)

    def add_document(self, text: str, tags: List[str] = None, doc_id: str = None) -> Dict:
        doc = {
            "id":       doc_id or f"extra_{len(self.extra_docs)}",
            "text":     text,
            "tags":     tags or [],
            "added_at": datetime.now().isoformat()
        }
        self.extra_docs.append(doc)
        self._save_extra()
        return {"status": "ok", "total_extra": len(self.extra_docs)}

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        q_tokens = _tokenize(query)
        all_docs = KNOWLEDGE_BASE + self.extra_docs

        scored = []
        for doc in all_docs:
            s = _score_doc(q_tokens, doc["text"], doc.get("tags", []))
            if s > 0:
                scored.append((s, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]

    def answer(self, query: str) -> Dict:
        """
        Answer a question using retrieved docs.
        Uses Gemini LLM if GEMINI_API_KEY is set, else returns extracted text.
        """
        docs = self.retrieve(query, top_k=3)
        if not docs:
            return {
                "answer":  "I don't have specific information on that. Please consult your college counsellor.",
                "sources": [],
                "confidence": 0.0
            }

        context = "\n\n".join(d["text"] for d in docs)

        # Try Gemini if API key is available
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key and api_key not in ("your_gemini_api_key_here", ""):
            try:
                answer_text = self._ask_gemini(query, context, api_key)
                return {
                    "answer":     answer_text,
                    "sources":    [d["id"] for d in docs],
                    "confidence": 0.9,
                    "mode":       "llm"
                }
            except Exception as e:
                pass  # fall through to local answer

        # Local answer: return top doc snippet + a brief summary
        answer_text = self._local_answer(query, docs)
        return {
            "answer":     answer_text,
            "sources":    [d["id"] for d in docs],
            "confidence": 0.75,
            "mode":       "local"
        }

    def _local_answer(self, query: str, docs: List[Dict]) -> str:
        """Return best-matching paragraph from retrieved docs."""
        if not docs:
            return "No relevant information found."
        # Return the first doc's text, nicely trimmed
        return docs[0]["text"].strip()

    def _ask_gemini(self, query: str, context: str, api_key: str) -> str:
        """Call Gemini Flash to generate a contextual answer."""
        import urllib.request, urllib.error
        prompt = (
            f"You are a career counsellor for engineering students in India.\n"
            f"Answer the student's question using ONLY the context provided. "
            f"Be concise and helpful.\n\n"
            f"Context:\n{context}\n\n"
            f"Student's question: {query}\n\n"
            f"Answer:"
        )
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 400, "temperature": 0.3}
        }).encode("utf-8")

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={api_key}"
        )
        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    def get_stats(self) -> Dict:
        return {
            "builtin_docs":  len(KNOWLEDGE_BASE),
            "extra_docs":    len(self.extra_docs),
            "total_docs":    len(KNOWLEDGE_BASE) + len(self.extra_docs)
        }


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    rag = RAGEngine()
    print("Stats:", rag.get_stats())
    queries = [
        "What is the salary of a CSE engineer?",
        "Which branch is better for AI and data science?",
        "What are the career options in electronics?",
        "How do I prepare for GATE?",
        "What is the future of mechanical engineering?"
    ]
    for q in queries:
        result = rag.answer(q)
        print(f"\nQ: {q}")
        print(f"A: {result['answer'][:150]}...")
        print(f"   Sources: {result['sources']}")
