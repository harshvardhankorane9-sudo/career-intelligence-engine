"""
Day-in-the-Life Simulator — Career Intelligence Engine v3.3
BRANCH_INTRO completely redesigned for 12th-standard students:
  - real_apps:        Everyday apps/products they use → what this branch built
  - bridge_12th:      Their 12th knowledge mapped to engineering superpowers
  - real_problems:    3 real before/after problem stories (no jargon)
  - personality_fit:  "You'll love this if..." statements
  - day_timeline:     Clickable hourly schedule
  - tools:            Tools list
  - reality_check:    The honest truth nobody tells you
  - youtube_search:   YouTube search query (always reliable)
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
# Branch introductions  — redesigned for students with zero prior knowledge
# ─────────────────────────────────────────────────────────────────────────────

BRANCH_INTRO: Dict[str, Dict] = {

    "CSE": {
        "tagline": "Every tap on your phone runs code that someone like you wrote.",
        "real_apps": [
            {
                "app": "LeetCode / Codeforces — competitive programming judges",
                "emoji": "🏆",
                "what_they_built": "The online judge that runs your submitted code against thousands of hidden test cases in milliseconds — enforcing time limits, memory limits, and catching edge cases — is itself a complex distributed system built by CSE engineers. It runs millions of untrusted code submissions safely every day using sandboxing and containerisation.",
                "cool_fact": "Codeforces runs over 1 million code submissions per day. Each one is executed in an isolated container so a malicious program cannot crash the server or read other users' code."
            },
            {
                "app": "AWS / Cloud infrastructure",
                "emoji": "☁️",
                "what_they_built": "Every time any website you use stays online — that reliability is built by cloud engineers. They design systems where even if 50 servers physically catch fire, the website keeps running. This involves concepts like load balancing, auto-scaling, replication, and consensus algorithms — all core CSE topics.",
                "cool_fact": "AWS runs the backend of Netflix, NASA, the Indian government's Aadhaar portal, and roughly 1/3 of the entire internet. A 1-hour AWS outage in 2021 took down thousands of unrelated websites simultaneously."
            },
            {
                "app": "Antivirus / cybersecurity tools",
                "emoji": "🛡️",
                "what_they_built": "When your antivirus scans a new file, it uses pattern matching algorithms to compare the file's binary signature against a database of 1 billion known malware signatures — in under a second. CSE engineers also build the intrusion detection systems that monitor network traffic and flag anomalies in real time.",
                "cool_fact": "Over 450,000 new malware programs are registered every day. Cybersecurity engineers must build systems that detect threats they have never seen before — using behavioural analysis, not just signature databases."
            },
            {
                "app": "Git / GitHub — version control",
                "emoji": "🔀",
                "what_they_built": "Git is a data structure — a directed acyclic graph where every commit is a node — designed by Linus Torvalds (who also created Linux) in 2005. Every merge, branch, and conflict resolution is a graph operation. The algorithm that merges two diverged codebases without losing changes is a three-way merge algorithm — pure CS theory turned into a tool every developer uses every day.",
                "cool_fact": "GitHub hosts over 330 million repositories. Every 'git merge' you run executes a three-way merge algorithm first described in academic CS papers in the 1980s."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Solving algebra problems step by step",
                "becomes_in_engineering": "Algorithm design — breaking any problem into logical steps a computer can execute",
                "emoji": "📐"
            },
            {
                "knew_in_12th": "Maths: sets, functions, logic gates",
                "becomes_in_engineering": "Data structures and discrete mathematics — the foundation of all programming",
                "emoji": "🔢"
            },
            {
                "knew_in_12th": "Computer Science class: if-else, loops, arrays",
                "becomes_in_engineering": "Writing production code used by millions — same concepts, infinitely bigger scale",
                "emoji": "💻"
            },
            {
                "knew_in_12th": "Physics: understanding how electricity flows in circuits",
                "becomes_in_engineering": "Understanding how hardware works — makes you a better systems programmer",
                "emoji": "⚡"
            },
        ],
        "real_problems": [
            {
                "problem": "In 2020, Zoom crashed for 300 million users on the same day.",
                "why_it_happened": "Their database couldn't handle the sudden load when the whole world switched to remote work overnight.",
                "how_engineers_fixed_it": "CSE engineers redesigned the database architecture to be distributed across hundreds of servers — so even if 10 servers fail, the app keeps running.",
                "lesson": "This is called 'distributed systems design' — one of the highest-paying skills in software.",
                "emoji": "🔧"
            },
            {
                "problem": "In 2019, a bank's online portal crashed and 2 lakh customers couldn't access their money for 3 days.",
                "why_it_happened": "A software update had a bug that corrupted the authentication system.",
                "how_engineers_fixed_it": "Now banks have 'canary deployments' — engineers release updates to 1% of users first. If something breaks, they catch it before it affects everyone.",
                "lesson": "This is 'DevOps engineering' — building systems so software updates are safe and automatic.",
                "emoji": "🏦"
            },
            {
                "problem": "Early ride-sharing apps in India assigned drivers randomly — sometimes a driver 15 km away when there was one 200m from you.",
                "why_it_happened": "The matching algorithm was too simple.",
                "how_engineers_fixed_it": "CSE engineers built a geospatial matching system that considers distance, traffic, driver rating, and ETA simultaneously — now Ola/Uber matching is nearly perfect.",
                "lesson": "Algorithm design changes actual user experience for millions of people.",
                "emoji": "🚕"
            },
        ],
        "personality_fit": [
            "You spend 10 minutes finding the 'cleanest' solution to a problem instead of the first one that works",
            "You get genuinely annoyed when an app is slow or crashes",
            "You've ever wondered how Instagram knows what you want to see before you do",
            "You enjoy puzzles, Sudoku, or anything where logic leads to a satisfying answer",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "Check overnight alerts", "detail": "A payment API is failing for 0.2% of requests. You open the server logs to investigate.", "mood": "detective"},
            {"time": "10:00 AM", "task": "Team standup (15 min)", "detail": "5 people, everyone says what they did yesterday and what they're doing today. Fast and focused.", "mood": "team"},
            {"time": "10:30 AM", "task": "Deep work: debugging", "detail": "You trace the payment bug to a race condition — two requests running at the same time stepping on each other. You write a fix.", "mood": "focus"},
            {"time": "1:00 PM", "task": "Lunch break", "detail": "30-60 minutes. Most engineers step away from screens — it genuinely helps with problem-solving.", "mood": "break"},
            {"time": "2:00 PM", "task": "Code review", "detail": "A colleague's new feature has a potential security vulnerability. You leave a detailed comment explaining the risk and how to fix it.", "mood": "team"},
            {"time": "3:30 PM", "task": "Architecture meeting", "detail": "Your team is planning a new notifications system. You draw diagrams showing how data flows between services.", "mood": "creative"},
            {"time": "5:00 PM", "task": "Deploy & verify", "detail": "Your bug fix goes to production. You watch the error rate drop to 0% in real-time. Deeply satisfying.", "mood": "win"},
        ],
        "tools": ["Python / Java / Go", "VS Code / IntelliJ", "Git + GitHub", "AWS / GCP", "Docker & Kubernetes", "Postman (API testing)", "Datadog (monitoring)"],
        "reality_check": "You will spend 30% of your time reading other people's old, messy code. That's normal — senior engineers are good at it, not frustrated by it. The '10x programmer' who codes alone all day is a myth. Real engineering is collaborative.",
        "salary_snapshot": "Fresher at product company: ₹8–18 LPA. After 5 years at a top startup/MNC: ₹35–80 LPA.",
        "youtube_search": "day in the life software engineer India",
        
    },

    "CSE-AIML": {
        "tagline": "The algorithm that decides what you watch next, what ad you see, and whether your loan is approved — an ML engineer trained it.",
        "real_apps": [
            {
                "app": "NEET / JEE aptitude pattern recognition",
                "emoji": "📝",
                "what_they_built": "EdTech platforms like Embibe and BYJU's use ML models that analyse thousands of a student's past answers to predict exactly which concept they are weak in — and which question type will trip them up next. The model identifies patterns like 'this student always gets parabola problems wrong when the axis is horizontal' from subtle answer timing and error data.",
                "cool_fact": "Embibe's ML system analyses 2 million data points per student to personalise question difficulty. It can predict a student's JEE rank 6 months before the exam with 87% accuracy."
            },
            {
                "app": "Kaggle competition winners — real ML research",
                "emoji": "🏅",
                "what_they_built": "When Kaggle runs a competition to predict hospital readmission or detect skin cancer from photos, the winning solutions are built by ML engineers using gradient boosting, ensemble methods, and custom loss functions. These solutions directly get adopted by hospitals and diagnostic labs — not as a product, but as a trained model that doctors use alongside their judgment.",
                "cool_fact": "The winning model in the 2016 Kaggle Diabetic Retinopathy Detection competition was more accurate than the average ophthalmologist. It is now used in real clinics in the UK."
            },
            {
                "app": "AlphaFold — protein structure prediction",
                "emoji": "🧬",
                "what_they_built": "For 50 years, predicting the 3D shape of a protein from its amino acid sequence was considered one of biology's hardest unsolved problems. In 2020, DeepMind's AlphaFold — an ML model — solved it. ML engineers designed a transformer architecture that treats amino acid sequences like language and predicts the spatial folding of 200 million proteins.",
                "cool_fact": "AlphaFold predicted the structure of every protein in the human body in 18 months. The same work would have taken traditional biochemistry methods millions of years."
            },
            {
                "app": "Fraud detection logic in banking",
                "emoji": "🔍",
                "what_they_built": "When your bank blocks a transaction and asks 'did you make this purchase?', an ML model made that decision in 30 milliseconds. It scored the transaction against 200+ features — your location, merchant type, transaction time, device fingerprint, and historical spend pattern — and flagged it as anomalous. ML engineers built and tuned the model that balances catching real fraud without blocking legitimate transactions.",
                "cool_fact": "A false positive (blocking a real transaction) costs a bank approximately ₹500 in customer service and relationship damage. Indian banks process 5 crore card transactions per day — getting the fraud threshold wrong by 0.1% has crore-level consequences."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Statistics: mean, standard deviation, probability distributions",
                "becomes_in_engineering": "The foundation of every ML model — you use probability to measure how 'confident' a model is in its predictions",
                "emoji": "📊"
            },
            {
                "knew_in_12th": "Maths: matrices, linear algebra (vectors, dot products)",
                "becomes_in_engineering": "How neural networks store knowledge — millions of numbers in matrices multiplied together to produce intelligence",
                "emoji": "🔢"
            },
            {
                "knew_in_12th": "Calculus: derivatives, rates of change",
                "becomes_in_engineering": "Gradient descent — how an ML model learns by calculating which direction to move to reduce its errors",
                "emoji": "📉"
            },
            {
                "knew_in_12th": "Programming: loops, conditions, functions",
                "becomes_in_engineering": "Python for ML — you write the training code, data pipelines, and deployment scripts",
                "emoji": "🐍"
            },
        ],
        "real_problems": [
            {
                "problem": "Doctors miss 20% of early-stage cancers in X-ray scans — because human eyes get tired and X-rays are subtle.",
                "why_it_happened": "Early cancer looks almost identical to normal tissue. Even expert radiologists disagree on borderline cases.",
                "how_engineers_fixed_it": "ML engineers trained a computer vision model on 1 million labelled X-rays. The model now detects early cancer with 94% accuracy and never gets tired. It has saved thousands of lives.",
                "lesson": "This is 'medical AI' — one of the most impactful and well-funded areas in ML right now.",
                "emoji": "🏥"
            },
            {
                "problem": "Banks were losing ₹1,000 crore per year to credit card fraud — human fraud analysts couldn't review every transaction in time.",
                "why_it_happened": "Millions of transactions happen every second. Manual review is too slow.",
                "how_engineers_fixed_it": "ML engineers built a fraud detection model that analyses every transaction in 50 milliseconds — checking location, merchant type, amount, and pattern against previous behaviour — and flags suspicious ones automatically.",
                "lesson": "This is 'real-time ML' — models that make decisions faster than any human ever could.",
                "emoji": "💳"
            },
            {
                "problem": "Farmers in India lose 30% of crops to pests they don't detect early enough.",
                "why_it_happened": "A farmer with 10 acres cannot inspect every plant daily. By the time pest damage is visible, it's too late.",
                "how_engineers_fixed_it": "An ML engineer built an app: take a photo of a leaf, and the AI identifies the pest or disease in 2 seconds, with treatment recommendations in Hindi. Used by 4 million farmers now.",
                "lesson": "ML is not just for tech companies — it's solving India-specific problems that affect hundreds of millions of people.",
                "emoji": "🌾"
            },
        ],
        "personality_fit": [
            "You've wondered 'how does Spotify know I'd like this song I've never heard?'",
            "You enjoy finding patterns — in data, in behaviour, in how things work",
            "You're comfortable with maths and actually find statistics interesting",
            "You like experiments — trying different approaches and measuring which works best",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "Check model metrics", "detail": "The fraud detection model's precision dropped 2% overnight. You open the dashboard to investigate what changed.", "mood": "detective"},
            {"time": "10:00 AM", "task": "Data exploration", "detail": "You load yesterday's transactions into a Jupyter notebook. Plot distributions. A new merchant category was added — the model has never seen it.", "mood": "research"},
            {"time": "11:30 AM", "task": "Retrain the model", "detail": "Include the new data, retrain, compare metrics. New model: +4% recall, same precision. You've improved the model without touching a line of the model code.", "mood": "focus"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "Walk outside if possible. Your brain solves problems in the background when you're not staring at a screen.", "mood": "break"},
            {"time": "2:00 PM", "task": "Code review", "detail": "A colleague's feature has a data leakage bug — they're accidentally using future data to train the model. You catch it before it ships.", "mood": "team"},
            {"time": "3:30 PM", "task": "Experiment: try new approach", "detail": "You test a gradient boosted model against the current neural net. Log all results in MLflow so you can compare later.", "mood": "creative"},
            {"time": "5:30 PM", "task": "Write up findings", "detail": "Document what you tried, what worked, and why. Good ML engineers are also good writers — reproducibility matters.", "mood": "win"},
        ],
        "tools": ["Python (NumPy, Pandas, PyTorch)", "Jupyter Notebook", "MLflow / W&B (experiment tracking)", "SQL + Spark (big data)", "Hugging Face (pre-trained models)", "Docker + Kubernetes", "AWS SageMaker / GCP Vertex AI"],
        "reality_check": "60–70% of your time is spent on data — cleaning it, understanding it, fixing broken pipelines. Only 10% is actually training models. The most important skill is not knowing fancy algorithms — it's knowing which simple one to try first.",
        "salary_snapshot": "Fresher: ₹10–20 LPA. Senior ML engineer after 5 years: ₹40–100 LPA. AI is the highest-paying engineering specialisation globally.",
        "youtube_search": "day in the life machine learning engineer",
        
    },

    "MECH": {
        "tagline": "Every physical thing you trust with your life — your car's brakes, the aircraft you fly in, the building you sit in — a mechanical engineer designed it.",
        "real_apps": [
            {
                "app": "Designing a suspension system from scratch",
                "emoji": "🔩",
                "what_they_built": "A mechanical engineering project in the automotive domain: given a vehicle weight, road profile (Indian potholes included), and speed range, design a suspension that keeps the tyre in contact with the road and the passenger comfortable. You model the spring-damper system mathematically, simulate it in MATLAB, then validate with FEA. This is a real final-year project type — and Tata Motors hires engineers who can do exactly this.",
                "cool_fact": "The suspension geometry on the Tata Nexon EV was specifically redesigned from the ICE version because the battery pack adds 300 kg of weight sitting low in the chassis — changing the entire centre-of-gravity calculation."
            },
            {
                "app": "Building a working heat exchanger prototype",
                "emoji": "🌡️",
                "what_they_built": "A core mechanical engineering project: design a shell-and-tube heat exchanger that cools industrial oil from 90°C to 40°C using water as the coolant. Calculate the required heat transfer area using LMTD method, select tube diameter and shell diameter, choose material (copper vs stainless steel), then build and test. Real thermal engineering used in every chemical plant, power station, and data centre in India.",
                "cool_fact": "Every data centre needs massive heat exchangers to remove the heat generated by servers. A Hyderabad hyperscale data centre uses more cooling water per day than a small town."
            },
            {
                "app": "Designing the Chandrayaan-3 lander legs",
                "emoji": "🚀",
                "what_they_built": "ISRO mechanical engineers designed the lander legs to absorb touchdown impact at 2 m/s on unknown terrain without bouncing or tipping. They ran finite element analysis simulations with thousands of different soil stiffness assumptions — because nobody knows exactly what the lunar surface feels like — and designed legs that survive the worst case. Then built them from aluminium honeycomb composite for minimum weight.",
                "cool_fact": "The lander legs each weigh under 3 kg but absorb a force equivalent to the lander slamming into a surface at 7 km/h — spread across 4 legs simultaneously. Getting the energy absorption wrong by 10% means the lander bounces or tips over."
            },
            {
                "app": "EV battery thermal management system",
                "emoji": "🔋",
                "what_they_built": "A real mechanical engineering project for Indian conditions: design a cooling system that keeps lithium-ion cells between 20°C and 40°C when ambient temperature is 48°C. Design glycol-water channels that run between cell modules, calculate flow rate needed, select pump and radiator, simulate steady-state and transient temperature using CFD. This exact project gets mechanical engineers hired at Tata, Ola Electric, and Ather.",
                "cool_fact": "Ola Electric's S1 Pro scooter battery thermal system was designed to handle Rajasthan summers. Getting it wrong — as some early EV manufacturers did — causes cells to swell, catch fire, or lose 40% capacity after 1 year."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Physics: Newton's laws, forces, motion, friction",
                "becomes_in_engineering": "Engineering Mechanics — calculating whether a bridge, car frame, or rocket nozzle will survive the forces acting on it",
                "emoji": "⚖️"
            },
            {
                "knew_in_12th": "Physics: heat, thermodynamics, laws of heat transfer",
                "becomes_in_engineering": "Designing engines, cooling systems, heat exchangers — anything involving energy conversion",
                "emoji": "🌡️"
            },
            {
                "knew_in_12th": "Maths: calculus, integration, differential equations",
                "becomes_in_engineering": "Structural analysis and fluid dynamics — the maths that predicts how materials deform and how fluids flow",
                "emoji": "📐"
            },
            {
                "knew_in_12th": "Engineering Drawing / technical drawing class",
                "becomes_in_engineering": "CAD software (SolidWorks, CATIA) — the same thinking, but in 3D on a computer with millimetre-level precision",
                "emoji": "✏️"
            },
        ],
        "real_problems": [
            {
                "problem": "Early electric vehicles in India had batteries that swelled, overheated, and sometimes caught fire in summer.",
                "why_it_happened": "Lithium-ion batteries degrade rapidly above 45°C. Indian summers regularly hit 48°C. Nobody had designed the thermal management properly.",
                "how_engineers_fixed_it": "Mechanical engineers designed active liquid cooling systems — channels filled with glycol-water coolant running between battery cells, like a radiator for your battery. The Tata Nexon EV now operates safely at 50°C ambient.",
                "lesson": "This is 'thermal management' — one of the fastest-growing fields in EV engineering in India.",
                "emoji": "🔋"
            },
            {
                "problem": "A suspension bracket on a production car was failing after 80,000 km — causing dangerous wobble at highway speeds.",
                "why_it_happened": "A sharp corner in the bracket design created a stress concentration point — the metal fatigued and cracked there predictably.",
                "how_engineers_fixed_it": "Running FEA (Finite Element Analysis) revealed the exact failure point. Adding a 3mm fillet (rounded corner) at that point distributed the stress across a larger area. The part now lasts 200,000 km. Cost to fix: ₹12 per part.",
                "lesson": "Sometimes a ₹12 change in geometry prevents a ₹50,000 recall. This is why FEA is the most valued skill in mechanical engineering.",
                "emoji": "🔩"
            },
            {
                "problem": "A chemical plant's heat exchanger was running at 75% efficiency instead of the designed 95% — costing ₹2 crore per year in wasted energy.",
                "why_it_happened": "Nobody had cleaned it for 18 months. Mineral deposits had coated the heat transfer surfaces, acting as insulation.",
                "how_engineers_fixed_it": "A maintenance schedule was implemented. The engineer also redesigned the water treatment system to prevent deposits. Efficiency restored. Annual savings: ₹1.8 crore.",
                "lesson": "Mechanical engineering is not just design — maintenance and operational optimisation are equally valued.",
                "emoji": "🏭"
            },
        ],
        "personality_fit": [
            "You enjoy taking things apart to understand how they work — and actually putting them back together",
            "You've wondered how a car engine works, or why a plane doesn't fall out of the sky",
            "You like drawing, building, making physical things — not just looking at a screen",
            "You find satisfaction in something that works in the real world — not just on a computer",
        ],
        "day_timeline": [
            {"time": "8:30 AM", "task": "Factory floor inspection", "detail": "A suspension bracket keeps failing after 5,000 assembly cycles. You go to the floor and inspect the physical parts — looking for patterns in where they crack.", "mood": "detective"},
            {"time": "9:30 AM", "task": "FEA simulation", "detail": "Back at your desk. Open ANSYS, apply the exact forces measured on the floor. The simulation highlights a stress concentration at a sharp corner. Found it.", "mood": "research"},
            {"time": "11:00 AM", "task": "Design review", "detail": "Present FEA results to the team. Propose adding a fillet radius. Everyone agrees. You update the drawing in SolidWorks.", "mood": "team"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "Factory cafeteria. Most manufacturing engineers eat with the production team — you learn more about real problems at lunch than in meetings.", "mood": "break"},
            {"time": "2:00 PM", "task": "Update drawing & send to workshop", "detail": "Revise the SolidWorks model, generate engineering drawings with tolerances, send to the workshop. A prototype will be ready in 3 days.", "mood": "focus"},
            {"time": "3:30 PM", "task": "Vendor call", "detail": "Review material test certificates for a new aluminium alloy. Check tensile strength, yield strength, and elongation against your design requirements.", "mood": "research"},
            {"time": "5:00 PM", "task": "Documentation", "detail": "Update the design change log. Every engineering change is documented — future engineers (or lawyers, if something fails) need to understand what was changed and why.", "mood": "win"},
        ],
        "tools": ["SolidWorks / CATIA / AutoCAD (3D modelling)", "ANSYS (stress, thermal, fluid simulation)", "MATLAB / Simulink (dynamics & control)", "GD&T (technical drawing standards)", "Excel / Python (data analysis)", "PLM software (managing design files)"],
        "reality_check": "The first 2 years are often repetitive — updating drawings, running standardised tests, writing reports. This is normal and necessary. Senior mech engineers who can also simulate (FEA/CFD) and code Python are extremely rare and very highly paid. That combination is your goal.",
        "salary_snapshot": "Fresher at core company: ₹4–8 LPA. Senior engineer at Bosch / ISRO / Tata after 7 years: ₹18–35 LPA. EV sector is paying significantly more now.",
        "youtube_search": "day in the life mechanical engineer",
        
    },

    "ECE": {
        "tagline": "The chip inside your phone, the antenna on the tower giving you 5G, the sensor in your smartwatch — an electronics engineer designed them.",
        "real_apps": [
            {
                "app": "Designing a PCB from scratch — IoT weather station",
                "emoji": "🌤️",
                "what_they_built": "A real ECE project: design a circuit board that reads temperature, humidity, and air quality from sensors, processes the data on an STM32 microcontroller, and transmits it over WiFi to a server — all running on a solar-charged battery for 6 months with no maintenance. You design the schematic (which components, how they connect), lay out the PCB (where each component sits on the board), write the firmware in C, and test with an oscilloscope.",
                "cool_fact": "ISRO deployed a network of 1,200 such IoT weather stations across India's river basins to provide early flood warnings. Each station was designed and built by ECE engineers — the entire sensor-to-server pipeline."
            },
            {
                "app": "Building a VLSI chip in Verilog — digital design project",
                "emoji": "⚙️",
                "what_they_built": "In a VLSI design project, you describe an entire digital circuit — like a 32-bit ALU (arithmetic logic unit, the heart of a CPU) — in Verilog hardware description language. You simulate it, verify timing, synthesise it to logic gates, then map it to an FPGA. Companies like Qualcomm and Intel interview specifically for this skill — being able to think in hardware, not just software.",
                "cool_fact": "The RISC-V instruction set — an open-source CPU architecture now used in ISRO satellites, Indian government chips, and hundreds of startups — was designed in Verilog by ECE engineers at UC Berkeley and is now being implemented by engineers at IIT Madras for India's domestic chip program."
            },
            {
                "app": "5G antenna array design",
                "emoji": "📡",
                "what_they_built": "5G uses a technology called Massive MIMO — instead of one antenna, a tower has 64 or 128 antenna elements that can beam signals precisely toward individual users. ECE engineers design the geometry of these antenna arrays, calculate the radiation patterns, and tune the beamforming algorithms that decide how to focus the signal. This is applied electromagnetics — the same Maxwell's equations you study in 12th physics, at industrial scale.",
                "cool_fact": "A single 5G Massive MIMO antenna panel can serve 100 users simultaneously by pointing individual beams at each user — like a spotlight instead of a floodlight. Jio's rollout used panels designed partly by ECE engineers from IIT Bombay and BITS Pilani."
            },
            {
                "app": "Embedded firmware for ISRO PSLV",
                "emoji": "🚀",
                "what_they_built": "The flight computer aboard a PSLV rocket runs firmware written in embedded C by ECE engineers. It reads 200+ sensors every millisecond, runs control algorithms that keep the rocket on trajectory, and makes microsecond decisions to fire attitude thrusters. The firmware must work perfectly the first time — there is no patch deployment at 70 km altitude.",
                "cool_fact": "PSLV-C58, launched in January 2024, carried the XPoSat X-ray astronomy satellite. Its embedded systems were designed at ISRO's Space Electronics Centre in Bengaluru — one of the top career destinations for ECE graduates from NIT Warangal, IIT Bombay, and Pune colleges."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Physics: electric circuits, Ohm's law, capacitors, inductors",
                "becomes_in_engineering": "Analog circuit design — designing the amplifiers, filters, and power circuits inside every electronic device",
                "emoji": "⚡"
            },
            {
                "knew_in_12th": "Physics: electromagnetic waves, light, optics",
                "becomes_in_engineering": "Communication systems and RF engineering — how signals travel through the air as waves and are received by antennas",
                "emoji": "📡"
            },
            {
                "knew_in_12th": "Maths: Fourier series, signals, differential equations",
                "becomes_in_engineering": "Digital Signal Processing — how to filter noise, compress audio/video, and extract information from sensor readings",
                "emoji": "〜"
            },
            {
                "knew_in_12th": "Computer Science / programming basics",
                "becomes_in_engineering": "Embedded C programming — writing firmware that runs directly on hardware with no operating system between your code and the chip",
                "emoji": "💾"
            },
        ],
        "real_problems": [
            {
                "problem": "An IoT sensor deployed in 10,000 farms was randomly rebooting every 2-3 days — making it useless for farmers who needed continuous soil moisture data.",
                "why_it_happened": "A slow memory leak in the firmware — the RAM gradually filled up until the microcontroller crashed and restarted.",
                "how_engineers_fixed_it": "The ECE engineer added heap memory monitoring that logged usage every hour to flash memory. After 48 hours, the log showed RAM growing by 200 bytes per hour. Found the bug: a buffer that was allocated but never freed in the sensor reading loop. Fixed in 20 minutes.",
                "lesson": "In embedded systems, you debug with oscilloscopes and log files, not IDE debuggers. The skill is systematically instrumenting your code.",
                "emoji": "🌱"
            },
            {
                "problem": "A PCB that passed all tests in the lab mysteriously failed 30% of the time in the field — but only near kitchen appliances.",
                "why_it_happened": "Microwave ovens emit strong electromagnetic interference at 2.45 GHz — exactly where the PCB's Wi-Fi module operated. The PCB had no RF shielding.",
                "how_engineers_fixed_it": "Added a metal shield can over the Wi-Fi module on the PCB. Redesigned the ground plane for better EMI isolation. Added software-side channel hopping. Field failure rate dropped from 30% to 0.1%.",
                "lesson": "Real-world electronics engineering involves electromagnetic compatibility (EMC) — making sure your device works in the same room as other devices.",
                "emoji": "🔌"
            },
            {
                "problem": "A new chip design failed to boot correctly 15% of the time after production — costing the company ₹50 crore in defective chips.",
                "why_it_happened": "The 1.8V power rail had voltage spikes during startup. The chip's internal logic was seeing incorrect voltage levels and misreading initial values.",
                "how_engineers_fixed_it": "VLSI engineers added decoupling capacitors closer to the power pins in a PCB redesign, and added a soft-start circuit to slow the power ramp rate. Boot failure rate dropped to 0.001%.",
                "lesson": "Power integrity is one of the most critical and underappreciated skills in hardware design.",
                "emoji": "⚙️"
            },
        ],
        "personality_fit": [
            "You've opened up a broken device to see what's inside — and weren't satisfied until you understood at least one component",
            "Physics circuits chapter was actually interesting to you — not just something to memorise",
            "You're drawn to things that work at the boundary of hardware and software",
            "You find it satisfying to make something physically work — LEDs blinking, motors turning, sensors reading",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "Scope out the power rail", "detail": "The IoT board is randomly rebooting. Plug in the oscilloscope and capture the 3.3V rail. There it is — a 400mV spike every time the WiFi transmits.", "mood": "detective"},
            {"time": "10:00 AM", "task": "PCB redesign", "detail": "Open KiCAD. Move the decoupling capacitors closer to the WiFi chip's power pins. Add a larger bulk capacitor. Update the PCB layout.", "mood": "focus"},
            {"time": "11:30 AM", "task": "Write embedded firmware", "detail": "Implement the power-save mode in C — put the sensor to sleep between readings. Target: battery life from 6 months to 18 months.", "mood": "creative"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "The lab smells like solder and coffee. Hardware engineers often eat together — good place to ask 'has anyone dealt with this before?'", "mood": "break"},
            {"time": "2:00 PM", "task": "Test firmware on dev board", "detail": "Flash the new code, measure sleep current with a precision ammeter. 8 microamps. Perfect — matches the target. Document the measurement.", "mood": "win"},
            {"time": "3:30 PM", "task": "Design review meeting", "detail": "Present the power rail fix and battery life improvement to the team. Someone asks about the antenna placement — that's tomorrow's problem.", "mood": "team"},
            {"time": "5:00 PM", "task": "Send Gerbers to PCB manufacturer", "detail": "Export the PCB design files. 3-day lead time for prototype boards. You'll test the fix when they arrive.", "mood": "focus"},
        ],
        "tools": ["KiCAD / Altium (PCB design)", "Oscilloscope + Multimeter + Logic Analyser", "Keil / STM32CubeIDE (embedded firmware)", "Xilinx Vivado (FPGA / Verilog)", "LTSpice / Proteus (circuit simulation)", "Python / MATLAB (signal analysis)"],
        "reality_check": "Hardware bugs can take days to find. A software bug is fixed by editing a file; a hardware bug means redesigning and manufacturing a new board — which takes days and costs money. This is why ECE engineers are extremely methodical. The best ECE engineers think in hardware AND software simultaneously — that combination is rare and extremely well-paid.",
        "salary_snapshot": "Fresher at embedded/VLSI company: ₹5–10 LPA. Senior VLSI engineer at Qualcomm/Intel after 7 years: ₹30–70 LPA.",
        "youtube_search": "day in the life electronics embedded engineer",
        
    },
    "CIVIL": {
        "tagline": "Your designs are permanent — every bridge, road, and building you create outlives you by a century.",
        "real_apps": [
            {
                "app": "Designing the Pune Metro viaduct from scratch",
                "emoji": "🚇",
                "what_they_built": "The elevated viaduct columns for Pune Metro Phase 1 were designed by civil structural engineers who calculated the exact load from trains, wind, and earthquakes — then specified the column dimensions, reinforcement steel layout, and foundation depth. Each column carries 1000+ tonnes. Getting it wrong by even 5% could cause catastrophic failure.",
                "cool_fact": "Pune Metro's Reach-1 viaduct uses 35,000 tonnes of structural steel — more than the Eiffel Tower. Every beam dimension was calculated and drawn by civil engineers."
            },
            {
                "app": "Mumbai-Pune Expressway — cutting through the Western Ghats",
                "emoji": "🛣️",
                "what_they_built": "The 6 tunnels and 15 major bridges on the Mumbai-Pune Expressway required civil engineers to analyse rock strata using boreholes, design tunnel support systems for different rock types, and calculate slope stability for every cut made into the Ghats. The expressway reduced travel time from 4 hours to 2 — a direct result of civil engineering.",
                "cool_fact": "The Khopoli bypass tunnel required a completely different design from the Amby Valley tunnel even though they are 2 km apart — the rock quality changed completely."
            },
            {
                "app": "Building a city's water supply network",
                "emoji": "💧",
                "what_they_built": "Pune's water supply system delivers 1,350 MLD (million litres per day) to 40 lakh residents through 2,800 km of pipelines. Civil engineers designed the treatment plants, pump stations, reservoir locations, and pipe diameters — calculating hydraulic gradients to ensure water reaches every floor in every building by gravity wherever possible.",
                "cool_fact": "The Katraj-Pune water supply main was designed in 1878 by British civil engineers. 146 years later, it still carries water to parts of old Pune — a testament to how permanent civil engineering designs are."
            },
            {
                "app": "IIT Bombay main building — earthquake-resistant structure",
                "emoji": "🏛️",
                "what_they_built": "Every large building in India's seismic zones (Pune is Zone III, Mumbai is Zone III) must be designed to survive an earthquake without collapse. Structural civil engineers design special column-beam connections, shear walls, and base isolators that absorb earthquake energy before it reaches the structure. IIT Bombay's main building was one of India's first to use modern earthquake-resistant structural design.",
                "cool_fact": "Japan has 6.2 magnitude earthquakes almost weekly — but buildings rarely collapse. This is entirely because of civil structural engineering standards enforced since 1981."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Physics: Newton's laws, forces, equilibrium",
                "becomes_in_engineering": "Structural analysis — calculating whether a beam, column, or truss will carry the applied loads without failing",
                "emoji": "⚖️"
            },
            {
                "knew_in_12th": "Physics: fluid pressure, Bernoulli's principle",
                "becomes_in_engineering": "Hydraulic engineering — designing dams, water supply systems, drainage networks, and flood control channels",
                "emoji": "💧"
            },
            {
                "knew_in_12th": "Maths: geometry, trigonometry, coordinate geometry",
                "becomes_in_engineering": "Surveying and setting out — measuring and marking the exact positions of structures on the ground before construction begins",
                "emoji": "📐"
            },
            {
                "knew_in_12th": "Chemistry: properties of materials, reactions",
                "becomes_in_engineering": "Concrete technology and material science — understanding why concrete gains strength, why steel rusts, and how to design durable structures for 100-year lifespans",
                "emoji": "🧱"
            },
        ],
        "real_problems": [
            {
                "problem": "A newly completed flyover in Pune started showing hairline cracks in the deck slab just 8 months after opening.",
                "why_it_happened": "The concrete mix design did not account for the high sulphate content in Pune's local aggregates. Sulphate attack causes gradual chemical deterioration of concrete from within.",
                "how_engineers_fixed_it": "Structural engineers tested the concrete core samples, confirmed sulphate attack, and specified Sulphate Resistant Cement (SRC) for all repair work and future pours. The affected sections were removed and reconstructed with the correct mix design.",
                "lesson": "Concrete mix design is not generic — it must be designed for the specific local materials, water quality, and environmental conditions of each project site.",
                "emoji": "🏗️"
            },
            {
                "problem": "A residential colony in a new part of Pune flooded every monsoon even though it had a drainage system designed by an engineer.",
                "why_it_happened": "The drainage system was designed using old rainfall data from 1990. Pune's annual rainfall has increased significantly since then, and the 30-year-old design could not handle modern monsoon intensities.",
                "how_engineers_fixed_it": "Civil engineers updated the hydrological analysis using recent 20-year rainfall data, redesigned the storm water drains for the new peak discharge, and added retention ponds to temporarily hold excess water during peak rain events.",
                "lesson": "Infrastructure must be designed for future conditions, not historical averages. Climate change is making rainfall more intense and unpredictable — civil engineers now routinely design for climate-adjusted scenarios.",
                "emoji": "🌧️"
            },
            {
                "problem": "A 5-storey building under construction in Pune was visibly tilting to one side at the 3rd floor level.",
                "why_it_happened": "The geotechnical investigation before construction found uniform soil across the site. But an undetected old abandoned well existed under one corner, causing differential settlement — one side of the foundation sank more than the other.",
                "how_engineers_fixed_it": "Construction was stopped immediately. Geotechnical engineers drilled investigation boreholes, located the old well, and designed a remediation: grouting (injecting cement slurry) to fill the void, then constructing a raft foundation to spread the load uniformly across a larger area.",
                "lesson": "Site investigation is the most critical phase of any civil project. Hidden underground features — old wells, filled ponds, soft clay pockets — are the most common cause of foundation failures in Indian cities.",
                "emoji": "🔍"
            },
        ],
        "personality_fit": [
            "You find satisfaction in things that are permanent — you want to build something that will still be there in 50 years",
            "You enjoy both the physical and technical sides of work — you're as comfortable on a construction site as at a drawing desk",
            "You are a good communicator — civil engineers spend as much time coordinating with contractors, clients, and government officials as doing technical work",
            "You can visualise 3D structures from 2D drawings — spatial thinking comes naturally to you",
        ],
        "day_timeline": [
            {"time": "8:00 AM", "task": "Site inspection", "detail": "Walk the under-construction flyover. Check that yesterday's concrete pour has achieved its target strength (measured with a rebound hammer). Identify one column where the formwork is not perfectly aligned — you flag it before concrete is poured.", "mood": "detective"},
            {"time": "9:30 AM", "task": "Design check", "detail": "Back at the site office. Review the shop drawings for the next week's steel reinforcement work. Spot a bar diameter discrepancy — the drawing says 20mm bars but the supplied bars are 16mm. Send a non-conformance notice immediately.", "mood": "focus"},
            {"time": "11:00 AM", "task": "Client meeting", "detail": "The client (MSRDC) wants to know why this section is 3 days behind schedule. You explain the rain delay and the material non-conformance — and present a revised programme showing you can recover the delay in 2 weeks.", "mood": "team"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "On site. Usually a box lunch because you rarely leave a live construction site during work hours. You eat with the site foreman and get informal updates about material delivery delays.", "mood": "break"},
            {"time": "2:00 PM", "task": "Design work", "detail": "Work on STAAD.Pro model for the new pedestrian bridge. Add the wind load case — Pune's design wind speed is 44 m/s. Check that the connection at the mid-span is not overstressed.", "mood": "research"},
            {"time": "4:00 PM", "task": "Progress report", "detail": "Update the project schedule in Primavera. Mark 3 activities complete. Flag one critical path activity that is at risk due to delayed material delivery.", "mood": "focus"},
            {"time": "5:30 PM", "task": "Documentation", "detail": "Sign off on the day's pour records, quality test results, and material delivery receipts. Every document is legally important — they form the basis of payment certificates.", "mood": "win"},
        ],
        "tools": ["AutoCAD Civil 3D (site drawings & road design)", "STAAD.Pro / ETABS (structural analysis)", "Revit BIM (3D building models)", "Primavera P6 / MS Project (scheduling)", "MATLAB / Python (hydraulic modelling)", "AutoCAD (general 2D drawings)"],
        "reality_check": "Civil engineering has the most variety of any engineering branch — you can work on roads, buildings, bridges, dams, airports, water supply, or smart cities. The first 2 years on site are physically demanding and often bureaucratic. But senior civil engineers have enormous responsibility — and enormous impact. When you drive on a road you designed, it is unlike any other professional feeling.",
        "salary_snapshot": "Fresher at L&T / government: ₹3.5–7 LPA. Senior project engineer after 7 years: ₹18–35 LPA. Project Director (15+ years): ₹50–80 LPA.",
        "youtube_search": "day in the life civil engineer India site",
    },

    "CHEM": {
        "tagline": "You design the industrial processes that turn crude oil into petrol, sugarcane into medicine, and wastewater into clean water.",
        "real_apps": [
            {
                "app": "Designing a pharmaceutical drug manufacturing process",
                "emoji": "💊",
                "what_they_built": "When a new cancer drug is discovered in a laboratory, the synthesis uses 50 ml flasks and produces 1 gram of product. A chemical engineer's job is to scale this up to produce 10,000 kg per month in a factory — while maintaining the exact same purity. This requires redesigning every step: reactor size, temperature control, solvent recovery, purification column dimensions, and waste treatment.",
                "cool_fact": "India supplies 20% of the world's generic medicines. Every tablet you take was made in a process designed by chemical engineers. Pune's pharmaceutical cluster (Bhosari, Pimpri) employs thousands of chemical engineers."
            },
            {
                "app": "Petroleum refinery — turning crude oil into useful products",
                "emoji": "⛽",
                "what_they_built": "A crude oil refinery takes black, smelly crude oil and separates it into petrol, diesel, kerosene, LPG, and hundreds of industrial chemicals — all through a series of distillation columns, catalytic reactors, and heat exchangers designed by chemical engineers. The Mumbai High offshore crude that fuels Maharashtra's vehicles has been processed by Indian chemical engineers at HPCL and BPCL.",
                "cool_fact": "A single refinery processes 200,000 barrels of crude oil per day — that is 31 million litres. The entire distillation system operates 24/7 for 3 years between scheduled shutdowns. Chemical engineers design for zero unplanned stops."
            },
            {
                "app": "Wastewater treatment — making industrial waste safe",
                "emoji": "🌊",
                "what_they_built": "Every pharmaceutical, chemical, and food factory in India must treat its wastewater before discharging it. Chemical engineers design the treatment system — biological reactors, chemical dosing systems, membrane filters, and sludge dewatering units — that reduce toxic chemical concentrations from thousands of ppm down to levels safe for rivers. MIDC Pimpri-Chinchwad's common effluent treatment plant was designed by chemical engineers.",
                "cool_fact": "The Mula-Mutha river pollution crisis led the MPCB (Maharashtra Pollution Control Board) to mandate advanced wastewater treatment for all Pune industrial estates. The engineers who designed those systems directly protected the river."
            },
            {
                "app": "Agrochemical / fertilizer production",
                "emoji": "🌾",
                "what_they_built": "The urea fertilizer used by Indian farmers is produced in a chemical plant where nitrogen from the air reacts with hydrogen (from natural gas) at 450°C and 200 atmospheres pressure. Chemical engineers designed the reactor, the heat recovery system, the gas purification trains, and the safety shutdown system that prevents catastrophic runaway reactions.",
                "cool_fact": "The Haber-Bosch process for making ammonia (used in fertilizers) is considered the single most important chemical engineering achievement in history. It feeds half the world's population. Without it, Earth could only support 4 billion people instead of 8 billion."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Chemistry: chemical reactions, rates, equilibrium (Le Chatelier's principle)",
                "becomes_in_engineering": "Chemical Reaction Engineering — designing industrial reactors where you control temperature, pressure, and concentration to maximise product yield and minimise unwanted byproducts",
                "emoji": "⚗️"
            },
            {
                "knew_in_12th": "Physics: thermodynamics (heat, work, efficiency)",
                "becomes_in_engineering": "Chemical Process Thermodynamics — calculating how much energy every process step requires, designing heat exchangers to recover wasted heat, and optimising energy efficiency across an entire plant",
                "emoji": "🌡️"
            },
            {
                "knew_in_12th": "Physics: fluid mechanics (pressure, flow, Bernoulli)",
                "becomes_in_engineering": "Transport phenomena and fluid flow in pipes, pumps, and reactors — ensuring that chemicals flow at the right rate and pressure through every part of the plant",
                "emoji": "💧"
            },
            {
                "knew_in_12th": "Maths: differential equations, calculus",
                "becomes_in_engineering": "Process modelling and simulation — writing equations that describe how a reactor or distillation column behaves over time and using software like Aspen HYSYS to simulate an entire plant before it is built",
                "emoji": "📊"
            },
        ],
        "real_problems": [
            {
                "problem": "A pharmaceutical plant's distillation column was producing a drug ingredient at only 89% purity instead of the required 99.5%. The drug batch had to be scrapped — a ₹2 crore loss.",
                "why_it_happened": "The reflux ratio (the ratio of liquid returned to the column vs liquid taken as product) had been reduced to save energy. This reduced separation efficiency enough to allow impurities to slip through into the product.",
                "how_engineers_fixed_it": "The chemical engineer ran Aspen HYSYS simulations to find the minimum reflux ratio that still achieved 99.5% purity, then installed automatic reflux ratio control tied to the online purity analyser. The column now self-adjusts when purity drifts.",
                "lesson": "Every change to an operating parameter in a chemical plant has consequences for product quality. Chemical engineers must understand the full thermodynamic system — not just the equipment.",
                "emoji": "🏭"
            },
            {
                "problem": "A batch reactor producing a specialty chemical kept overheating dangerously during one specific reaction step — even though the cooling system was working.",
                "why_it_happened": "The reaction was exothermic (releases heat). At lab scale (5 litres), the surface area to volume ratio was high enough that the cooling jacket could remove heat fast enough. At plant scale (5000 litres), the volume is 1000× larger but the surface area only 100× larger — so heat accumulates much faster than it can be removed.",
                "how_engineers_fixed_it": "The chemical engineer redesigned the reactor with internal cooling coils (not just a jacket), installed a feed rate controller that slows down reagent addition if temperature rises above a threshold, and added a high-temperature emergency quench system.",
                "lesson": "Scale-up is the most dangerous phase of chemical plant design. Reactions that are safe in a lab can become runaway — even explosive — at industrial scale if the heat balance is not carefully re-engineered.",
                "emoji": "⚠️"
            },
            {
                "problem": "A specialty chemical plant's final product consistently showed 2–3% impurity of an unknown compound, failing the customer's specification.",
                "why_it_happened": "A minor side reaction was occurring in the reactor at high temperature — one that had never been observed at lab scale because the lab never ran at temperatures above 80°C. At plant temperatures of 120°C, the side reaction produced an unexpected byproduct.",
                "how_engineers_fixed_it": "The engineer ran controlled experiments at different temperatures, identified the side reaction mechanism, and redesigned the process to run at 75°C using a catalyst instead of high temperature. Impurity dropped below 0.1%.",
                "lesson": "Laboratory chemistry and industrial chemistry are not the same. Temperature, pressure, mixing, and residence time all interact in complex ways at plant scale. Chemical engineers must anticipate these interactions before they cause problems.",
                "emoji": "🔬"
            },
        ],
        "personality_fit": [
            "Chemistry and physics were interesting to you — you understand how molecules behave and why reactions happen",
            "You are comfortable with mathematics — chemical engineering has more differential equations than any other engineering branch",
            "You like systematic thinking — process engineering is about understanding systems, not just individual pieces of equipment",
            "You are patient — industrial processes take time to optimise and problems often take days of careful analysis to solve",
        ],
        "day_timeline": [
            {"time": "7:00 AM", "task": "Daily plant walkthrough", "detail": "Walk through the reactor area, distillation section, and utility systems. Check pressure gauges, temperature indicators, and flow meters visually. Something always looks slightly different from yesterday — today the pressure drop across one heat exchanger is higher than normal.", "mood": "detective"},
            {"time": "8:30 AM", "task": "Morning production meeting", "detail": "Daily operations meeting: last 24 hours production vs target, quality results, any safety incidents. You report the high pressure drop — it likely indicates fouling in the heat exchanger. Maintenance team is asked to plan a cleaning for the weekend shutdown.", "mood": "team"},
            {"time": "10:00 AM", "task": "Process troubleshooting", "detail": "The distillation column product purity has slipped to 97.8% (spec is 98.5%). Open Aspen HYSYS simulation. Run different scenarios — feed composition change? Temperature drift? Confirm it correlates with the high pressure drop in the upstream heat exchanger: less heat exchange = cooler feed = less separation.", "mood": "research"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "Plant canteens are excellent. Chemical plant operators and engineers eat together — the best process knowledge comes from the operators who have watched the plant for 20 years.", "mood": "break"},
            {"time": "2:00 PM", "task": "Process safety review", "detail": "Monthly HAZOP review. The team analyses what happens if the cooling water to Reactor R-102 fails. You identify a new protection layer needed: a high-temperature interlock that automatically stops the reagent feed. Document in the action register.", "mood": "focus"},
            {"time": "4:00 PM", "task": "Simulation and optimisation", "detail": "Run Aspen simulation to find the optimal operating temperature for next month's product — the customer wants a different viscosity specification. Find that 118°C instead of 120°C reduces the side reaction and meets the new spec.", "mood": "creative"},
            {"time": "5:30 PM", "task": "Handover", "detail": "Write the shift handover report for the night shift engineer. Note the heat exchanger pressure drop issue and the purity recovery plan. Include a clear instruction: if purity drops below 97%, hold product for QC review before sending to tank farm.", "mood": "win"},
        ],
        "tools": ["Aspen HYSYS / Aspen Plus (process simulation)", "AutoCAD P&ID (process diagrams)", "MATLAB / Python (modelling)", "HAZOP worksheets", "DCS / SCADA (plant control systems)", "Six Sigma tools (DMAIC, control charts)"],
        "reality_check": "Chemical engineering is one of the most intellectually demanding engineering branches — it combines chemistry, physics, thermodynamics, fluid mechanics, and economics simultaneously. The first job often involves shift work in a plant environment. But the problem-solving is genuinely interesting, the impact is tangible, and senior chemical engineers are among the highest-paid engineers in the PSU and pharmaceutical sectors.",
        "salary_snapshot": "Fresher at Reliance / UPL / Sun Pharma: ₹4–8 LPA. Senior process engineer after 7 years: ₹15–28 LPA. PSU (ONGC, HPCL via GATE): ₹8–12 LPA + perks.",
        "youtube_search": "day in the life chemical engineer plant India",
    },

    "BME": {
        "tagline": "When a doctor diagnoses cancer from an MRI scan, the machine was designed by a biomedical engineer.",
        "real_apps": [
            {
                "app": "Designing the ECG machine in your nearest hospital",
                "emoji": "💓",
                "what_they_built": "The ECG machine that records your heart's electrical activity is a biomedical engineering system: metal electrodes that detect millivolt-level electrical signals from skin, differential amplifiers that separate the heart signal from noise, analog-to-digital converters that digitise the waveform, and signal processing algorithms that measure your heart rate, detect arrhythmias, and flag ST-segment elevation (the warning sign of a heart attack). Every component was designed by a biomedical engineer.",
                "cool_fact": "A hospital-grade ECG must detect signals as small as 0.5 millivolts (0.0005 volts) while the patient is connected to a 220V power outlet just 1 metre away. The shielding and filtering that makes this safe is sophisticated biomedical engineering."
            },
            {
                "app": "Jaipur Foot — India's world-famous prosthetic limb",
                "emoji": "🦿",
                "what_they_built": "The Jaipur Foot prosthetic limb was designed by biomedical engineers to allow Indian amputees to walk barefoot on uneven terrain, squat cross-legged (for toileting and sitting on the floor), and even run. Unlike Western prosthetics designed for shoe use, the Jaipur Foot is specifically biomechanically designed for Indian conditions. It is made from rubber and costs ₹45,000 — vs ₹3 lakh for Western equivalents.",
                "cool_fact": "The Jaipur Foot has been fitted to over 1.3 million people in 26 countries. It was recently redesigned using 3D printing for better fit customisation — the new version takes 45 minutes to fit instead of 1 hour."
            },
            {
                "app": "MRI scanner — seeing inside the body without surgery",
                "emoji": "🧲",
                "what_they_built": "An MRI machine uses a powerful magnetic field (1.5–3 Tesla — 60,000× stronger than Earth's magnetic field) to align hydrogen atoms in your body, then briefly disturbs them with radio waves and listens to how they snap back. Different tissues snap back at different rates, creating contrast in the image. Biomedical engineers designed the superconducting magnet coils, the radio frequency transmitter/receiver, the signal processing chain, and the image reconstruction algorithms.",
                "cool_fact": "The entire MRI machine weighs 8–10 tonnes and operates at -269°C (just 4 degrees above absolute zero) to keep the superconducting magnets working. Yet it produces images of 1mm resolution inside the human body without any radiation."
            },
            {
                "app": "Continuous Glucose Monitor (CGM) worn by diabetic patients",
                "emoji": "⌚",
                "what_they_built": "A CGM is a wearable sensor the size of a 50-paise coin that sits on the arm and measures blood glucose every 5 minutes — without drawing blood. Biomedical engineers designed the glucose oxidase enzyme sensor that reacts with glucose in the interstitial fluid under the skin, the miniaturised signal conditioning electronics, the Bluetooth transmitter, and the calibration algorithm that converts the electrochemical signal to an accurate glucose reading.",
                "cool_fact": "India has 77 million diabetic patients — the second highest in the world. Affordable CGM devices designed specifically for Indian price points (current global devices cost ₹3,000/month) is one of the biggest unsolved BME challenges in India today."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Biology: how the heart pumps blood, how neurons fire, how muscles contract",
                "becomes_in_engineering": "Biomechanics and physiological modelling — treating the human body as an engineering system with pumps, electrical circuits, levers, and sensors, then designing devices that interface with each system",
                "emoji": "🫀"
            },
            {
                "knew_in_12th": "Physics: electricity and circuits (current, voltage, resistance, capacitors)",
                "becomes_in_engineering": "Medical instrumentation — designing the amplifiers, filters, and signal processing circuits that capture and clean up the tiny electrical signals produced by the heart, brain, and muscles",
                "emoji": "⚡"
            },
            {
                "knew_in_12th": "Maths: statistics, probability, data analysis",
                "becomes_in_engineering": "Biomedical signal processing and medical data analysis — separating genuine physiological signals from noise, detecting patterns that indicate disease, and validating that medical devices meet accuracy requirements",
                "emoji": "📊"
            },
            {
                "knew_in_12th": "Chemistry: material properties, reactions, polymers",
                "becomes_in_engineering": "Biomaterials science — selecting and testing materials (metals, ceramics, polymers) that can be implanted in the human body without causing rejection or corrosion inside a living system",
                "emoji": "🧬"
            },
        ],
        "real_problems": [
            {
                "problem": "A hospital reported that their new ultrasound machine produced blurry images for overweight patients — clear images for others.",
                "why_it_happened": "The ultrasound transducer frequency (7.5 MHz) was optimised for imaging at depths of 4–6 cm. For overweight patients, the organs of interest were 10–12 cm deep. At that depth, the 7.5 MHz signal attenuates too much to return a strong echo.",
                "how_engineers_fixed_it": "The biomedical engineer specified a 3.5 MHz transducer option for the same machine. Lower frequency penetrates deeper while sacrificing some resolution — the correct tradeoff for deeper imaging. Modern machines now automatically select frequency based on measured depth.",
                "lesson": "Medical device design must account for the full range of real patients — not just average-sized patients in controlled lab conditions. Inclusive design is both an ethical and engineering requirement.",
                "emoji": "🏥"
            },
            {
                "problem": "A low-cost pulse oximeter developed for rural health workers gave inaccurate SpO2 readings for patients with darker skin tones — overestimating oxygen levels during COVID-19.",
                "why_it_happened": "Pulse oximeters measure blood oxygen by shining red and infrared light through the finger and measuring how much is absorbed. Melanin (darker skin pigment) absorbs some of the red light — causing the device to calculate a falsely high oxygen reading.",
                "how_engineers_fixed_it": "Biomedical engineers redesigned the calibration algorithm using a dataset that included diverse skin tones. They also added a fourth wavelength (green LED) that is less affected by melanin and improves accuracy across skin tones. This directly impacted patient safety during the COVID-19 pandemic.",
                "lesson": "Medical devices trained or calibrated on non-representative patient populations can cause systematic harm to specific groups. Biomedical engineers carry direct ethical responsibility for device safety across all patient demographics.",
                "emoji": "💉"
            },
            {
                "problem": "A titanium bone implant placed in a patient's femur began loosening 2 years after surgery, requiring a painful revision surgery.",
                "why_it_happened": "The implant surface was too smooth — bone cells could not adhere properly to the smooth titanium surface. Without good bone-implant bonding (osseointegration), micro-movement at the interface eventually caused loosening.",
                "how_engineers_fixed_it": "Biomedical engineers developed a porous titanium surface coating using 3D printing (SLM process) — the porous texture mimics the natural roughness of bone and dramatically improves osseointegration. The revised implant design reduced revision surgery rates from 8% to under 1% in 5-year follow-up studies.",
                "lesson": "Biomedical engineering is not just about making something that functions — it must function while living inside a human body, interacting with cells, fluids, and mechanical loads simultaneously, for 15–20 years.",
                "emoji": "🦴"
            },
        ],
        "personality_fit": [
            "You find the intersection of engineering and medicine deeply interesting — the idea of technology that directly saves lives appeals to you",
            "You are comfortable with both biology and electronics — BME requires you to speak the language of both doctors and engineers",
            "You have a research mindset — BME involves a lot of testing, validation, and iterative improvement rather than following established formulas",
            "You care about people — the end user of your design is a patient, and understanding their real-world experience matters as much as the technical specifications",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "Clinical rounds with the medical team", "detail": "Join the cardiology ward round at Sassoon Hospital. The clinical engineer accompanies doctors to understand why two ECG machines are giving inconsistent readings. You notice both have lead wire damage — order replacements and flag for preventive maintenance.", "mood": "team"},
            {"time": "10:30 AM", "task": "Device testing and validation", "detail": "In the BME lab, test the new SpO2 monitor against the gold-standard reference device on 10 volunteers with different skin tones. Results show 1.8% mean bias — within acceptable range. Document all results for the regulatory submission.", "mood": "research"},
            {"time": "12:00 PM", "task": "Signal processing work", "detail": "Write Python code to process the 24-hour Holter ECG recordings from 50 patients. The algorithm must automatically detect and classify arrhythmia events. Test against cardiologist-labelled gold standard — current sensitivity is 91%, target is 95%.", "mood": "focus"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "Hospital canteen. You often eat with clinical staff — conversations over lunch teach you more about how medical devices are actually used (and misused) than any specification document.", "mood": "break"},
            {"time": "2:30 PM", "task": "Regulatory documentation", "detail": "Prepare the 510(k) technical file section on biocompatibility testing for a new wound dressing sensor. The FDA requires specific ISO 10993 test data. Review test reports from the contract lab and write the summary in the correct regulatory format.", "mood": "focus"},
            {"time": "4:00 PM", "task": "Design review meeting", "detail": "Team review of the wearable glucose sensor prototype version 3. The sensor accuracy in cold conditions (winter use) is insufficient. You propose a temperature compensation algorithm based on the onboard thermistor. Team agrees — assigned to you for next sprint.", "mood": "creative"},
            {"time": "5:30 PM", "task": "Literature review", "detail": "Read 2 papers on flexible strain sensors for prosthetic finger feedback. BME engineers must stay current with research — a technique published last month might solve your current design problem.", "mood": "research"},
        ],
        "tools": ["MATLAB / Python (biomedical signal processing)", "SolidWorks (medical device CAD)", "LabVIEW (instrumentation)", "3D Slicer / ImageJ (medical imaging)", "KiCAD (PCB for medical devices)", "SPSS / R (clinical statistics)"],
        "reality_check": "BME is the most multidisciplinary engineering branch — you must be part engineer, part biologist, and part regulatory compliance expert. The field is slower-paced than software (a medical device takes 5–7 years from concept to approval) but the impact is profound and deeply personal. The pay gap vs CSE is real at the fresher level but narrows significantly with experience, especially in medical AI and device R&D.",
        "salary_snapshot": "Fresher at GE Healthcare / Philips / Medtronic: ₹4–9 LPA. Senior BME R&D engineer after 7 years: ₹18–30 LPA. Medical AI engineer combining BME+ML: ₹20–50 LPA.",
        "youtube_search": "day in the life biomedical engineer medical device",
    },

    "AERO": {
        "tagline": "Every commercial flight you take is kept in the air by equations that aerospace engineers solved — and recalculate before every single flight.",
        "real_apps": [
            {
                "app": "ISRO PSLV — designing a rocket that reliably launches satellites",
                "emoji": "🚀",
                "what_they_built": "The PSLV-C58 rocket launched in January 2024 carried India's XPoSat X-ray astronomy satellite to orbit. Aerospace engineers at ISRO designed the aerodynamic fairing (nose cone) that protects the satellite from the supersonic airflow during ascent, the four strap-on solid rocket boosters that provide the initial thrust, and the fourth-stage liquid engine that precisely inserts the satellite into the correct orbit 600 km above Earth.",
                "cool_fact": "PSLV has a 96% success rate over 60 launches — one of the most reliable rockets in the world. This reliability is not luck; it is the result of 35 years of iterative aerospace engineering. Every failure was analysed and every system redesigned until it was bulletproof."
            },
            {
                "app": "LCA Tejas — India's indigenous fighter aircraft",
                "emoji": "✈️",
                "what_they_built": "The Tejas is a delta-wing combat aircraft developed over 30 years by HAL and DRDO. Aerospace engineers designed the carbon fibre composite airframe (which is 45% of the aircraft's structure by weight and stronger than aluminium but 30% lighter), the unstable fly-by-wire flight control system that makes the aircraft agile, and the engine air intakes that supply air to the GE F404 engine at all angles of attack from -15° to +30°.",
                "cool_fact": "The Tejas airframe is 70% made in India — including all the carbon fibre composite panels that HAL manufactures at their advanced composites division in Bangalore. Each panel is hand-laid and autoclave-cured, a process that takes 8 hours per panel."
            },
            {
                "app": "Skyroot Aerospace Vikram-S — India's first private space rocket",
                "emoji": "🛸",
                "what_they_built": "In November 2022, Skyroot Aerospace launched Vikram-S — India's first privately developed rocket. Skyroot aerospace engineers (most under 30 years old, many from IIT/NIT backgrounds) designed the 3D-printed Kalam-5 solid rocket motor using HTPB propellant, the carbon fibre motor casing that is lighter than any comparable steel casing, and the trajectory optimisation software that guided the rocket to its target altitude.",
                "cool_fact": "Vikram-S reached 89.5 km altitude and achieved Mach 5 (5× the speed of sound) — all with a team of 120 engineers. By comparison, NASA employs 17,000 people. The IN-SPACe policy that enabled this was announced in 2020; the rocket flew 2 years later."
            },
            {
                "app": "Pixxel — Indian Earth observation satellites",
                "emoji": "🛰️",
                "what_they_built": "Pixxel is a Bangalore-based startup that launched a constellation of hyperspectral Earth observation satellites. Aerospace engineers designed the satellite bus (the structural and power platform), the attitude control system (reaction wheels + star trackers that keep the camera pointing at the right spot on Earth to within 0.001°), and the thermal management system that keeps electronics at operating temperature despite swinging from +120°C in sunlight to -180°C in shadow every 90 minutes.",
                "cool_fact": "Pixxel's satellites image Earth in 55 spectral bands (vs 3–4 for a regular camera) — enough to detect crop disease, oil spills, illegal mining, and forest fire risk from space. Every 200 km strip they image has 200 years of agricultural and environmental intelligence."
            },
        ],
        "bridge_12th": [
            {
                "knew_in_12th": "Physics: Newton's laws, forces, motion, pressure",
                "becomes_in_engineering": "Aerodynamics and flight mechanics — understanding how air flowing over a wing generates lift, how drag varies with speed, and how to balance an aircraft so it flies stably without constant pilot input",
                "emoji": "🌬️"
            },
            {
                "knew_in_12th": "Physics: thermodynamics, heat engines, efficiency",
                "becomes_in_engineering": "Aircraft propulsion — understanding how a jet engine compresses air, burns fuel, and expands gases to produce 80,000 kg of thrust, and how to design the thermodynamic cycle for maximum efficiency",
                "emoji": "🔥"
            },
            {
                "knew_in_12th": "Maths: calculus, differential equations, vectors",
                "becomes_in_engineering": "Computational fluid dynamics (CFD) and structural analysis — solving the partial differential equations that describe how air flows around a wing and how the wing structure deforms under that load",
                "emoji": "📐"
            },
            {
                "knew_in_12th": "Physics: material properties, stress, strain",
                "becomes_in_engineering": "Aircraft structures and composites — designing carbon fibre airframes that are strong enough to survive 3g manoeuvres, thermal cycling from -55°C to +80°C, and 30,000 pressurisation cycles over a 25-year aircraft life",
                "emoji": "🏗️"
            },
        ],
        "real_problems": [
            {
                "problem": "A drone kept drifting 15° to the left during forward flight even though the control algorithm commanded it to fly straight. All 4 motors appeared to be running at the correct RPM.",
                "why_it_happened": "The drone's centre of mass was not aligned with its geometric centre — the battery, which weighs 400g, had been mounted 3cm to the left of centre during assembly. This asymmetric weight distribution caused the flight controller to constantly fight a persistent roll tendency.",
                "how_engineers_fixed_it": "The aerospace engineer ran an inertial measurement and found the CG offset. Repositioned the battery pack. But also wrote a centre-of-mass verification procedure for every assembly — because asymmetric loading causes many subtle flight anomalies that are often blamed on the flight controller software.",
                "lesson": "In aerospace, the physical configuration of a vehicle matters as much as the control algorithm. Aircraft are inherently sensitive to mass distribution — this is why airlines weigh and balance passengers and cargo before every commercial flight.",
                "emoji": "🚁"
            },
            {
                "problem": "A student aerospace team's rocket nozzle throat was eroding significantly after just 2 seconds of firing — far more than the material specification predicted.",
                "why_it_happened": "The aluminium oxide (Al₂O₃) particles in the solid rocket exhaust were striking the nozzle throat at high velocity and temperature. This abrasive combustion product was not considered in the material selection — the team only checked the thermal resistance of the graphite nozzle material, not its erosion resistance to particle impingement.",
                "how_engineers_fixed_it": "Switched to a C-C composite (carbon-carbon) nozzle insert that is specifically designed for high-temperature particle erosion resistance. Also redesigned the propellant grain geometry to reduce the Al₂O₃ particle size in the exhaust.",
                "lesson": "Rocket nozzle design is not just a thermodynamics problem — it is simultaneously a fluid mechanics, material science, and combustion chemistry problem. Aerospace engineers must understand all these interactions, not just the dominant one.",
                "emoji": "🔥"
            },
            {
                "problem": "A small satellite's solar panels degraded 40% faster than predicted, shortening the mission life from 5 years to 3 years.",
                "why_it_happened": "The radiation environment in the satellite's orbit (a sun-synchronous orbit at 500 km) was more intense than the modelled environment — specifically, the trapped proton belts during solar maximum were not correctly accounted for in the radiation dose calculations.",
                "how_engineers_fixed_it": "Mission engineers implemented a 'radiation-hardened design by software' approach: reduced solar panel operating voltage during high-radiation periods, implemented a gradual battery discharge strategy that accounts for reduced panel output, and increased the power margin requirement for future missions in the same orbit by 25%.",
                "lesson": "Space is a uniquely harsh environment where every component degrades in ways that have no equivalent on Earth. Aerospace engineers must model the operating environment over the entire mission life — not just at launch.",
                "emoji": "🛰️"
            },
        ],
        "personality_fit": [
            "Physics and maths are your strongest subjects and you actually enjoy complex derivations rather than just memorising formulas",
            "You have been fascinated by planes, rockets, or space since childhood — this passion matters because aerospace has a steep learning curve",
            "You are comfortable with very long development timescales — aircraft and spacecraft take 5–15 years from design to flight",
            "You are methodical and detail-oriented — in aerospace, a small calculation error can have catastrophic consequences, and engineers are trained to triple-check everything",
        ],
        "day_timeline": [
            {"time": "9:00 AM", "task": "CFD simulation review", "detail": "Review overnight ANSYS Fluent CFD run of the new wing design at Mach 0.78 (cruise condition). The drag coefficient is 3.8% higher than the previous design at that specific angle of attack. Identify the cause: a pressure bump on the upper surface at 65% chord — sign of early flow separation.", "mood": "research"},
            {"time": "10:30 AM", "task": "Design modification", "detail": "Try a 0.3mm change to the trailing edge geometry in CATIA to delay the separation. Re-mesh and submit another overnight CFD run. Document the design hypothesis and expected outcome.", "mood": "creative"},
            {"time": "11:30 AM", "task": "Structural analysis", "detail": "Run ABAQUS finite element model of the wing spar under the 3.5g design load condition. Check that the maximum stress at the root fitting is within the design allowable for the carbon fibre layup. It passes — but only with 8% margin. Flag for senior review: is 8% adequate?", "mood": "focus"},
            {"time": "1:00 PM", "task": "Lunch", "detail": "ISRO/HAL canteens are legendary. The aerospace community is small — you know most people in your building. Technical conversations over lunch are common and often productive.", "mood": "break"},
            {"time": "2:00 PM", "task": "Test data analysis", "detail": "Analyse strain gauge data from yesterday's static load test. The measured strain at station 412 is 7% higher than the FEM prediction. Investigate: check if the load was applied correctly, check the gauge calibration, then check if the model boundary condition needs updating.", "mood": "detective"},
            {"time": "3:30 PM", "task": "Design review", "detail": "Present 3 alternative nose cone designs to the project team. Each has different drag-weight-manufacturing tradeoffs. The team selects option B — slightly higher drag but 30% easier to manufacture. Sometimes the best aerodynamic design is not the best engineering decision.", "mood": "team"},
            {"time": "5:30 PM", "task": "Documentation", "detail": "Write the daily technical note documenting the wing modification rationale, the structural analysis findings, and the action item on the 8% stress margin. In aerospace, every engineering decision must be documented so it can be reviewed and approved before it is implemented.", "mood": "win"},
        ],
        "tools": ["ANSYS Fluent / OpenFOAM (CFD)", "CATIA V5 (aircraft CAD)", "ABAQUS / NASTRAN (structural FEA)", "MATLAB / Python (simulation & data analysis)", "STK (satellite mission analysis)", "DAVE (flight dynamics modelling)"],
        "reality_check": "Aerospace has the highest entry barrier of any engineering branch — you need excellent grades, strong maths/physics, and ideally research or competition experience (rocketry team, drone project) to get into ISRO/HAL/private space. The jobs are fewer than CSE but the work is extremely stimulating and the missions are genuinely historic. GATE Aerospace is the critical exam — prepare from Sem 7.",
        "salary_snapshot": "Fresher at ISRO/HAL: ₹5–8 LPA + excellent benefits. Private space startup: ₹8–15 LPA + equity. Senior engineer after 7 years: ₹18–35 LPA. International (Airbus/Boeing/SpaceX): ₹40–120 LPA.",
        "youtube_search": "day in the life aerospace engineer ISRO India",
    },

}


# ─────────────────────────────────────────────────────────────────────────────
# Scenario bank (unchanged — keep all 4×4 scenarios)
# ─────────────────────────────────────────────────────────────────────────────

SCENARIOS: Dict[str, List[Dict]] = {

    # ── CSE — everyday app/logic situations, no jargon ──────────────────────
    "CSE": [
        {
            "id": 1,
            "title": "📱  Your app crashes when too many people use it",
            "context": (
                "You built a food-ordering app for your college. It works perfectly "
                "when 5 people test it. But on the first day of the college fest, "
                "200 people open the app simultaneously — and it stops responding for everyone."
            ),
            "situation": "What is the MOST LIKELY reason this happened?",
            "options": [
                {
                    "id": "A",
                    "text": "The app has a typo in the code",
                    "score": 1,
                    "feedback": "❌ A typo would have broken the app even for 1 person.",
                    "explanation": "Typos are consistent bugs — they break the app for everyone all the time. "
                                   "This worked fine for 5 people but broke for 200, which tells you the issue is about load (scale), not a logic error."
                },
                {
                    "id": "B",
                    "text": "The server ran out of resources — memory or database connections got exhausted",
                    "score": 10,
                    "feedback": "✅ Exactly right. This is called a 'scalability problem' — the most common real-world software failure.",
                    "explanation": "Every server has a limit on how many requests it can handle at once. "
                                   "200 simultaneous users hit that limit. Engineers fix this by optimising resource usage, "
                                   "adding more servers, or using a waiting queue. This is what 'system design' is about."
                },
                {
                    "id": "C",
                    "text": "Someone hacked the app and took it down",
                    "score": 2,
                    "feedback": "Unlikely in this scenario — the timing matches a load spike, not an attack.",
                    "explanation": "While hacking is possible, a crash that happens exactly when 200 people join simultaneously "
                                   "is almost always a resource exhaustion problem, not an attack."
                }
            ],
            "learning": "Software that works for 5 people often breaks for 5000. Engineers must design for scale — this is one of the most important skills in software development."
        },
        {
            "id": 2,
            "title": "🐛  A bug that only one user can see",
            "context": (
                "A user messages you: 'Every time I log in, I see someone else's order history.' "
                "You try it yourself and everything looks normal. Your test accounts work perfectly."
            ),
            "situation": "This is a serious bug — some users are seeing other users' private data. How do you approach it?",
            "options": [
                {
                    "id": "A",
                    "text": "Reply to the user saying it works fine on your end, so it must be their device",
                    "score": 0,
                    "feedback": "❌ Never dismiss a bug just because you can't reproduce it — especially one involving private data.",
                    "explanation": "The user is seeing real data that belongs to someone else. That is a serious privacy breach. "
                                   "Dismissing it means it will keep happening. Real engineers take every report seriously."
                },
                {
                    "id": "B",
                    "text": "Check the code that fetches order history — look for where it identifies 'which user' to load data for",
                    "score": 10,
                    "feedback": "✅ Perfect instinct. The bug is in the logic that connects a user to their data.",
                    "explanation": "This is called an 'authorisation bug' — the system is loading data for the wrong user. "
                                   "By looking at the code that fetches the data, you'll find where user IDs are being mixed up. "
                                   "This is one of the most important security problems in web applications."
                },
                {
                    "id": "C",
                    "text": "Take the app offline immediately and put up a maintenance notice",
                    "score": 6,
                    "feedback": "Taking it offline is responsible — but you also need to find and fix the root cause.",
                    "explanation": "Taking down the app protects users while you investigate, which is reasonable. "
                                   "But the real answer is B — taking it down AND fixing the bug. "
                                   "Taking it down alone without understanding the cause doesn't solve anything."
                }
            ],
            "learning": "When users report strange behaviour with their data, it's almost always an authorisation bug — the code is accidentally showing one person's data to another. These must always be investigated seriously."
        },
        {
            "id": 3,
            "title": "🤝  Two people edited the same file",
            "context": (
                "You and your project partner are both working on the same Python file for your college project. "
                "You both made changes yesterday. Today, when your partner uploaded their version, "
                "all your changes disappeared. You have to redo 3 hours of work."
            ),
            "situation": "How do you prevent this from ever happening again?",
            "options": [
                {
                    "id": "A",
                    "text": "Only one person works on the project at a time — take turns",
                    "score": 4,
                    "feedback": "This works but completely kills your productivity. Real teams have 50+ people working simultaneously.",
                    "explanation": "Waiting for your turn would make software development impossibly slow. "
                                   "There's a much better solution that all professional developers use."
                },
                {
                    "id": "B",
                    "text": "Use Git — version control software where every change is tracked and conflicts are highlighted and merged",
                    "score": 10,
                    "feedback": "✅ This is exactly what Git was built for — and it's used by every software team on Earth.",
                    "explanation": "Git tracks every change made by every person. When two people edit the same file, "
                                   "Git highlights the conflict and lets you choose which changes to keep. "
                                   "Learning Git is one of the first things you do in a CSE job. It's non-negotiable."
                },
                {
                    "id": "C",
                    "text": "Keep a backup copy of every file every hour — just restore from backup if something is overwritten",
                    "score": 3,
                    "feedback": "Backups help with recovery but don't prevent the conflict in the first place.",
                    "explanation": "Backups help if you lose work, but they don't tell you whose changes to keep "
                                   "or help you merge two people's edits intelligently. Git solves all of this."
                }
            ],
            "learning": "Version control (Git) is the foundational tool of every software team. It tracks every change, every person, every version. Learning it is one of the first things you do as a developer."
        },
        {
            "id": 4,
            "title": "🔔  Notification sent 3 times",
            "context": (
                "Users of your app are complaining that they received the same birthday wish notification "
                "3 times in a row. You check the code — it looks correct. "
                "The notification function is called once. Yet users got it 3 times."
            ),
            "situation": "What type of bug most likely caused this?",
            "options": [
                {
                    "id": "A",
                    "text": "There is a typo in the notification message",
                    "score": 0,
                    "feedback": "❌ A typo would change the message text, not send it multiple times.",
                    "explanation": "Typos affect content, not how many times something runs. "
                                   "The issue here is about execution count, not the message itself."
                },
                {
                    "id": "B",
                    "text": "The function that sends notifications ran 3 times — there are probably 3 places in the code that call it",
                    "score": 9,
                    "feedback": "✅ Very likely — duplicate code paths is the most common cause of 'sent multiple times' bugs.",
                    "explanation": "If three different parts of your code all trigger the notification function, "
                                   "it runs three times. Engineers fix this by searching for all the places the function is called "
                                   "and making sure it's only triggered once per birthday."
                },
                {
                    "id": "C",
                    "text": "The notification system retried automatically because it thought the first one failed",
                    "score": 8,
                    "feedback": "✅ Also a very real cause — automatic retries without a 'already sent' check.",
                    "explanation": "Many notification systems automatically retry if they don't get a success confirmation. "
                                   "If the first notification sent successfully but the confirmation was lost, "
                                   "the system retries and sends again. Engineers fix this with 'idempotency' — "
                                   "making sure sending twice has no effect after the first send."
                }
            ],
            "learning": "When something runs more than once unexpectedly, look for either duplicate code calling the same function, or a retry system without a 'already done' check. Both are extremely common in real apps."
        }
    ],

    # ── CSE-AIML — everyday AI/data logic, no ML terminology ────────────────
    "CSE-AIML": [
        {
            "id": 1,
            "title": "🎵  Music app recommends only one genre",
            "context": (
                "You built a music recommendation feature for a college app. "
                "The app recommends songs based on what students have listened to before. "
                "But every student — whether they like classical, rock, or jazz — "
                "keeps getting recommended only Bollywood songs."
            ),
            "situation": "What went wrong with the AI recommendation system?",
            "options": [
                {
                    "id": "A",
                    "text": "The algorithm is too simple — replace it with a more complex one",
                    "score": 3,
                    "feedback": "Complexity is not the problem here — bad training data is.",
                    "explanation": "Making the algorithm more complex won't fix the issue if the data it learned from is unbalanced. "
                                   "You'd end up with a more complex system that still recommends only Bollywood."
                },
                {
                    "id": "B",
                    "text": "The training data had too many Bollywood songs — the AI learned that everyone likes Bollywood",
                    "score": 10,
                    "feedback": "✅ Exactly. Garbage in, garbage out — this is the most fundamental rule of AI.",
                    "explanation": "If 90% of your training songs are Bollywood, the AI concludes that Bollywood = good music. "
                                   "It has no evidence that anyone likes anything else. "
                                   "The fix is balanced training data — equal representation of all genres, "
                                   "and using each user's actual listening history to personalise."
                },
                {
                    "id": "C",
                    "text": "Bollywood is the most popular genre, so the AI is technically correct",
                    "score": 2,
                    "feedback": "Popularity doesn't equal personalisation — recommendation systems should be personal, not generic.",
                    "explanation": "A recommendation that tells everyone 'listen to the most popular thing' is not a recommendation — "
                                   "it's just a chart. The whole point of AI recommendations is to find what THIS specific user will enjoy."
                }
            ],
            "learning": "The quality of an AI model is determined entirely by the quality of the data it learned from. If the training data is biased or unbalanced, the AI will be too — regardless of how sophisticated the algorithm is."
        },
        {
            "id": 2,
            "title": "🌿  Plant disease app fails for poor farmers",
            "context": (
                "You trained an AI to detect plant diseases from photos. It works great in testing — "
                "98% accuracy. But after launching, farmers in rural Maharashtra say the app "
                "keeps saying 'plant is healthy' even when the crop is visibly sick."
            ),
            "situation": "What is the most likely reason the app fails for these farmers specifically?",
            "options": [
                {
                    "id": "A",
                    "text": "Rural farmers don't know how to use the app correctly",
                    "score": 0,
                    "feedback": "❌ Blaming users is never the answer. The engineer's job is to make the app work for all users.",
                    "explanation": "If the app only works for tech-savvy users in controlled conditions, it has failed its purpose. "
                                   "An AI built to help farmers must work for farmers."
                },
                {
                    "id": "B",
                    "text": "The training photos were likely high-quality photos taken in good lighting — but farmers take blurry, low-light photos on cheap phones",
                    "score": 10,
                    "feedback": "✅ Exactly right. The AI learned from perfect photos but encounters real-world imperfect photos.",
                    "explanation": "If all training data was professional close-up photos in bright sunlight, "
                                   "the AI genuinely doesn't know what disease looks like in a blurry, low-light photo taken from 1 metre away. "
                                   "The fix: collect training photos from actual farmers using actual cheap phones in real conditions."
                },
                {
                    "id": "C",
                    "text": "The AI needs more computing power to work on rural internet connections",
                    "score": 3,
                    "feedback": "Internet speed affects how fast results load, not whether the AI detects disease correctly.",
                    "explanation": "The AI runs the photo through its model and gives a result. "
                                   "Slow internet makes this take longer but doesn't change the answer. "
                                   "The problem is with what the AI learned, not how fast it loads."
                }
            ],
            "learning": "AI systems fail when real-world conditions don't match training conditions. Always collect training data that represents the actual users and environments your AI will encounter — not just convenient lab conditions."
        },
        {
            "id": 3,
            "title": "🎓  AI marks attendance — but unfairly",
            "context": (
                "Your college installs an AI face recognition system to mark student attendance automatically. "
                "It works well overall — 94% accuracy. But students with darker skin tones "
                "are marked absent 3× more often even when they are present."
            ),
            "situation": "Your principal wants to use this system for exams where a wrong 'absent' mark could mean failing the semester. What do you recommend?",
            "options": [
                {
                    "id": "A",
                    "text": "Go ahead — 94% accuracy is impressive for an AI system",
                    "score": 1,
                    "feedback": "❌ 94% overall accuracy hides a serious fairness problem for specific students.",
                    "explanation": "Average accuracy is misleading when the errors are concentrated on one group. "
                                   "If the system fails 3× more for darker-skinned students, those students bear all the harm "
                                   "while others benefit. For high-stakes decisions like exams, this is unacceptable."
                },
                {
                    "id": "B",
                    "text": "Don't use it for high-stakes decisions until the fairness problem is fixed by collecting more diverse training photos",
                    "score": 10,
                    "feedback": "✅ Correct — fixing the training data imbalance is the right technical and ethical response.",
                    "explanation": "The system was likely trained on fewer photos of darker-skinned people, "
                                   "so it learned that feature less well. The fix is retraining with balanced representation. "
                                   "Never use a biased AI for decisions that affect people's futures."
                },
                {
                    "id": "C",
                    "text": "Use it but let affected students appeal if they are marked wrongly",
                    "score": 4,
                    "feedback": "Appeals are a partial fix but put the burden on the students who are already being discriminated against.",
                    "explanation": "Making specific groups prove they were present — while others are automatically believed — "
                                   "is an unfair process. The real fix is addressing the bias in the model, not creating a workaround."
                }
            ],
            "learning": "AI fairness is not just a technical issue — it has direct consequences for real people. Systems must be tested for fairness across all groups, not just overall accuracy, before being used for important decisions."
        },
        {
            "id": 4,
            "title": "📰  Fake news detector has a problem",
            "context": (
                "You train an AI to detect fake news. You test it and get 97% accuracy. "
                "Excited, you show it to your professor. She asks: "
                "'What if someone writes fake news in a style that copies a real newspaper?' "
                "You test this — and the AI says it's real news every time."
            ),
            "situation": "What does this reveal about your AI model?",
            "options": [
                {
                    "id": "A",
                    "text": "The model learned to detect writing style, not actual facts",
                    "score": 10,
                    "feedback": "✅ Exactly — the model took a shortcut. Style is easier to learn than truth.",
                    "explanation": "Instead of learning what makes information true or false, the model learned "
                                   "'professional newspaper style = real, informal style = fake'. "
                                   "This is called learning a 'spurious correlation'. Anyone who copies the style "
                                   "of a real newspaper can fool the model, even with completely false content."
                },
                {
                    "id": "B",
                    "text": "The model needs to be larger to catch this type of fake news",
                    "score": 2,
                    "feedback": "A larger model learning the wrong thing will just be more confidently wrong.",
                    "explanation": "If the model is learning the wrong feature (style instead of content truthfulness), "
                                   "more parameters won't help — it'll just learn that wrong feature more thoroughly."
                },
                {
                    "id": "C",
                    "text": "97% accuracy is too low — you need at least 99% to handle edge cases",
                    "score": 3,
                    "feedback": "Accuracy percentage doesn't reveal what the model actually learned — that's a deeper problem.",
                    "explanation": "A model can be 97% accurate on test data while failing completely on a specific type of input. "
                                   "This is why engineers test AI on deliberately adversarial examples, not just random samples."
                }
            ],
            "learning": "AI models often learn shortcuts — easy patterns that work on training data but fail in the real world. Always ask: 'What did the model actually learn?' Test it deliberately with tricky examples, not just random ones."
        }
    ],

    # ── MECH — everyday physical situations, no engineering jargon ──────────
    "MECH": [
        {
            "id": 1,
            "title": "🪑  Canteen chair leg keeps breaking",
            "context": (
                "The college canteen bought 50 new steel chairs 3 months ago. "
                "8 of them have a broken leg — always the same front-right leg, "
                "always at the spot where the leg meets the seat frame. "
                "The steel used is good quality. The weight limit was not exceeded."
            ),
            "situation": "What is the most likely engineering reason the same leg keeps breaking at the same spot?",
            "options": [
                {
                    "id": "A",
                    "text": "Students are sitting on the chairs incorrectly",
                    "score": 1,
                    "feedback": "❌ Blaming users is not an engineering answer. A good design must handle real-world use.",
                    "explanation": "People naturally lean, tilt, and shift on chairs. A proper design accounts for this. "
                                   "If the chair breaks from normal use, it's an engineering failure, not user error."
                },
                {
                    "id": "B",
                    "text": "The joint where the leg meets the frame is a stress concentration point — that exact spot experiences the highest force every time someone sits or stands",
                    "score": 10,
                    "feedback": "✅ Exactly right. Where two parts meet is almost always the weakest point.",
                    "explanation": "When you sit down, force travels through the frame and concentrates at the joint. "
                                   "If the joint has a sharp corner or a weak weld, that's where the metal will fatigue and crack over thousands of cycles. "
                                   "The fix: redesign the joint with a rounded corner (called a fillet) to distribute the stress over a larger area."
                },
                {
                    "id": "C",
                    "text": "The steel delivered was fake — not the grade ordered",
                    "score": 4,
                    "feedback": "Possible, but the systematic pattern (same leg, same spot) points to a design issue, not material fraud.",
                    "explanation": "If the steel was uniformly bad, legs would break randomly everywhere. "
                                   "The fact that it's always the same leg, same spot, tells you the design concentrates stress there."
                }
            ],
            "learning": "In mechanical engineering, failure almost always happens at joints, sharp corners, or transitions — places where stress concentrates. The most important skill is predicting these spots before the product is built."
        },
        {
            "id": 2,
            "title": "🥤  Water bottle cracks in summer",
            "context": (
                "Your startup designed a plastic water bottle. It passed all lab tests. "
                "But after selling 10,000 units, customers in Nagpur and Rajasthan are returning "
                "cracked bottles. Customers in Pune and Mumbai are happy. "
                "You check — Nagpur and Rajasthan regularly reach 48°C in summer. "
                "Your lab tests were done at 25°C."
            ),
            "situation": "What was the fundamental mistake in your design process?",
            "options": [
                {
                    "id": "A",
                    "text": "The plastic grade used was too cheap",
                    "score": 5,
                    "feedback": "Possibly — but you don't know yet because you never tested at high temperatures.",
                    "explanation": "The plastic might be fine or might need upgrading — but without high-temperature testing, "
                                   "you can't tell. The root cause is the missing test, not necessarily the material."
                },
                {
                    "id": "B",
                    "text": "The design was only tested at lab conditions, not at the worst-case temperature customers would actually experience",
                    "score": 10,
                    "feedback": "✅ This is the fundamental mistake — always design and test for worst-case real conditions.",
                    "explanation": "A product that sells across India must be tested at 48°C, 100% humidity, and direct sunlight — "
                                   "not just comfortable lab conditions. This principle is called 'design for worst case'. "
                                   "Every mechanical engineer learns this the hard way, or learns it properly."
                },
                {
                    "id": "C",
                    "text": "Put a warning label: 'Do not use in temperatures above 40°C'",
                    "score": 2,
                    "feedback": "That's not engineering — that's just warning people that your product doesn't work.",
                    "explanation": "Warning labels don't fix the product. The engineering solution is to design "
                                   "a bottle that works in the conditions it will actually be used in."
                }
            ],
            "learning": "Always design and test for the worst conditions your product will encounter in the real world — not just comfortable lab conditions. For an Indian product, that means 48°C summer heat, monsoon humidity, and rough handling."
        },
        {
            "id": 3,
            "title": "🚲  College bike rental — brakes wear out too fast",
            "context": (
                "Your college launches a bike-sharing service with 30 cycles. "
                "After 2 months, 18 bikes have worn-out brakes that need replacing. "
                "The brake pads were supposed to last 6 months. "
                "The bikes are used mostly on the college's sloped roads, "
                "and students frequently brake hard going downhill."
            ),
            "situation": "The brake pads are wearing out 3× faster than expected. What is the engineering explanation?",
            "options": [
                {
                    "id": "A",
                    "text": "Students are braking too hard — they need to be trained to brake gently",
                    "score": 2,
                    "feedback": "Students braking hard downhill is expected behaviour, not misuse. The design must handle this.",
                    "explanation": "If your product fails when used exactly as intended, it's the design that needs to change. "
                                   "Braking hard on slopes is completely normal bike usage."
                },
                {
                    "id": "B",
                    "text": "The brake pad specification was for flat-road use — downhill braking generates much more heat and friction, wearing pads faster",
                    "score": 10,
                    "feedback": "✅ Correct. The pads were specified for average use, not for the actual use pattern on your campus.",
                    "explanation": "Brake pad life depends heavily on how they are used. Downhill braking means constant sustained braking, "
                                   "generating heat that accelerates wear. The fix: specify heavier-duty pads rated for hilly terrain, "
                                   "or increase the maintenance schedule for these bikes. This is called 'use-case analysis'."
                },
                {
                    "id": "C",
                    "text": "The brake pads are counterfeit — contact the supplier",
                    "score": 4,
                    "feedback": "Possible, but the consistent pattern across 18 bikes suggests a usage mismatch, not a product defect.",
                    "explanation": "If 18 out of 30 bikes have the same issue, and all are on a hilly campus, "
                                   "usage pattern is the more likely explanation than all 18 bikes having fake parts."
                }
            ],
            "learning": "In mechanical engineering, understanding the actual use pattern is as important as the design itself. A product designed for average use will fail under heavy use. Engineers must analyse real-world usage, not just average-case usage."
        },
        {
            "id": 4,
            "title": "❄️  Air conditioner struggles in summer",
            "context": (
                "Your college installs new ACs rated to cool a room to 22°C. "
                "In January they work perfectly. In May (when outside temperature is 44°C), "
                "the same ACs can only cool the room to 28°C — 6 degrees short of the spec."
            ),
            "situation": "The AC company says 'the AC is working correctly'. Are they right, and what is really happening?",
            "options": [
                {
                    "id": "A",
                    "text": "The AC company is wrong — 28°C means the AC is faulty",
                    "score": 4,
                    "feedback": "They might actually be right — the AC could be working at full capacity, just against tougher conditions.",
                    "explanation": "Before blaming the AC, you need to understand the relationship between outside temperature and cooling capacity."
                },
                {
                    "id": "B",
                    "text": "The AC might be working correctly — cooling capacity depends on the temperature difference between inside and outside. At 44°C outside, maintaining 22°C requires far more power than at 25°C outside",
                    "score": 10,
                    "feedback": "✅ This is exactly right — cooling capacity is not a fixed number, it depends on conditions.",
                    "explanation": "An AC rated at 1.5 tons works harder and achieves less cooling when outside is 44°C vs 25°C. "
                                   "The engineering fix: specify the AC rating at the worst-case summer temperature, not at standard test conditions (which are typically 35°C outside). "
                                   "If the spec says 22°C at 35°C outside, it may legally be working correctly at 28°C when it's 44°C outside."
                },
                {
                    "id": "C",
                    "text": "The electricity supply is weaker in summer due to grid overload",
                    "score": 3,
                    "feedback": "Voltage fluctuation is a real issue but would affect all electrical equipment, not just cooling performance.",
                    "explanation": "While grid issues can reduce AC performance slightly, the primary explanation for 6°C shortfall "
                                   "is the thermodynamic relationship between indoor-outdoor temperature difference and cooling capacity."
                }
            ],
            "learning": "In thermodynamics (heat engineering), performance is never a fixed number — it always depends on operating conditions. Engineers must always specify ratings at worst-case conditions, not standard lab conditions."
        }
    ],

    # ── ECE — everyday electronics situations, no circuit theory jargon ─────
    "ECE": [
        {
            "id": 1,
            "title": "💡  Arduino LED blinks randomly at home",
            "context": (
                "For your school science exhibition, you built an Arduino circuit that blinks "
                "an LED exactly once per second. It worked perfectly at school. "
                "At home, the LED blinks randomly — sometimes fast, sometimes slow, sometimes not at all. "
                "You didn't change any code. You're using your phone charger as power supply instead "
                "of the school's lab bench power supply."
            ),
            "situation": "The code is identical. What is the most likely reason it behaves differently at home?",
            "options": [
                {
                    "id": "A",
                    "text": "The Arduino board got damaged when you transported it",
                    "score": 3,
                    "feedback": "Possible, but the timing symptom points to a more specific and common cause.",
                    "explanation": "If the board was physically damaged, it would likely fail completely or behave very erratically. "
                                   "Timing issues specifically suggest a power supply problem."
                },
                {
                    "id": "B",
                    "text": "Phone chargers deliver 'noisy' power — small voltage fluctuations that confuse the Arduino's internal clock",
                    "score": 10,
                    "feedback": "✅ This is one of the most common beginner electronics problems.",
                    "explanation": "Lab bench power supplies are very stable and clean. Cheap phone chargers have ripple — "
                                   "small fluctuations in voltage that happen at different rates. "
                                   "The Arduino uses power supply stability to count time accurately. "
                                   "Noisy power = inaccurate timing. Fix: add a small capacitor across the power pins "
                                   "to smooth out the ripple, or use a proper regulated power adapter."
                },
                {
                    "id": "C",
                    "text": "Your home WiFi is interfering with the Arduino's timing",
                    "score": 2,
                    "feedback": "WiFi doesn't typically affect a basic Arduino timing circuit.",
                    "explanation": "Unless your Arduino has a WiFi module and is using radio frequencies, "
                                   "household WiFi won't affect a simple LED blink program. Power supply is the much more likely cause."
                }
            ],
            "learning": "Power supply quality is one of the most underappreciated aspects of electronics. Cheap or noisy power supplies cause mysterious, hard-to-diagnose problems. Electronics engineers always check power quality first when behaviour is erratic."
        },
        {
            "id": 2,
            "title": "🔊  Speaker distorts at high volume",
            "context": (
                "You build a simple Bluetooth speaker for a college project. "
                "At low volume it sounds crystal clear. "
                "But when you turn it up to 70% volume, the sound becomes harsh, "
                "crackly, and distorted — like a cheap radio. "
                "The speaker itself is good quality."
            ),
            "situation": "What is most likely causing the distortion at high volume?",
            "options": [
                {
                    "id": "A",
                    "text": "The Bluetooth signal is getting corrupted",
                    "score": 2,
                    "feedback": "Bluetooth corruption would affect all volume levels equally, not just high volumes.",
                    "explanation": "Bluetooth transmits a digital signal — it either arrives correctly or it doesn't. "
                                   "A problem that only appears at high volume is an analog power problem, not a digital transmission problem."
                },
                {
                    "id": "B",
                    "text": "The amplifier chip is being pushed beyond its power limit — it's trying to produce more power than it can handle",
                    "score": 10,
                    "feedback": "✅ Exactly — this is called 'clipping', the most common cause of speaker distortion.",
                    "explanation": "Every amplifier has a maximum output power. Beyond that point, instead of making the sound louder, "
                                   "the tops and bottoms of the audio wave get cut off (clipped). "
                                   "This creates that harsh, crackling sound. Fix: use a more powerful amplifier chip, "
                                   "or limit the maximum volume in software."
                },
                {
                    "id": "C",
                    "text": "The speaker cone is too small for high volumes",
                    "score": 4,
                    "feedback": "Possible if the speaker is severely underpowered, but amplifier clipping is far more common.",
                    "explanation": "A speaker cone can produce distortion if it's physically moving beyond its limits, "
                                   "but this typically happens at very high volumes. The amplifier clipping usually happens first."
                }
            ],
            "learning": "In electronics, 'clipping' occurs when an amplifier is driven beyond its power rating. It's one of the most common audio problems and is fixed by matching the amplifier power rating to the required output — or limiting the input signal."
        },
        {
            "id": 3,
            "title": "🔋  Smartwatch battery dies in 1 day in summer",
            "context": (
                "You design a smartwatch that is advertised as having a 7-day battery life. "
                "Users in Pune and Delhi complain it lasts only 1 day in summer. "
                "Users in Shimla and Manali (hill stations) report the full 7 days. "
                "Nothing is different between the watches — same model, same software."
            ),
            "situation": "What is causing the battery to drain so much faster in hot places?",
            "options": [
                {
                    "id": "A",
                    "text": "People in hot cities use their phones more, so they check the watch more often",
                    "score": 2,
                    "feedback": "This doesn't explain a 7× difference in battery life.",
                    "explanation": "Even heavy usage wouldn't reduce battery from 7 days to 1 day. "
                                   "A physical effect of temperature is the more likely explanation."
                },
                {
                    "id": "B",
                    "text": "Heat makes lithium batteries less efficient — high temperatures cause the battery to discharge faster and also damage its capacity over time",
                    "score": 10,
                    "feedback": "✅ Correct. Temperature is the biggest enemy of lithium battery performance.",
                    "explanation": "Lithium batteries have an ideal operating range of 15°C–35°C. "
                                   "Above 35°C, internal resistance increases, self-discharge accelerates, and capacity drops. "
                                   "At 45°C ambient (which a wrist-worn device can reach easily in Pune summer), "
                                   "effective capacity can drop by 30–50%. Engineers must specify battery life at maximum operating temperature, not just room temperature."
                },
                {
                    "id": "C",
                    "text": "The display is brighter in sunlight due to auto-brightness, using more power",
                    "score": 5,
                    "feedback": "Auto-brightness does increase display power, but it explains hours, not a 7× difference.",
                    "explanation": "Display brightness increase from auto-brightness might add 20-30% drain. "
                                   "A 7× difference (7 days → 1 day) requires a more fundamental cause like battery chemistry being affected by temperature."
                }
            ],
            "learning": "Temperature is one of the most important factors in electronics design — especially for batteries. Engineers always specify and test device performance at the extremes of the operating temperature range, not just at room temperature."
        },
        {
            "id": 4,
            "title": "📡  Circuit works on desk but not inside a metal box",
            "context": (
                "You design a small wireless sensor circuit. On your desk it works perfectly — "
                "sends data every 5 seconds without fail. "
                "You put the circuit inside a metal enclosure (box) to protect it. "
                "Now it stops sending data completely. "
                "You open the box — it works again. Close it — stops again."
            ),
            "situation": "What is the metal box doing to your circuit?",
            "options": [
                {
                    "id": "A",
                    "text": "The metal box is getting hot and overheating the circuit",
                    "score": 3,
                    "feedback": "Heat could be a factor, but the immediate on/off behaviour with the box being opened/closed points to a different cause.",
                    "explanation": "If it were heat, there would be a delay — the temperature would need time to build up. "
                                   "The immediate failure when you close the box suggests something instantaneous."
                },
                {
                    "id": "B",
                    "text": "The metal box is acting as a Faraday cage — blocking the radio signals the circuit uses to send data",
                    "score": 10,
                    "feedback": "✅ Classic Faraday cage effect — every ECE student learns this.",
                    "explanation": "Metal enclosures block electromagnetic waves — including the radio waves your wireless sensor uses. "
                                   "This is called the Faraday cage effect. Fix: drill a small hole for an external antenna, "
                                   "or position the antenna to poke outside the box. "
                                   "This is why your microwave oven has a metal mesh on the door — it keeps microwaves inside."
                },
                {
                    "id": "C",
                    "text": "The metal box is too heavy and pressing down on the circuit board, damaging connections",
                    "score": 2,
                    "feedback": "If physical pressure caused damage, the circuit would stay broken after you open the box.",
                    "explanation": "Since the circuit works again as soon as you open the box, there's no permanent damage. "
                                   "The effect is immediate and reversible — which means the metal is affecting the signal propagation, not the physical connections."
                }
            ],
            "learning": "Metal enclosures block radio signals — a phenomenon called the Faraday cage effect. This is one of the first things ECE students learn in electromagnetic theory. Wireless sensors, GPS receivers, and any radio device must have their antenna outside or accessible through the enclosure."
        }
    ],

    "CIVIL": [
        {
            "id": 1,
            "title": "🏗️  Cracks in a newly built road after monsoon",
            "context": (
                "You are a junior engineer at a road construction company in Pune. "
                "A 2 km stretch of road your team built just 8 months ago has developed "
                "wide cracks running across the road after the first monsoon. "
                "The client (PMC) is furious and demanding answers."
            ),
            "situation": "What is your FIRST step in investigating the cause?",
            "options": [
                {
                    "id": "A",
                    "text": "Immediately blame the contractor for using low-quality asphalt",
                    "score": 1,
                    "feedback": "❌ Blaming without investigation is unprofessional and probably wrong.",
                    "explanation": "Cracks can be caused by poor subgrade (soil below the road), drainage problems, incorrect asphalt mix, or overloading — not necessarily the asphalt quality. Jumping to conclusions without evidence damages professional relationships and misses the real problem."
                },
                {
                    "id": "B",
                    "text": "Dig trial pits to inspect the road layers — check subgrade soil condition and drainage",
                    "score": 10,
                    "feedback": "✅ Correct. Systematic investigation starts with understanding what is below the surface.",
                    "explanation": "Most premature road failures in India are caused by inadequate drainage (water softening the subgrade) or poor subgrade soil quality — not the surface asphalt. Trial pits reveal the layer thicknesses, compaction quality, and moisture content. This is standard pavement forensics."
                },
                {
                    "id": "C",
                    "text": "Resurface the cracked section with a new asphalt layer",
                    "score": 2,
                    "feedback": "Resurfacing without fixing the root cause means the new layer will crack in the next monsoon too.",
                    "explanation": "This is the most common and most expensive mistake in road maintenance. If the subgrade is weak or drainage is poor, any surface treatment is temporary. Fix the foundation first."
                }
            ],
            "learning": "In civil engineering, visible surface failures almost always have subsurface causes. Always investigate the root cause before specifying a repair — otherwise you are spending money to delay the same failure."
        },
        {
            "id": 2,
            "title": "🏢  Building floor slab is deflecting too much",
            "context": (
                "You are reviewing the structural design of a 4-storey residential building. "
                "After construction of the second floor slab, the surveyor reports that "
                "the centre of the slab is visibly lower than the edges — it has deflected "
                "25mm. The design allowed 20mm maximum deflection."
            ),
            "situation": "The contractor says it is fine — '5mm extra is nothing.' What do you do?",
            "options": [
                {
                    "id": "A",
                    "text": "Accept it — 5mm extra is a minor difference, the building is safe",
                    "score": 2,
                    "feedback": "Exceeding a design limit without engineering justification is not acceptable — even by 5mm.",
                    "explanation": "Design limits exist for reasons: excessive deflection can crack finishes, cause doors and windows to jam, and in severe cases indicate inadequate structural capacity. You cannot informally accept an exceedance without analysis."
                },
                {
                    "id": "B",
                    "text": "Stop work on the upper floors, review the structural calculations, and check whether the slab reinforcement was actually placed as designed",
                    "score": 10,
                    "feedback": "✅ Correct. Excessive deflection during construction is a red flag that must be investigated before adding more load.",
                    "explanation": "Before the upper floors add more weight, you must understand whether the deflection is elastic (acceptable, will partially recover) or indicates inadequate reinforcement. Checking the as-built reinforcement layout against the design drawing is essential."
                },
                {
                    "id": "C",
                    "text": "Add extra steel columns below the slab to support it",
                    "score": 4,
                    "feedback": "Adding support might temporarily help but creates permanent changes not in the structural design.",
                    "explanation": "Adding unplanned columns changes load paths to foundations that were not designed for those loads. The correct approach is to understand the cause first, then decide if remediation is needed — and if so, get a structural engineer to design it properly."
                }
            ],
            "learning": "In structural engineering, deviations from design must be investigated — not accepted verbally. Excessive deflection during construction, before the full design load is applied, is a serious warning sign."
        },
        {
            "id": 3,
            "title": "💧  Water supply pipeline keeps breaking at joints",
            "context": (
                "Pune Municipal Corporation's new water supply main — a 600mm diameter "
                "pipe running 4 km — keeps bursting at flange joints, once every 2–3 months. "
                "Each burst disrupts water supply to 50,000 people and costs ₹8 lakh to repair. "
                "You are the project engineer asked to find out why."
            ),
            "situation": "The contractor says the joints were installed correctly. What do you investigate?",
            "options": [
                {
                    "id": "A",
                    "text": "Replace all flanged joints with welded joints — they are stronger",
                    "score": 5,
                    "feedback": "This might help but is expensive and doesn't confirm the root cause.",
                    "explanation": "Welded joints are stronger, but replacing 4 km of flanged joints costs crores. Before spending that money, you need to confirm that joint failure is actually the root cause and not a symptom of something else like water hammer or ground movement."
                },
                {
                    "id": "B",
                    "text": "Install pressure monitoring along the pipeline — check if water hammer is causing sudden pressure spikes that exceed the joint design pressure",
                    "score": 10,
                    "feedback": "✅ Systematic diagnosis first. Water hammer is a very common cause of repeated joint failures in water supply mains.",
                    "explanation": "Water hammer occurs when pumps start or stop suddenly, or when valves close too fast — creating pressure waves that can be 5–10× the normal operating pressure. Flanged joints may be correctly installed but rated for 10 bar operating pressure, while water hammer produces 40 bar spikes. The fix: install surge protection vessels and slow-closing valves."
                },
                {
                    "id": "C",
                    "text": "Sue the pipe manufacturer for supplying defective flanges",
                    "score": 1,
                    "feedback": "❌ Legal action without technical evidence is premature and will not solve the problem.",
                    "explanation": "If the same type of joint is used worldwide without this failure pattern, the problem is almost certainly in the operating conditions, not the product. Investigate before litigating."
                }
            ],
            "learning": "Repeated failure at the same component type usually means an operating condition is exceeding the design limit — not that the component is defective. Always measure the actual operating conditions before concluding on root cause."
        },
        {
            "id": 4,
            "title": "🌧️  Colony floods every monsoon despite a drainage system",
            "context": (
                "A newly developed residential colony in Hadapsar, Pune floods to 1 metre depth "
                "every time there is a heavy rain event, even though a storm water drainage system "
                "was designed and built by a civil engineer. Residents are angry."
            ),
            "situation": "The original designer says the system was designed correctly. How do you evaluate this?",
            "options": [
                {
                    "id": "A",
                    "text": "The designer is right — some flooding is unavoidable in Pune monsoon",
                    "score": 1,
                    "feedback": "❌ Accepting a design failure as inevitable is engineering negligence.",
                    "explanation": "Well-designed drainage systems protect against design storm events. If the system is not working, either the design assumptions were wrong, construction was incorrect, or the system is blocked. 'Monsoon is heavy' is not an engineering answer."
                },
                {
                    "id": "B",
                    "text": "Check the design rainfall assumption — was the system designed for modern rainfall data or 20-year-old rainfall records?",
                    "score": 9,
                    "feedback": "✅ Very likely the issue — Pune's rainfall intensity has increased significantly in the past two decades.",
                    "explanation": "Many drainage systems in Pune's newer areas were designed using 1990s–2000s rainfall intensity data. With climate change, 1-hour peak rainfall in Pune has increased by 25–40% since then. A correctly designed system for old data may be completely inadequate for current conditions."
                },
                {
                    "id": "C",
                    "text": "Check if the drain outlets are blocked, and verify the as-built drain sizes match the design drawings",
                    "score": 10,
                    "feedback": "✅ Also essential — construction defects and blockages are equally common causes.",
                    "explanation": "Both checks are necessary: first verify the system was built as designed (construction quality), then verify the design was correct for current conditions (design adequacy). Start with the simpler check — physical blockage — then move to the design adequacy question."
                }
            ],
            "learning": "Civil infrastructure performance must be verified against current conditions, not design-time assumptions. Both design adequacy and construction quality must be checked when a system fails — and in urban India, outdated design rainfall data is one of the most common causes of drainage system failure."
        }
    ],

    "CHEM": [
        {
            "id": 1,
            "title": "⚗️  Distillation column producing off-spec product",
            "context": (
                "You are a process engineer at a pharmaceutical plant in Pune's Bhosari MIDC. "
                "The main distillation column is producing a solvent at 94% purity "
                "instead of the required 99.5% specification. "
                "The batch cannot be used and represents a ₹15 lakh loss."
            ),
            "situation": "What is the most logical first thing to investigate?",
            "options": [
                {
                    "id": "A",
                    "text": "The column is broken — shut down the plant and call for maintenance",
                    "score": 2,
                    "feedback": "Shutting down without evidence of a mechanical failure is premature and expensive.",
                    "explanation": "Purity loss in a distillation column is usually a process condition problem (wrong temperature, reflux ratio, feed composition) rather than a mechanical failure. Equipment failures are much rarer and usually accompanied by other symptoms like unusual pressures or visible leaks."
                },
                {
                    "id": "B",
                    "text": "Check the operating conditions — reflux ratio, column temperatures, and feed composition against the design values",
                    "score": 10,
                    "feedback": "✅ Correct. Off-spec product from a distillation column is almost always a process conditions deviation.",
                    "explanation": "Distillation column performance depends critically on the reflux ratio (how much liquid is recycled), the temperature profile, and the feed composition. A slight change in any of these changes the separation. Check the DCS trend data — often you will see the deviation started hours before the product failed spec."
                },
                {
                    "id": "C",
                    "text": "Increase the steam flow to the reboiler to drive more vapour up the column",
                    "score": 4,
                    "feedback": "Increasing steam might help but can also cause flooding — always diagnose before adjusting.",
                    "explanation": "Blindly increasing reboiler duty without understanding why purity dropped can cause the column to flood (too much vapour carries liquid droplets upward, reducing separation). Diagnose first, then make targeted adjustments."
                }
            ],
            "learning": "In chemical plants, performance problems are almost always caused by process condition deviations, not equipment failures. Always check DCS trend data and operating parameters before assuming mechanical failure."
        },
        {
            "id": 2,
            "title": "🔥  Reactor overheating during scale-up",
            "context": (
                "Your company is scaling a new agrochemical synthesis from 10 litres in the lab "
                "to 5,000 litres in the production reactor. "
                "In the lab the reaction was well-controlled at 60°C. "
                "In the plant reactor, the temperature keeps rising uncontrollably to 95°C "
                "despite the cooling jacket running at full capacity."
            ),
            "situation": "This is a potentially dangerous situation. What is the core engineering reason?",
            "options": [
                {
                    "id": "A",
                    "text": "The plant reactor is faulty — the cooling jacket must have a leak",
                    "score": 3,
                    "feedback": "Possible but unlikely if the equipment was tested before startup. The problem is more fundamental.",
                    "explanation": "If the cooling system was leak-tested and commissioned correctly, a structural failure is unlikely to be the first-time cause. The temperature behaviour — rising despite full cooling — points to a fundamental heat balance problem."
                },
                {
                    "id": "B",
                    "text": "The surface area to volume ratio decreases at scale — the cooling jacket cannot remove heat fast enough from the larger reactor",
                    "score": 10,
                    "feedback": "✅ This is the classic and most important scale-up problem in chemical reaction engineering.",
                    "explanation": "When you scale from 10L to 5000L, the volume increases 500×, but the cooling surface area (jacket) only increases ~60×. The reaction generates heat proportional to volume, but cooling removes heat proportional to surface area. The heat balance fundamentally changes — a reaction that was thermally manageable at lab scale can become runaway at plant scale."
                },
                {
                    "id": "C",
                    "text": "The raw materials used in the plant are lower quality than the lab-grade chemicals",
                    "score": 4,
                    "feedback": "Possible, but material quality would affect product purity, not usually cause uncontrolled temperature rise.",
                    "explanation": "Impurities could theoretically catalyse side reactions, but the specific pattern of uncontrolled temperature rise despite full cooling is a textbook heat transfer scale-up problem, not a materials quality issue."
                }
            ],
            "learning": "Scale-up from lab to plant is the most critical and dangerous phase of chemical process development. The surface area to volume ratio changes fundamentally — reactions that are thermally safe at lab scale must be re-engineered for heat removal at plant scale."
        },
        {
            "id": 3,
            "title": "🌊  Wastewater treatment plant failing environmental standards",
            "context": (
                "The effluent treatment plant (ETP) at your chemical factory in Pune's MIDC "
                "is suddenly producing treated water with Chemical Oxygen Demand (COD) "
                "of 450 mg/L — the MPCB permit limit is 250 mg/L. "
                "You have 48 hours to fix this or the plant will be shut down by regulators."
            ),
            "situation": "What is your immediate priority?",
            "options": [
                {
                    "id": "A",
                    "text": "Discharge the off-spec water quietly overnight and hope inspectors do not visit",
                    "score": 0,
                    "feedback": "❌ This is illegal, unethical, and causes genuine environmental damage.",
                    "explanation": "Discharging industrial effluent above permit limits is a criminal offence under the Environment Protection Act. The Mula-Mutha river and Pune's groundwater are directly downstream. This choice ends careers and can result in criminal prosecution."
                },
                {
                    "id": "B",
                    "text": "Identify what changed in the last 24 hours — check if a new chemical batch with a different composition entered the ETP",
                    "score": 10,
                    "feedback": "✅ Correct. A sudden change in ETP performance almost always traces to a change in what entered the system.",
                    "explanation": "ETP biological treatment systems are sensitive to changes in influent composition, pH, and toxic inputs. A new solvent, a cleaning agent, or an accidental spill of a biocide can kill the biological treatment bacteria — causing COD to spike. Finding what changed and stopping it is the immediate priority."
                },
                {
                    "id": "C",
                    "text": "Add more coagulant chemicals to the treatment system to reduce COD quickly",
                    "score": 5,
                    "feedback": "Chemical dosing can help but is a temporary measure and expensive at scale.",
                    "explanation": "Coagulants can reduce COD by precipitation — useful as a short-term emergency measure. But without finding and fixing the root cause, the problem recurs every time. Use chemical dosing to buy time while you investigate."
                }
            ],
            "learning": "Environmental compliance is non-negotiable in chemical engineering. When treatment performance suddenly worsens, the first question is always: what changed in the input? Finding and eliminating the root cause is more important than temporarily fixing the symptoms."
        },
        {
            "id": 4,
            "title": "🧪  New product has unexpected impurity",
            "context": (
                "Your company has developed a new specialty polymer. "
                "The product consistently fails the customer's specification because "
                "of a 1.8% unknown impurity that was never present in the lab synthesis. "
                "The customer's application requires less than 0.1% total impurities."
            ),
            "situation": "What is the most methodical approach to finding and fixing this?",
            "options": [
                {
                    "id": "A",
                    "text": "Add an extra filtration step at the end of the process to remove the impurity",
                    "score": 5,
                    "feedback": "Filtration might remove it, but you don't know if this impurity is filterable — and you still don't know where it came from.",
                    "explanation": "If the impurity is a dissolved compound rather than a suspended solid, filtration will not remove it. And without knowing its source, it may cause other problems. Identify first, then remove."
                },
                {
                    "id": "B",
                    "text": "Run the synthesis at different temperatures, pressures, and residence times to understand under which conditions the impurity forms",
                    "score": 10,
                    "feedback": "✅ Design of experiments — the systematic engineering approach to understanding an unknown problem.",
                    "explanation": "By varying one process parameter at a time and measuring the impurity level, you build a map of which conditions generate the impurity. This reveals the mechanism — perhaps a side reaction occurring above 140°C, or a degradation product from extended residence time. Once you know the mechanism, the fix is obvious."
                },
                {
                    "id": "C",
                    "text": "Use GC-MS to identify the molecular structure of the impurity, then research what reaction could produce it",
                    "score": 9,
                    "feedback": "✅ Also essential — knowing what the impurity IS helps you find where it comes from.",
                    "explanation": "Mass spectrometry identification of the impurity structure is very valuable — if you know the molecular structure, an experienced chemist can often immediately identify which side reaction produces it. Combine this with the experimental approach for the fastest diagnosis."
                }
            ],
            "learning": "In chemical process development, systematic experimentation (Design of Experiments) and analytical chemistry (identification of unknowns) work together. The most efficient path to solving an unknown impurity problem combines both approaches."
        }
    ],

    "BME": [
        {
            "id": 1,
            "title": "💓  ECG machine showing alarming reading for a calm patient",
            "context": (
                "A nurse calls you urgently — the ECG monitor for a patient in Ward 5 "
                "is showing an alarming irregular heartbeat pattern. "
                "The patient is 68 years old, sitting calmly, and says they feel completely fine. "
                "Other vital signs are normal."
            ),
            "situation": "The nurse is about to call the on-call cardiologist at midnight. What do you check first?",
            "options": [
                {
                    "id": "A",
                    "text": "Agree — call the cardiologist immediately, the machine reading must be correct",
                    "score": 3,
                    "feedback": "Patient safety first — but a biomedical engineer should first check for equipment or connection issues before escalating.",
                    "explanation": "Waking a cardiologist at midnight for an equipment artefact is a serious waste of resources and causes alarm to patient and family. A quick 2-minute equipment check should precede clinical escalation."
                },
                {
                    "id": "B",
                    "text": "Check the electrode connections — verify all leads are firmly attached and the skin contact is good",
                    "score": 10,
                    "feedback": "✅ The most common cause of artefact ECG readings is a loose or poorly-attached electrode.",
                    "explanation": "A loose electrode creates a high-impedance connection that introduces motion artefact and electrical noise — which looks exactly like an arrhythmia on screen. Re-attaching the loose lead and checking that the skin was properly prepared (cleaned, dry) resolves the majority of false alarms in clinical settings."
                },
                {
                    "id": "C",
                    "text": "Switch to a different ECG machine and see if the reading persists",
                    "score": 7,
                    "feedback": "Reasonable approach — if the reading persists on a different machine, it is more likely to be real.",
                    "explanation": "Switching machines is a valid diagnostic step, but it is slower and more disruptive than checking electrode connections first. Check electrodes first (30 seconds), then switch machines if the reading persists."
                }
            ],
            "learning": "Biomedical engineers in clinical settings must quickly distinguish between equipment artefacts and genuine clinical events. The most common cause of ECG false alarms is signal quality problems — loose electrodes, poor skin preparation, or motion artefact. Always check signal quality before escalating clinically."
        },
        {
            "id": 2,
            "title": "🦾  Prosthetic limb breaking at the knee joint",
            "context": (
                "A low-cost prosthetic knee joint your team designed for Indian patients "
                "keeps failing at the knee hinge within 3–4 weeks of use for most recipients. "
                "The component is made from high-strength aluminium alloy — your calculations "
                "showed it should last years."
            ),
            "situation": "Why might a component that passes static strength calculations fail so quickly in real use?",
            "options": [
                {
                    "id": "A",
                    "text": "The aluminium was supplied at lower quality than ordered — test the material",
                    "score": 5,
                    "feedback": "Possible, but material testing should follow design review — static strength calculations may have missed the real loading pattern.",
                    "explanation": "If material quality was the only issue, failure would be random and unpredictable. Systematic early failure at a specific location points to a design issue with the loading assumptions."
                },
                {
                    "id": "B",
                    "text": "Static calculations don't capture fatigue — the joint experiences millions of load cycles from walking, each applying a stress that causes microscopic crack growth",
                    "score": 10,
                    "feedback": "✅ Fatigue failure is one of the most important and commonly missed failure modes in mechanical and biomedical design.",
                    "explanation": "Walking 8,000 steps per day × 365 days = 2.9 million load cycles per year. Even if each cycle applies a stress far below the yield strength, repeated cycling causes fatigue cracks that grow until sudden fracture. Prosthetic joints must be designed for fatigue life, not just static strength."
                },
                {
                    "id": "C",
                    "text": "The patients are overloading the prosthetic by doing activities it was not designed for",
                    "score": 2,
                    "feedback": "❌ Blaming patients for using a limb for normal daily activities is not an engineering answer.",
                    "explanation": "A prosthetic limb must be designed for real-world use by real Indian patients — who climb stairs, squat, walk on uneven ground, and carry loads. 'Normal use' in India is different from the test conditions based on Western patient activities that many standard prosthetics are designed for."
                }
            ],
            "learning": "In biomedical device design, fatigue failure under cyclic loading is often more critical than static strength. Any implant or prosthetic that experiences repeated loading must be designed and tested for fatigue life — typically millions of cycles representing years of patient activity."
        },
        {
            "id": 3,
            "title": "📊  Glucose monitor reads 15% too high in summer",
            "context": (
                "Your wearable blood glucose monitor works accurately in validation tests "
                "at 22°C in the laboratory. But in field trials in Rajasthan during summer, "
                "users report readings 12–18% higher than their parallel blood draw tests. "
                "This is clinically dangerous — patients may under-dose their insulin."
            ),
            "situation": "What is the most likely technical cause of the temperature-dependent error?",
            "options": [
                {
                    "id": "A",
                    "text": "The Bluetooth connection is affected by heat — data is getting corrupted during transmission",
                    "score": 1,
                    "feedback": "❌ Bluetooth data transmission is digital — either a packet is received correctly or it is not. It cannot cause a systematic 15% upward bias.",
                    "explanation": "A systematic (not random) bias that is consistent in direction and magnitude across all users in hot conditions points to a physics or chemistry problem in the sensor, not a data transmission problem."
                },
                {
                    "id": "B",
                    "text": "The glucose oxidase enzyme sensor has a temperature-dependent reaction rate — higher temperature means the enzyme reacts faster and produces a higher current signal at the same glucose concentration",
                    "score": 10,
                    "feedback": "✅ Exactly right. Enzyme-based electrochemical sensors are inherently temperature-sensitive.",
                    "explanation": "Glucose oxidase catalyses the reaction of glucose with oxygen, producing a current proportional to glucose concentration. But this reaction rate increases with temperature — so at 38°C skin temperature (common in Rajasthan summer), the same glucose concentration produces ~15% more current than at 22°C lab temperature. The fix: add a temperature sensor to the device and apply a temperature compensation algorithm."
                },
                {
                    "id": "C",
                    "text": "People sweat more in summer and sweat contaminating the sensor causes false high readings",
                    "score": 5,
                    "feedback": "Sweat interference is a real issue in wearable sensors, but it would cause variable and unpredictable errors, not the consistent systematic 15% upward bias across all users.",
                    "explanation": "Sweat contains glucose, lactate, and other compounds that could interfere with the sensor. But the consistent direction and magnitude of the error in the Rajasthan field trial strongly suggests a temperature effect on the enzyme kinetics, not random sweat contamination."
                }
            ],
            "learning": "Biomedical sensors must be validated under the actual environmental conditions they will be used in — not just ideal lab conditions. Temperature, humidity, and patient activity all affect sensor performance. Every wearable sensor that uses biological elements (enzymes, antibodies) requires temperature compensation."
        },
        {
            "id": 4,
            "title": "🏥  Hospital wants to connect all devices to one system",
            "context": (
                "A 500-bed hospital in Pune asks your medical device company to integrate all "
                "bedside monitors (ECG, SpO2, blood pressure) into a central nursing station system "
                "that shows all patients on one screen. "
                "The IT team wants to connect everything over the hospital's existing WiFi network."
            ),
            "situation": "What is the most critical risk to address before deployment?",
            "options": [
                {
                    "id": "A",
                    "text": "The screen at the nursing station might be too small to display 500 patients' data",
                    "score": 2,
                    "feedback": "UI design matters but is the easiest problem to solve — and not the critical risk.",
                    "explanation": "Screen size and display layout can be adjusted. The more fundamental risks involve data reliability, security, and clinical alarm management — problems that can directly harm patients."
                },
                {
                    "id": "B",
                    "text": "WiFi network reliability — if the network drops, nurses lose visibility of critical patient parameters in real time",
                    "score": 9,
                    "feedback": "✅ Network reliability is a critical patient safety issue in connected medical devices.",
                    "explanation": "A 2-second WiFi dropout at the wrong moment could mean a nurse misses a cardiac alarm. Medical device networks must use redundant wired connections for critical monitoring, with WiFi only as backup. IEC 80001-1 (risk management for IT networks incorporating medical devices) mandates reliability requirements."
                },
                {
                    "id": "C",
                    "text": "Cybersecurity — medical devices connected to hospital WiFi are vulnerable to ransomware attacks that could disable all monitoring simultaneously",
                    "score": 10,
                    "feedback": "✅ The most critical risk. Hospital ransomware attacks have disabled medical devices and directly contributed to patient deaths.",
                    "explanation": "In 2020, a ransomware attack on a German hospital disabled medical devices and contributed to the death of a patient who had to be diverted to another hospital. Connected medical devices must be on isolated network segments, use encrypted communications, and have offline fallback modes. Cybersecurity is now a mandatory medical device regulatory requirement globally."
                }
            ],
            "learning": "Connected medical devices create patient safety risks beyond the device itself — network reliability and cybersecurity are now core biomedical engineering responsibilities. A medical device that works perfectly in isolation can become dangerous when connected to a vulnerable network."
        }
    ],

    "AERO": [
        {
            "id": 1,
            "title": "🚁  Drone drifts left during straight-line flight",
            "context": (
                "You built a quadcopter drone for aerial photography. "
                "The flight controller code is correct and all 4 motors appear to spin at "
                "the commanded RPM. But during any straight-line forward flight, "
                "the drone consistently drifts 20° to the left and requires constant "
                "right stick correction to fly straight."
            ),
            "situation": "All motors are confirmed spinning at correct speed. What is the most likely physical cause?",
            "options": [
                {
                    "id": "A",
                    "text": "The flight controller software has a bug in the heading hold algorithm",
                    "score": 4,
                    "feedback": "Possible if all motors are truly at the correct RPM — but a physical cause should be checked first.",
                    "explanation": "If the motors are confirmed at correct RPM, the flight controller is doing its job — commanding the right speeds. The physical problem is more likely to be the cause, since software can be ruled out when actuator outputs are correct."
                },
                {
                    "id": "B",
                    "text": "The drone's centre of mass is offset to the left — the battery or payload is not centred on the frame",
                    "score": 10,
                    "feedback": "✅ An off-centre centre of mass is the most common cause of systematic directional drift in multirotor drones.",
                    "explanation": "Even a 10g mass offset from the geometric centre creates an asymmetric aerodynamic load — the flight controller compensates by tilting the drone, which then translates to a lateral velocity. The 'constant correction' needed is exactly what a CG offset causes: the pilot is fighting a permanent aerodynamic imbalance."
                },
                {
                    "id": "C",
                    "text": "One of the propellers is mounted upside down — generating thrust in the wrong direction",
                    "score": 6,
                    "feedback": "An inverted propeller would cause dramatic, obvious instability — not a gentle consistent drift.",
                    "explanation": "An inverted propeller would generate negative thrust (downward) instead of positive thrust — the drone would oscillate violently or crash immediately. A gentle consistent drift is far more consistent with a small mass asymmetry."
                }
            ],
            "learning": "In aerospace, small physical asymmetries have significant effects on flight behaviour. Centre of mass location is one of the most fundamental checks before any flight — in commercial aviation, load and balance calculations are legally required before every takeoff."
        },
        {
            "id": 2,
            "title": "✈️  Wind tunnel result vs actual flight performance",
            "context": (
                "Your student team designed a small fixed-wing UAV. "
                "The wind tunnel tests showed the wing generates enough lift to fly at 15 m/s. "
                "But in actual flight tests, the aircraft barely gets airborne even at full throttle, "
                "and the motor is overheating. The wind tunnel result predicted plenty of margin."
            ),
            "situation": "The wing is correct — the wind tunnel proved it. Where is the discrepancy?",
            "options": [
                {
                    "id": "A",
                    "text": "The wind tunnel model was too small — aerodynamic results from small models do not scale correctly",
                    "score": 8,
                    "feedback": "Partially correct — Reynolds number scaling is a real issue in wind tunnel testing.",
                    "explanation": "Wind tunnels test scale models, and aerodynamic coefficients vary with Reynolds number (which depends on size and speed). A wing that works well at model scale may perform differently at full scale. This is a well-known limitation of wind tunnel testing."
                },
                {
                    "id": "B",
                    "text": "The actual aircraft weighs more than the design weight used in the wind tunnel lift calculation",
                    "score": 10,
                    "feedback": "✅ The most common cause of 'not enough lift' when the aerodynamics test correctly — the actual aircraft is heavier than designed.",
                    "explanation": "Student teams routinely underestimate the weight of wiring, connectors, fasteners, and control linkages — often adding 15–25% to the design mass. If the wind tunnel test used the design weight but the actual aircraft is 20% heavier, the calculated minimum flight speed is wrong, and the motor must work much harder to generate the required climb performance."
                },
                {
                    "id": "C",
                    "text": "The motor selected does not produce enough thrust — order a more powerful motor",
                    "score": 5,
                    "feedback": "The motor might be undersized, but this is a consequence — first understand why the required thrust increased.",
                    "explanation": "If the aircraft is heavier than designed, then yes, a more powerful motor may be needed. But without understanding the weight discrepancy, you may order a new motor and still find it is not enough — because the real problem is unknown excess weight."
                }
            ],
            "learning": "In aerospace design, weight is always the enemy. Every gram added to an aircraft requires more lift, more thrust, and more fuel or battery. Actual build weight almost always exceeds design weight — experienced aerospace engineers add a 15–20% weight margin to all designs."
        },
        {
            "id": 3,
            "title": "🔥  Rocket nozzle eroding after 3 test firings",
            "context": (
                "Your college rocketry team is testing a solid rocket motor. "
                "The graphite nozzle throat is eroding significantly after just 3 test firings — "
                "each lasting 4 seconds. The manufacturer's data sheet says graphite "
                "should survive 10+ firings at these conditions."
            ),
            "situation": "What is the most likely cause of the accelerated erosion?",
            "options": [
                {
                    "id": "A",
                    "text": "The graphite is fake — the supplier sent a lower quality material",
                    "score": 3,
                    "feedback": "Possible but should be confirmed with material testing before replacing.",
                    "explanation": "If the graphite was the problem, erosion would be random and variable. Systematic accelerated erosion after every firing points to a combustion condition that exceeds the material's design envelope."
                },
                {
                    "id": "B",
                    "text": "The combustion temperature is higher than the manufacturer's rating — possibly because the propellant grain geometry produces more aluminium oxide particles at a higher temperature than specified",
                    "score": 10,
                    "feedback": "✅ Nozzle erosion in solid rockets is driven by combustion temperature and particle impingement — both determined by propellant chemistry and grain geometry.",
                    "explanation": "Solid rocket propellants containing aluminium produce Al₂O₃ particles in the exhaust. These particles strike the nozzle throat at high velocity and temperature, causing abrasive erosion. If the propellant formulation or grain geometry produces higher combustion temperatures or more particles than the design assumed, erosion is much faster. A calorimetric test of the actual propellant temperature is the first step."
                },
                {
                    "id": "C",
                    "text": "The nozzle was machined incorrectly — the throat diameter is too small causing excessive pressure and heat",
                    "score": 6,
                    "feedback": "A smaller-than-designed throat would cause higher chamber pressure — which could contribute. This is worth checking.",
                    "explanation": "Throat diameter directly controls chamber pressure (smaller throat = higher pressure = higher temperature). Measuring the actual throat diameter against the design value is a quick and important check. But propellant chemistry is the more fundamental issue."
                }
            ],
            "learning": "Rocket propulsion involves extreme conditions — temperatures above 3000°C and pressures above 100 atmospheres. Every material decision must account for the actual combustion environment, including particle erosion from metal oxide products. Material data sheets specify conditions — always verify your operating conditions are within those specifications."
        },
        {
            "id": 4,
            "title": "🛰️  Satellite solar panel degrading faster than predicted",
            "context": (
                "A 3U CubeSat your college team built and launched 18 months ago "
                "is generating only 60% of its design power from the solar panels. "
                "The original design predicted it would still produce 90% power at 18 months. "
                "All other systems are working normally."
            ),
            "situation": "What is the most likely cause of the accelerated power degradation?",
            "options": [
                {
                    "id": "A",
                    "text": "The solar panels were installed at the wrong angle — they are not pointing at the sun correctly",
                    "score": 3,
                    "feedback": "If the attitude control is working and other systems are normal, pointing is probably not the issue.",
                    "explanation": "If the satellite's attitude control system is functioning normally (which the problem statement implies — all other systems work), then panel orientation is being maintained. A gradual degradation over 18 months points to a material degradation issue, not a pointing problem."
                },
                {
                    "id": "B",
                    "text": "Space radiation (protons and electrons in the Van Allen belts) has damaged the solar cell crystal structure, permanently reducing their efficiency",
                    "score": 10,
                    "feedback": "✅ Radiation-induced degradation is the primary cause of solar panel power loss in low-Earth orbit satellites.",
                    "explanation": "Solar cells in space are continuously bombarded by high-energy protons and electrons. These particles damage the silicon crystal lattice, creating defects that reduce charge carrier mobility and therefore reduce cell efficiency. This degradation is predictable and is modelled using 'equivalent fluence' calculations — but small satellites with limited radiation shielding can degrade faster than predicted if the orbit passes through high-radiation zones."
                },
                {
                    "id": "C",
                    "text": "The solar panels are covered in micrometeorite dust that is blocking sunlight",
                    "score": 4,
                    "feedback": "Contamination can reduce output, but a 40% loss at 18 months is far more than contamination alone would cause.",
                    "explanation": "Micrometeorite and debris contamination does occur in space, but the typical contamination loss over 18 months is 2–5%, not 30–40%. The scale of degradation points to radiation damage, not contamination."
                }
            ],
            "learning": "Designing for the space environment requires accounting for radiation, thermal cycling, and vacuum conditions that have no equivalent on Earth. Space radiation damage to solar cells is a well-understood phenomenon — every satellite mission must include a radiation budget analysis that predicts end-of-life power output."
        }
    ],
}

BRANCH_NAMES  = {
    "CSE": "Computer Science & Engineering",
    "CSE-AIML": "CSE with AI & Machine Learning",
    "MECH": "Mechanical Engineering",
    "ECE": "Electronics & Communication Engineering",
    "CIVIL": "Civil Engineering",
    "CHEM": "Chemical Engineering",
    "BME": "Biomedical Engineering",
    "AERO": "Aerospace Engineering",
}
BRANCH_EMOJIS = {
    "CSE": "💻", "CSE-AIML": "🤖", "MECH": "⚙️", "ECE": "🔌",
    "CIVIL": "🏗️", "CHEM": "⚗️", "BME": "🏥", "AERO": "🚀",
}


class DayInLifeSimulator:
    def get_available_branches(self): return list(SCENARIOS.keys())
    def get_branch_info(self, code):
        return {"code": code, "name": BRANCH_NAMES.get(code, code),
                "emoji": BRANCH_EMOJIS.get(code, "🎓"),
                "total_scenarios": len(SCENARIOS.get(code, []))}
    def get_intro(self, code): return BRANCH_INTRO.get(code.upper())
    def get_scenario(self, branch_code, scenario_index):
        scenarios = SCENARIOS.get(branch_code, [])
        if 0 <= scenario_index < len(scenarios):
            s = scenarios[scenario_index].copy()
            s["index"] = scenario_index; s["total"] = len(scenarios)
            s["branch_code"] = branch_code; s["branch_name"] = BRANCH_NAMES.get(branch_code, branch_code)
            return s
        return None
    def evaluate_choice(self, branch_code, scenario_index, choice_id):
        scenario = self.get_scenario(branch_code, scenario_index)
        if not scenario: return {"error": "Invalid scenario"}
        chosen = next((o for o in scenario["options"] if o["id"] == choice_id), None)
        if not chosen: return {"error": "Invalid choice"}
        is_last = (scenario_index + 1) >= scenario["total"]
        return {"choice_id": choice_id, "score": chosen["score"], "max_score": 10,
                "feedback": chosen["feedback"], "explanation": chosen["explanation"],
                "learning": scenario["learning"], "scenario_title": scenario["title"],
                "is_last": is_last, "next_index": scenario_index + 1 if not is_last else None}
    def calculate_final_score(self, decisions):
        if not decisions: return {"error": "No decisions"}
        total = sum(d.get("score", 0) for d in decisions)
        max_p = len(decisions) * 10
        pct   = round(total / max_p * 100, 1) if max_p else 0
        if   pct >= 85: level, msg, emoji = "Outstanding", "You think like a practising engineer! This branch suits you very well.", "🏆"
        elif pct >= 70: level, msg, emoji = "Good",         "Solid judgment. A bit of learning and you'd excel here.", "✅"
        elif pct >= 50: level, msg, emoji = "Developing",   "You have the right instincts — keep exploring this field.", "📈"
        else:           level, msg, emoji = "Needs Work",   "This field might need more study before it clicks. Try other branches too.", "💡"
        return {"total_score": total, "max_score": max_p, "percentage": pct,
                "level": level, "message": msg, "emoji": emoji, "decisions": len(decisions)}


if __name__ == "__main__":
    sim = DayInLifeSimulator()
    for code in sim.get_available_branches():
        intro = sim.get_intro(code)
        print(f"\n{BRANCH_EMOJIS[code]} {BRANCH_NAMES[code]}")
        print(f"  Tagline    : {intro['tagline'][:60]}...")
        print(f"  Real apps  : {len(intro['real_apps'])}")
        print(f"  Bridge 12th: {len(intro['bridge_12th'])}")
        print(f"  Problems   : {len(intro['real_problems'])}")
        print(f"  YT Search  : {intro['youtube_search']}")
    print("\n✅ Simulator OK")
