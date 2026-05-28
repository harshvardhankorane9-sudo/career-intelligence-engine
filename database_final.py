"""
Career Intelligence Engine — Database Models & Seed Data
SQLAlchemy ORM for SQLite (dev) / PostgreSQL (prod)

Branches (8 total):
  Existing : CSE | CSE-AIML | MECH | ECE
  New      : CIVIL | CHEM | BME | AERO
"""

import os
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    JSON, Text, ForeignKey, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# ---------------------------------------------------------------------------
# ORM Models
# ---------------------------------------------------------------------------

class Student(Base):
    __tablename__ = "students"
    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(255), nullable=False)
    email        = Column(String(255), unique=True, index=True, nullable=False)
    college      = Column(String(255), default="")
    branch_year  = Column(Integer, default=1)
    created_at   = Column(DateTime, default=datetime.utcnow)

    assessments  = relationship("Assessment",       back_populates="student", cascade="all, delete-orphan")
    simulations  = relationship("SimulationRecord", back_populates="student", cascade="all, delete-orphan")
    chats        = relationship("ChatSession",      back_populates="student", cascade="all, delete-orphan")


class Branch(Base):
    __tablename__ = "branches"
    id               = Column(Integer, primary_key=True, index=True)
    code             = Column(String(30), unique=True, nullable=False)
    name             = Column(String(255), nullable=False)
    tagline          = Column(String(255))
    description      = Column(Text)
    core_subjects    = Column(JSON)   # list[str]
    core_skills      = Column(JSON)   # list[str]
    skill_weights    = Column(JSON)   # {dimension: weight 0-1}
    career_paths     = Column(JSON)   # list[str]
    top_recruiters   = Column(JSON)   # list[str]
    certifications   = Column(JSON)   # list[str]
    higher_studies   = Column(JSON)   # list[str]
    future_scope     = Column(Text)
    entry_salary     = Column(String(50))
    mid_salary       = Column(String(50))
    senior_salary    = Column(String(50))
    growth_rate      = Column(String(30))
    job_openings     = Column(String(30))
    color            = Column(String(20), default="#667eea")


class Assessment(Base):
    __tablename__ = "assessments"
    id                   = Column(Integer, primary_key=True, index=True)
    student_id           = Column(Integer, ForeignKey("students.id"), nullable=False)
    raw_answers          = Column(JSON)
    skill_scores         = Column(JSON)
    recommended_branches = Column(JSON)
    confidence           = Column(Float, default=0.0)
    completed_at         = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="assessments")


class SimulationRecord(Base):
    __tablename__ = "simulation_records"
    id           = Column(Integer, primary_key=True, index=True)
    student_id   = Column(Integer, ForeignKey("students.id"), nullable=False)
    branch_code  = Column(String(30), nullable=False)
    decisions    = Column(JSON, default=list)
    total_score  = Column(Float, default=0.0)
    max_score    = Column(Float, default=0.0)
    percentage   = Column(Float, default=0.0)
    performance  = Column(String(50), default="")
    is_complete  = Column(Boolean, default=False)
    started_at   = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="simulations")


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    student  = relationship("Student", back_populates="chats")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id         = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role       = Column(String(20), nullable=False)   # user | assistant
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


# ---------------------------------------------------------------------------
# DB engine / session
# ---------------------------------------------------------------------------

# Render gives "postgres://" but SQLAlchemy needs "postgresql://"
_raw_url    = os.getenv("DATABASE_URL", "sqlite:///./career_intelligence.db")
DATABASE_URL = _raw_url.replace("postgres://", "postgresql://", 1)

# Build engine kwargs — pool_pre_ping keeps cloud connections alive
_engine_kwargs: dict = {"pool_pre_ping": True}
if "sqlite" in DATABASE_URL:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# All 11 branches
# ---------------------------------------------------------------------------

BRANCHES = [

    # ── 1. CSE ──────────────────────────────────────────────────────────────
    {
        "code":    "CSE",
        "name":    "Computer Science & Engineering",
        "tagline": "Build the software that runs the world",
        "color":   "#4f46e5",
        "description": (
            "CSE is the foundation of modern technology. You'll master algorithms, "
            "data structures, operating systems, databases, and software engineering. "
            "Graduates build everything from mobile apps to cloud infrastructure."
        ),
        "core_subjects": [
            "Data Structures & Algorithms", "Operating Systems", "DBMS",
            "Computer Networks", "Software Engineering", "Compiler Design",
            "Theory of Computation", "Web Development"
        ],
        "core_skills": [
            "Python / Java / C++", "DSA & Problem Solving", "System Design",
            "Web / App Development", "Databases (SQL, NoSQL)", "Git & DevOps"
        ],
        "skill_weights": {
            "coding": 0.95, "mathematics": 0.70, "analytical": 0.85,
            "hardware": 0.20, "creativity": 0.60, "research": 0.50,
            "communication": 0.55, "entrepreneurship": 0.60
        },
        "career_paths": [
            "Software Development Engineer (SDE)",
            "Backend / Frontend / Full-Stack Developer",
            "DevOps & Cloud Engineer",
            "Database Administrator",
            "System Architect",
            "Technical Product Manager"
        ],
        "top_recruiters": [
            "Google", "Microsoft", "Amazon", "Flipkart",
            "Infosys", "TCS", "Wipro", "Atlassian", "Adobe"
        ],
        "certifications": [
            "AWS Solutions Architect", "Google Cloud Professional",
            "Meta Full-Stack Developer", "Oracle Java SE"
        ],
        "higher_studies": ["M.Tech CSE", "MS Abroad", "MBA (Tech)", "PhD CS"],
        "future_scope": (
            "Software demand is growing 25% YoY. Cloud, cybersecurity, and "
            "distributed systems are hot areas. CSE grads have the widest job market."
        ),
        "entry_salary":  "6–14 LPA",
        "mid_salary":    "18–40 LPA",
        "senior_salary": "50–120 LPA",
        "growth_rate":   "+25% YoY",
        "job_openings":  "~3.5 Lakh"
    },

    # ── 2. CSE-AIML ──────────────────────────────────────────────────────────
    {
        "code":    "CSE-AIML",
        "name":    "CSE with AI & Machine Learning",
        "tagline": "Engineer the intelligence of tomorrow",
        "color":   "#7c3aed",
        "description": (
            "CSE-AIML is CSE supercharged with deep learning, NLP, computer vision, "
            "and MLOps. You'll build intelligent systems that learn from data — "
            "from recommendation engines to autonomous systems."
        ),
        "core_subjects": [
            "Machine Learning", "Deep Learning", "Natural Language Processing",
            "Computer Vision", "Data Science & Analytics", "Reinforcement Learning",
            "Big Data Engineering", "Probability & Statistics"
        ],
        "core_skills": [
            "Python (NumPy, Pandas, Scikit-learn)", "TensorFlow / PyTorch",
            "Data Preprocessing & EDA", "Model Deployment (MLOps)",
            "Statistics & Probability", "SQL & NoSQL for Big Data"
        ],
        "skill_weights": {
            "coding": 0.90, "mathematics": 0.92, "analytical": 0.95,
            "hardware": 0.15, "creativity": 0.65, "research": 0.80,
            "communication": 0.55, "entrepreneurship": 0.55
        },
        "career_paths": [
            "Machine Learning Engineer",
            "Data Scientist",
            "AI Research Scientist",
            "NLP / Computer Vision Engineer",
            "MLOps / AI Platform Engineer",
            "Generative AI Engineer"
        ],
        "top_recruiters": [
            "Google DeepMind", "OpenAI", "Microsoft AI", "Amazon",
            "NVIDIA", "Zomato", "PhonePe", "Meesho", "Fractal Analytics"
        ],
        "certifications": [
            "TensorFlow Developer Certificate", "AWS ML Specialty",
            "Google Professional ML Engineer", "Coursera Deep Learning Specialization"
        ],
        "higher_studies": ["M.Tech AI/ML", "MS in CS (ML focus)", "PhD AI", "MBA (Data)"],
        "future_scope": (
            "AI is the fastest-growing tech field. Generative AI, LLMs, and autonomous "
            "systems are creating entirely new industries. This is the highest-paying "
            "tech specialisation globally."
        ),
        "entry_salary":  "8–18 LPA",
        "mid_salary":    "20–45 LPA",
        "senior_salary": "60–150 LPA",
        "growth_rate":   "+40% YoY",
        "job_openings":  "~1.8 Lakh"
    },

    # ── 3. MECH ──────────────────────────────────────────────────────────────
    {
        "code":    "MECH",
        "name":    "Mechanical Engineering",
        "tagline": "Design and build the physical world",
        "color":   "#d97706",
        "description": (
            "Mechanical Engineering is the broadest engineering discipline — spanning "
            "thermodynamics, fluid mechanics, manufacturing, robotics, and product design. "
            "Mechs design everything from engines to spacecraft."
        ),
        "core_subjects": [
            "Engineering Mechanics (Statics & Dynamics)", "Thermodynamics",
            "Fluid Mechanics", "Strength of Materials",
            "Manufacturing Processes", "Theory of Machines",
            "Heat Transfer", "CAD / CAM / FEA"
        ],
        "core_skills": [
            "AutoCAD / SolidWorks / CATIA", "FEA (ANSYS, Abaqus)",
            "Manufacturing & Machining", "Thermodynamic Analysis",
            "Robotics & Automation (ROS)", "MATLAB / Python for simulation"
        ],
        "skill_weights": {
            "coding": 0.40, "mathematics": 0.80, "analytical": 0.75,
            "hardware": 0.85, "creativity": 0.80, "research": 0.55,
            "communication": 0.60, "entrepreneurship": 0.55
        },
        "career_paths": [
            "Design Engineer",
            "Manufacturing / Production Engineer",
            "Automotive / Aerospace Engineer",
            "Robotics & Automation Engineer",
            "HVAC / Thermal Systems Engineer",
            "R&D Scientist"
        ],
        "top_recruiters": [
            "Tata Motors", "Mahindra", "L&T", "ISRO", "DRDO",
            "Bosch", "Cummins India", "Siemens", "John Deere", "Eaton"
        ],
        "certifications": [
            "SolidWorks CSWA / CSWP", "AutoCAD Certified Professional",
            "Six Sigma Green Belt", "PMP (Project Management)"
        ],
        "higher_studies": [
            "M.Tech Manufacturing / Thermal", "MS Mechanical Engineering",
            "MBA Operations", "M.Tech Robotics"
        ],
        "future_scope": (
            "EV revolution, Industry 4.0, additive manufacturing (3D printing), "
            "and defense modernisation are driving huge demand. "
            "Mechs who learn coding + simulation are premium hires."
        ),
        "entry_salary":  "4–9 LPA",
        "mid_salary":    "12–22 LPA",
        "senior_salary": "25–55 LPA",
        "growth_rate":   "+12% YoY",
        "job_openings":  "~2.2 Lakh"
    },

    # ── 4. ECE ───────────────────────────────────────────────────────────────
    {
        "code":    "ECE",
        "name":    "Electronics & Communication Engineering",
        "tagline": "Power the signals that connect everything",
        "color":   "#0891b2",
        "description": (
            "ECE blends electronics, signal processing, communication systems, "
            "and embedded programming. ECE engineers design chips, build wireless systems, "
            "create IoT devices, and work on 5G and satellite communication."
        ),
        "core_subjects": [
            "Analog & Digital Electronics", "Signals & Systems",
            "Digital Signal Processing", "Communication Systems",
            "Microprocessors & Embedded Systems", "VLSI Design",
            "Antenna & RF Engineering", "Control Systems"
        ],
        "core_skills": [
            "Circuit Design (Analog + Digital)", "Embedded C / RTOS",
            "MATLAB / Simulink", "PCB Design (KiCAD / Altium)",
            "FPGA / Verilog / VHDL", "Communication Protocols (SPI, I2C, UART)"
        ],
        "skill_weights": {
            "coding": 0.65, "mathematics": 0.80, "analytical": 0.80,
            "hardware": 0.95, "creativity": 0.55, "research": 0.60,
            "communication": 0.55, "entrepreneurship": 0.45
        },
        "career_paths": [
            "Embedded Systems Engineer",
            "VLSI / Chip Design Engineer",
            "RF / Communication Engineer",
            "IoT Solutions Architect",
            "Signal Processing Engineer",
            "Telecom Network Engineer"
        ],
        "top_recruiters": [
            "Intel", "Qualcomm", "Texas Instruments", "Samsung Semiconductor",
            "ISRO", "Airtel", "Jio", "STMicroelectronics", "NXP", "MediaTek"
        ],
        "certifications": [
            "ARM Certified Engineer", "Cisco CCNA",
            "Certified IoT Professional (CIoTP)", "Cadence PCB Design"
        ],
        "higher_studies": [
            "M.Tech VLSI", "M.Tech Signal Processing",
            "MS ECE Abroad", "M.Tech Embedded Systems"
        ],
        "future_scope": (
            "5G rollout, semiconductor self-reliance (India Chip Mission), "
            "IoT explosion, and space-tech boom are creating massive ECE demand. "
            "VLSI engineers are among the highest-paid hardware professionals."
        ),
        "entry_salary":  "5–11 LPA",
        "mid_salary":    "14–28 LPA",
        "senior_salary": "30–70 LPA",
        "growth_rate":   "+18% YoY",
        "job_openings":  "~1.5 Lakh"
    },

    # ── 5. CIVIL ─────────────────────────────────────────────────────────────
    {
        "code":    "CIVIL",
        "name":    "Civil Engineering",
        "tagline": "Build the infrastructure that holds a nation together",
        "color":   "#059669",
        "description": (
            "Civil Engineering is the oldest and most visible engineering discipline. "
            "Civil engineers design and build roads, bridges, dams, airports, metro systems, "
            "water supply networks, and smart cities. In India, with massive infrastructure "
            "spending under National Infrastructure Pipeline (₹111 lakh crore by 2025), "
            "civil engineers are in unprecedented demand."
        ),
        "core_subjects": [
            "Structural Analysis", "Reinforced Concrete Design (RCC)",
            "Geotechnical Engineering (Soil Mechanics)", "Transportation Engineering",
            "Fluid Mechanics & Hydraulics", "Environmental Engineering",
            "Construction Management", "Surveying & Geo-informatics"
        ],
        "core_skills": [
            "AutoCAD Civil 3D / STAAD.Pro", "ETABS / SAP2000 (structural analysis)",
            "Revit BIM (Building Information Modelling)", "MS Project / Primavera",
            "Soil testing & site investigation", "Quantity estimation & costing"
        ],
        "skill_weights": {
            "coding": 0.25, "mathematics": 0.85, "analytical": 0.80,
            "hardware": 0.70, "creativity": 0.75, "research": 0.55,
            "communication": 0.80, "entrepreneurship": 0.60
        },
        "career_paths": [
            "Structural Design Engineer",
            "Site / Project Engineer (Construction)",
            "Transportation & Highway Engineer",
            "Geotechnical / Foundation Engineer",
            "Urban Planner & Smart City Consultant",
            "Government Engineer (PWD / NHAI / Municipal Corporation)"
        ],
        "top_recruiters": [
            "L&T Construction", "Shapoorji Pallonji", "NCC Limited",
            "Afcons Infrastructure", "NHAI", "NMRC / Metro Rail",
            "AECOM India", "Jacobs India", "Pune Municipal Corporation",
            "MSRDC (Maharashtra State Road Development Corporation)"
        ],
        "certifications": [
            "STAAD.Pro Certified Engineer", "Autodesk Revit BIM Professional",
            "PMP (Project Management Professional)", "LEED Green Associate"
        ],
        "higher_studies": [
            "M.Tech Structural Engineering", "M.Tech Geotechnical Engineering",
            "M.Tech Transportation Engineering", "MS Civil Abroad",
            "MBA Construction Management", "GATE → PSU / IES"
        ],
        "future_scope": (
            "India's National Infrastructure Pipeline targets ₹111 lakh crore in "
            "roads, railways, airports, and smart cities by 2025. "
            "Pune Metro Phase 2, Mumbai-Pune Expressway expansion, and Navi Mumbai airport "
            "are all creating large-scale civil engineering demand. "
            "BIM (Building Information Modelling) and smart city planning are premium skills."
        ),
        "entry_salary":  "3.5–7 LPA",
        "mid_salary":    "10–20 LPA",
        "senior_salary": "22–50 LPA",
        "growth_rate":   "+15% YoY",
        "job_openings":  "~4.0 Lakh"
    },

    # ── 5. CHEM ──────────────────────────────────────────────────────────────
    {
        "code":    "CHEM",
        "name":    "Chemical Engineering",
        "tagline": "Transform raw materials into the products that make modern life possible",
        "color":   "#dc2626",
        "description": (
            "Chemical Engineering applies chemistry, physics, and mathematics to design "
            "industrial processes that convert raw materials into useful products — "
            "fuels, pharmaceuticals, plastics, fertilisers, specialty chemicals, and food. "
            "Chemical engineers design reactors, distillation columns, heat exchangers, "
            "and safety systems for some of the world's most complex industrial facilities."
        ),
        "core_subjects": [
            "Chemical Process Thermodynamics", "Fluid Mechanics & Mass Transfer",
            "Heat Transfer Operations", "Chemical Reaction Engineering",
            "Process Control & Instrumentation", "Mass Transfer (Distillation, Absorption)",
            "Plant Design & Economics", "Safety & Hazard Analysis (HAZOP)"
        ],
        "core_skills": [
            "HYSYS / Aspen Plus (process simulation)", "AutoCAD P&ID",
            "MATLAB / Python for process modelling", "HAZOP & safety analysis",
            "Reactor design & scale-up", "Quality control & Six Sigma"
        ],
        "skill_weights": {
            "coding": 0.40, "mathematics": 0.88, "analytical": 0.85,
            "hardware": 0.65, "creativity": 0.60, "research": 0.75,
            "communication": 0.65, "entrepreneurship": 0.50
        },
        "career_paths": [
            "Process / Plant Engineer",
            "Production Engineer (Pharma / Refinery / Fertilizer)",
            "R&D Chemist / Process Development Engineer",
            "Environmental / Safety Engineer",
            "Quality Assurance Engineer",
            "Petroleum / Refinery Engineer"
        ],
        "top_recruiters": [
            "Reliance Industries", "ONGC", "HPCL", "BPCL",
            "UPL Pune", "Thermax Pune", "Bajaj Finserv (Chemicals)",
            "Sun Pharma", "Dr. Reddy's Laboratories", "BASF India",
            "Pidilite Industries", "Asian Paints"
        ],
        "certifications": [
            "Aspen Plus Certified User", "Six Sigma Green Belt",
            "Process Safety Management (PSM)", "NEBOSH International General Certificate",
            "GATE → PSU (ONGC, HPCL, BPCL)"
        ],
        "higher_studies": [
            "M.Tech Chemical Engineering", "M.Tech Petroleum Refining",
            "M.Tech Pharmaceutical Technology", "MS Chemical Engineering (Abroad)",
            "MBA Operations / Supply Chain", "GATE → IIT / PSU"
        ],
        "future_scope": (
            "India's specialty chemicals market is growing at 12% annually, driven by "
            "global supply chain shifts away from China. "
            "Pharmaceutical manufacturing (India is the world's pharmacy) and green chemistry "
            "(bio-based plastics, green hydrogen) are hot areas. "
            "Pune's pharmaceutical cluster employs thousands of chemical engineers."
        ),
        "entry_salary":  "4–8 LPA",
        "mid_salary":    "10–22 LPA",
        "senior_salary": "22–48 LPA",
        "growth_rate":   "+13% YoY",
        "job_openings":  "~1.2 Lakh"
    },

    # ── 6. BME ───────────────────────────────────────────────────────────────
    {
        "code":    "BME",
        "name":    "Biomedical Engineering",
        "tagline": "Engineer solutions that save and extend human lives",
        "color":   "#db2777",
        "description": (
            "Biomedical Engineering sits at the intersection of engineering and medicine. "
            "BME engineers design medical devices (pacemakers, prosthetics, MRI machines), "
            "develop diagnostic equipment, build hospital information systems, and apply "
            "AI to medical imaging and drug discovery. "
            "India's medical device sector is growing rapidly with government push for "
            "domestic manufacturing (Make in India for medical devices)."
        ),
        "core_subjects": [
            "Human Anatomy & Physiology", "Biomechanics",
            "Medical Instrumentation & Sensors", "Biomedical Signal Processing",
            "Medical Imaging (MRI, CT, Ultrasound)", "Biomaterials",
            "Hospital Information Systems", "Regulatory Affairs (FDA / CDSCO)"
        ],
        "core_skills": [
            "MATLAB / Python for biomedical signal processing",
            "LabVIEW (medical instrumentation)", "SolidWorks (medical device design)",
            "Medical imaging software (3D Slicer, ImageJ)",
            "PCB design for low-power medical devices",
            "Clinical trial documentation & regulatory compliance"
        ],
        "skill_weights": {
            "coding": 0.60, "mathematics": 0.75, "analytical": 0.82,
            "hardware": 0.70, "creativity": 0.70, "research": 0.85,
            "communication": 0.70, "entrepreneurship": 0.55
        },
        "career_paths": [
            "Medical Device Design Engineer",
            "Biomedical / Clinical Engineer (Hospital)",
            "Medical Imaging Specialist",
            "Regulatory Affairs Engineer (FDA / CDSCO)",
            "Biomedical Data Scientist",
            "Prosthetics & Rehabilitation Engineer"
        ],
        "top_recruiters": [
            "Philips Healthcare India", "GE Healthcare India",
            "Siemens Healthineers", "Medtronic India",
            "Stryker India", "Trivitron Healthcare",
            "HLL Lifecare", "Wipro GE Healthcare", "Skanray Technologies",
            "AIIMS / NIMHANS (Research positions)"
        ],
        "certifications": [
            "CBET (Certified Biomedical Equipment Technician)",
            "Regulatory Affairs Certification (RAC)", "Six Sigma Healthcare",
            "MATLAB Biomedical Signal Processing", "LabVIEW Core Developer"
        ],
        "higher_studies": [
            "M.Tech Biomedical Engineering", "M.Tech Medical Devices",
            "MS Biomedical Engineering (Abroad)", "MD / MBA (Healthcare Management)",
            "PhD Biomedical Sciences"
        ],
        "future_scope": (
            "India's medical device market is projected to reach $50 billion by 2030. "
            "Government's Production Linked Incentive (PLI) scheme for medical devices "
            "is attracting global companies to manufacture in India. "
            "AI-based medical imaging diagnostics (cancer detection, radiology AI) is the "
            "fastest-growing niche — combining BME and ML knowledge."
        ),
        "entry_salary":  "4–9 LPA",
        "mid_salary":    "10–22 LPA",
        "senior_salary": "22–50 LPA",
        "growth_rate":   "+18% YoY",
        "job_openings":  "~80,000"
    },

    # ── 7. AERO ─────────────────────────────────────────────────────────────
    {
        "code":    "AERO",
        "name":    "Aerospace Engineering",
        "tagline": "Design the machines that conquer the sky and reach for the stars",
        "color":   "#6d28d9",
        "description": (
            "Aerospace Engineering covers the design, development, and testing of aircraft, "
            "helicopters, rockets, satellites, and drones. It combines aerodynamics, structural "
            "analysis, propulsion, avionics, and control systems. "
            "India's space economy is booming — ISRO, IN-SPACe (private space policy), "
            "and Indian defence modernisation are creating significant aerospace demand. "
            "Pune has HAL (Hindustan Aeronautics Limited) and a growing aerospace cluster."
        ),
        "core_subjects": [
            "Aerodynamics (Subsonic, Transonic, Supersonic)", "Aircraft Structures",
            "Propulsion Systems (Jet Engines, Rockets)", "Flight Mechanics & Control",
            "Avionics & Navigation Systems", "Computational Fluid Dynamics (CFD)",
            "Spacecraft Systems & Mission Design", "Composite Materials & Fatigue"
        ],
        "core_skills": [
            "ANSYS Fluent / OpenFOAM (CFD simulation)", "CATIA / SolidWorks (aircraft design)",
            "MATLAB / Simulink (flight dynamics)", "Embedded C (avionics firmware)",
            "Wind tunnel testing & data analysis", "Composite material lay-up & testing"
        ],
        "skill_weights": {
            "coding": 0.55, "mathematics": 0.92, "analytical": 0.90,
            "hardware": 0.82, "creativity": 0.70, "research": 0.80,
            "communication": 0.60, "entrepreneurship": 0.45
        },
        "career_paths": [
            "Aerodynamics / CFD Engineer",
            "Aircraft Structural Design Engineer",
            "Propulsion / Gas Turbine Engineer",
            "Avionics / Flight Systems Engineer",
            "Spacecraft / Satellite Systems Engineer",
            "Drone / UAV Systems Engineer"
        ],
        "top_recruiters": [
            "ISRO", "HAL (Hindustan Aeronautics Limited)", "DRDO (ADE / GTRE)",
            "NAL (National Aerospace Laboratories)", "Mahindra Defence",
            "Tata Advanced Systems", "Safran India", "Boeing India",
            "Airbus India Engineering Centre", "AgniKul Cosmos", "Skyroot Aerospace"
        ],
        "certifications": [
            "ANSYS Fluent CFD Certification", "Catia V5 Aerospace Certified",
            "DGCA Aircraft Maintenance Engineer (AME) License",
            "AS9100 Quality Management (Aerospace)"
        ],
        "higher_studies": [
            "M.Tech Aerospace Engineering", "M.Tech CFD / Propulsion",
            "MS Aerospace (USA / Germany / France)", "PhD Aerospace Sciences",
            "GATE → ISRO / HAL / DRDO / IIT"
        ],
        "future_scope": (
            "India's space economy is projected to grow from $8 billion to $44 billion by 2033. "
            "IN-SPACe policy opened private space to startups — AgniKul, Skyroot, Pixxel all "
            "hiring aerospace engineers. "
            "Defence indigenisation (LCA Tejas Mk2, AMCA stealth fighter, DRDO projects) "
            "and drone manufacturing (PLI scheme) are creating 50,000+ aerospace jobs."
        ),
        "entry_salary":  "5–12 LPA",
        "mid_salary":    "14–28 LPA",
        "senior_salary": "28–65 LPA",
        "growth_rate":   "+22% YoY",
        "job_openings":  "~60,000"
    },


]


# ---------------------------------------------------------------------------
# Seed — checks each branch individually so re-running adds new ones
# ---------------------------------------------------------------------------

def seed_branches(db):
    """
    Upsert-style seed: inserts any branch whose code is not yet in the DB.
    Safe to call on both a fresh DB and one that already has the original 4 branches.
    """
    added = 0
    for b in BRANCHES:
        exists = db.query(Branch).filter(Branch.code == b["code"]).first()
        if not exists:
            db.add(Branch(**b))
            added += 1
    if added:
        db.commit()
        print(f"✅ Seeded {added} new branch(es)  (total: {db.query(Branch).count()})")
    else:
        print(f"ℹ️  All {db.query(Branch).count()} branches already present — nothing to seed")


# ---------------------------------------------------------------------------
# Run directly to initialise / re-seed
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    init_database()
    db = SessionLocal()
    seed_branches(db)
    db.close()
    print("🎉 Database ready!")
