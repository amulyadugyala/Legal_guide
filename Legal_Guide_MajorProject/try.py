import streamlit as st
from dotenv import load_dotenv
from crew import legal_assistant_crew
import time

load_dotenv()

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Legal Reasoning Assistant",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- SIDEBAR NAV ---------------- #
st.sidebar.title("⚖️ Legal AI")

page = st.sidebar.radio(
    "Navigate",
    [
        "💬 Chat Assistant",
        "🏛️ Legal Insights",
        "📊 Analysis Dashboard",
        "📞 Emergency Help",
        "📘 About System"
    ]
)

def format_legal_report(text):
    """
    Converts raw AI output into structured sections.
    """

    sections = {
        "Case Overview": "",
        "Key Legal Issues": "",
        "Applicable IPC Sections": "",
        "Legal Precedents": "",
        "Opponent Perspective": "",
        "Defence Perspective": "",
        "Judicial Analysis": "",
        "Final Interpretation": ""
    }

    current_section = "Case Overview"

    for line in text.split("\n"):
        line_lower = line.lower()

        if "ipc" in line_lower:
            current_section = "Applicable IPC Sections"
        elif "precedent" in line_lower:
            current_section = "Legal Precedents"
        elif "opponent" in line_lower:
            current_section = "Opponent Perspective"
        elif "defence" in line_lower or "defense" in line_lower:
            current_section = "Defence Perspective"
        elif "judge" in line_lower or "analysis" in line_lower:
            current_section = "Judicial Analysis"
        elif "conclusion" in line_lower or "final" in line_lower:
            current_section = "Final Interpretation"

        sections[current_section] += line + "\n"

    return sections

# ---------------- SESSION ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

# =========================================================
# 💬 CHAT ASSISTANT (CHATGPT STYLE)
# =========================================================
if page == "💬 Chat Assistant":

    st.markdown("""
    <style>
    .chat-container {max-width: 850px; margin: auto;}
    .chat-row {display: flex; margin-bottom: 12px;}
    .chat-row.user {justify-content: flex-end;}
    .chat-row.ai {justify-content: flex-start;}
    .chat-bubble {padding: 12px 16px; border-radius: 12px; max-width: 70%;}

    /* Light */
    .user-bubble {background: #DCF8C6; color: black;}
    .ai-bubble {background: #F1F0F0; color: black;}

    /* Dark */
    @media (prefers-color-scheme: dark) {
        .user-bubble {background: #2e7d32; color: white;}
        .ai-bubble {background: #2b2b2b; color: white;}
    }

    .avatar {margin: 0 8px; font-size: 18px;}
    </style>
    """, unsafe_allow_html=True)

    st.subheader("💬 Chat with AI Legal Assistant")

    # Display messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-row user">
                <div class="chat-bubble user-bubble">{msg["content"]}</div>
                <div class="avatar">🧑</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-row ai">
                <div class="avatar">🤖</div>
                <div class="chat-bubble ai-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Typing animation
    def stream_text(text, placeholder):
        words = text.split()
        output = ""
        for word in words:
            output += word + " "
            placeholder.markdown(f"""
            <div class="chat-row ai">
                <div class="avatar">🤖</div>
                <div class="chat-bubble ai-bubble">{output}▌</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.02)

        placeholder.markdown(f"""
        <div class="chat-row ai">
            <div class="avatar">🤖</div>
            <div class="chat-bubble ai-bubble">{output}</div>
        </div>
        """, unsafe_allow_html=True)

    user_input = st.chat_input("Describe your legal issue...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        st.markdown(f"""
        <div class="chat-row user">
            <div class="chat-bubble user-bubble">{user_input}</div>
            <div class="avatar">🧑</div>
        </div>
        """, unsafe_allow_html=True)

        placeholder = st.empty()

        with st.spinner("🤖 Analyzing..."):
            result = legal_assistant_crew.kickoff(
                inputs={"user_input": user_input}
            )

        output = result if isinstance(result, str) else str(result)

        st.session_state["last_result"] = output

        stream_text(output, placeholder)

        st.session_state.messages.append({"role": "assistant", "content": output})


# =========================================================
# 🏛️ LEGAL INSIGHTS (ADVANCED INTERACTIVE)
# =========================================================
if page == "🏛️ Legal Insights":

    st.markdown("<h2>⚖️ LawInsight</h2>", unsafe_allow_html=True)
    st.caption("Explore Indian legal domains with examples and structure")

    # ---------------- STATE ---------------- #
    if "selected_domain" not in st.session_state:
        st.session_state.selected_domain = None

    # ---------------- CSS ---------------- #
    st.markdown("""
    <style>
    .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }

    .card-btn button {
        height: 120px;
        border-radius: 16px;
        font-size: 16px;
        font-weight: 600;
        background-color: #2b2b36;
        color: white;
        border: none;
        transition: 0.3s;
    }

    .card-btn button:hover {
        transform: translateY(-5px);
        box-shadow: 0px 6px 18px rgba(0,0,0,0.3);
    }

    @media (prefers-color-scheme: light) {
        .card-btn button {
            background-color: #f4f6f8;
            color: black;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- GRID BUTTONS ---------------- #
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⚖️ Criminal Laws", use_container_width=True):
            st.session_state.selected_domain = "criminal"

        if st.button("📜 Constitutional Laws", use_container_width=True):
            st.session_state.selected_domain = "constitutional"

        if st.button("💼 Labor Laws", use_container_width=True):
            st.session_state.selected_domain = "labor"

        # NEW
        if st.button("👨‍👩‍👧 Family Law", use_container_width=True):
            st.session_state.selected_domain = "family"

        if st.button("⚙️ Procedural Law", use_container_width=True):
            st.session_state.selected_domain = "procedural"

        if st.button("🌱 Environmental Law", use_container_width=True):
            st.session_state.selected_domain = "environment"

    with col2:
        if st.button("🏛️ Civil Laws", use_container_width=True):
            st.session_state.selected_domain = "civil"

        if st.button("🏢 Corporate Laws", use_container_width=True):
            st.session_state.selected_domain = "corporate"

        if st.button("🏠 Property Laws", use_container_width=True):
            st.session_state.selected_domain = "property"

        # NEW
        if st.button("🏛️ Administrative Law", use_container_width=True):
            st.session_state.selected_domain = "administrative"

        if st.button("💻 Cyber Law", use_container_width=True):
            st.session_state.selected_domain = "cyber"

        if st.button("💰 Tax Law", use_container_width=True):
            st.session_state.selected_domain = "tax"

    st.divider()

    # =========================================================
    # 🔍 MODAL VIEW (DETAIL PANEL)
    # =========================================================
    if st.session_state.selected_domain:

        st.subheader("📖 Detailed Insight")
        domain = st.session_state.selected_domain

        # EXISTING DOMAINS (UNCHANGED)
        if domain == "criminal":
            st.markdown("### ⚖️ Criminal Law (India)")
            st.markdown("""
**Core Laws:**
- Indian Penal Code (IPC), 1860  
- Criminal Procedure Code (CrPC)  
- Indian Evidence Act  

**Key Concepts:**
- Mens rea (guilty mind)  
- Actus reus (guilty act)  
- Burden of proof (beyond reasonable doubt)  

**Scope:**
Crimes against individuals or society like theft, assault, murder, cybercrime.

#### 📌 Mini Case Example
""")
            st.info("A person steals a mobile phone → IPC Section 378 (Theft) applies.")
            st.markdown("""
#### ⚖️ Practical Interpretation
The prosecution must prove both intent and action. Without intent, criminal liability may fail.

#### 📊 Legal Flow
Crime → FIR → Investigation → Trial → Judgment
""")

        elif domain == "civil":
            st.markdown("### 🏛️ Civil Law")
            st.markdown("""
**Core Laws:**
- Indian Contract Act, 1872  
- Civil Procedure Code (CPC)  

**Key Concepts:**
- Breach of contract  
- Damages and compensation  
- Preponderance of probability  

**Scope:**
Disputes between individuals or entities (contracts, family, property).

#### 📌 Mini Case Example
""")
            st.info("A company fails to deliver goods after payment → breach of contract.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Civil cases focus on compensation rather than punishment.

#### 📊 Legal Flow
Dispute → Suit → Evidence → Judgment
""")

        elif domain == "constitutional":
            st.markdown("### 📜 Constitutional Law")
            st.markdown("""
**Core Document:**
- Constitution of India  

**Key Concepts:**
- Fundamental Rights  
- Judicial Review  
- Basic Structure Doctrine  

**Scope:**
Defines rights, duties, and governance structure.

#### 📌 Mini Case Example
""")
            st.info("Restriction on speech → Article 19 violation challenge.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Courts ensure laws do not violate constitutional rights.

#### 📊 Structure
Rights → Duties → Governance → Judicial Review
""")

        elif domain == "corporate":
            st.markdown("### 🏢 Corporate Law")
            st.markdown("""
**Core Laws:**
- Companies Act, 2013  
- SEBI Regulations  

**Key Concepts:**
- Corporate governance  
- Compliance  
- Fiduciary duty  

**Scope:**
Regulates companies and business conduct.

#### 📌 Mini Case Example
""")
            st.info("Company hides financial losses → violation of compliance norms.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Directors are legally responsible for transparency and accountability.

#### 📊 Flow
Company → Compliance → Audit → Regulation → Action
""")

        elif domain == "labor":
            st.markdown("### 💼 Labor Law")
            st.markdown("""
**Core Laws:**
- Minimum Wages Act  
- Industrial Disputes Act  

**Key Concepts:**
- Fair wages  
- Worker protection  
- Industrial disputes  

**Scope:**
Protects employees and regulates employer-employee relations.

#### 📌 Mini Case Example
""")
            st.info("Worker not paid minimum wage → labor violation.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Employers must comply with statutory protections for workers.

#### 📊 Flow
Employment → Dispute → Tribunal → Resolution
""")

        elif domain == "property":
            st.markdown("### 🏠 Property Law")
            st.markdown("""
**Core Laws:**
- Transfer of Property Act  
- Registration Act  

**Key Concepts:**
- Ownership rights  
- Transfer of title  
- Possession vs ownership  

**Scope:**
Ownership, transfer, and disputes related to property.

#### 📌 Mini Case Example
""")
            st.info("Two individuals claim same land → title dispute.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Legal ownership depends on valid documentation and registration.

#### 📊 Flow
Ownership → Transfer → Registration → Dispute → Court
""")

        # ================= NEW DOMAINS ================= #

        elif domain == "family":
            st.markdown("### 👨‍👩‍👧 Family Law")
            st.markdown("""
**Core Laws:**
- Hindu Marriage Act  
- Special Marriage Act  
- Protection of Women from Domestic Violence Act  

**Key Concepts:**
- Marriage & divorce  
- Maintenance (alimony)  
- Child custody  
- Domestic violence protection  

**Scope:**
Regulates family relationships including marriage, divorce, custody, and maintenance.

#### 📌 Mini Case Example
""")
            st.info("A spouse files for divorce due to cruelty → governed under Hindu Marriage Act.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Courts focus on fairness, welfare of children, and protection of vulnerable individuals.

#### 📊 Flow
Marriage → Dispute → Family Court → Mediation → Judgment
""")

        elif domain == "administrative":
            st.markdown("### 🏛️ Administrative Law")
            st.markdown("""
**Core Framework:**
- Constitution of India  
- Administrative Tribunals Act  

**Key Concepts:**
- Judicial review  
- Rule of law  
- Delegated legislation  
- Natural justice  

**Scope:**
Regulates actions and decisions of government authorities and public bodies.

#### 📌 Mini Case Example
""")
            st.info("A business license is cancelled unfairly → challenged in court under administrative law.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Courts ensure government decisions are fair, lawful, and not arbitrary.

#### 📊 Flow
Government Action → Citizen Challenge → Judicial Review → Decision
""")

        elif domain == "procedural":
            st.markdown("### ⚙️ Procedural Law")
            st.markdown("""
**Core Laws:**
- Criminal Procedure Code (CrPC)  
- Civil Procedure Code (CPC)  

**Key Concepts:**
- Due process  
- Jurisdiction  
- Filing procedures  
- Trial stages  

**Scope:**
Defines the procedures for conducting civil and criminal cases in courts.

#### 📌 Mini Case Example
""")
            st.info("Filing an FIR and investigation process → governed under CrPC.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Even strong cases can fail if proper legal procedures are not followed.

#### 📊 Flow
Complaint → Filing → Hearing → Trial → Judgment
""")

        elif domain == "cyber":
            st.markdown("### 💻 Cyber Law")
            st.markdown("""
**Core Law:**
- Information Technology Act, 2000  

**Key Concepts:**
- Cyber fraud  
- Data privacy  
- Identity theft  
- Digital signatures  

**Scope:**
Deals with crimes and legal issues related to digital platforms and online activities.

#### 📌 Mini Case Example
""")
            st.info("Unauthorized online transaction → cyber fraud under IT Act.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Digital evidence plays a critical role in proving cyber crimes.

#### 📊 Flow
Cyber Crime → Complaint → Cyber Cell → Digital Investigation → Action
""")

        elif domain == "environment":
            st.markdown("### 🌱 Environmental Law")
            st.markdown("""
**Core Laws:**
- Environment Protection Act  
- Air (Prevention and Control of Pollution) Act  
- Water (Prevention and Control of Pollution) Act  

**Key Concepts:**
- Sustainable development  
- Polluter pays principle  
- Environmental impact  

**Scope:**
Protects environment and regulates pollution and ecological balance.

#### 📌 Mini Case Example
""")
            st.info("A factory releases untreated waste into a river → violation of environmental laws.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Industries must comply with environmental norms or face penalties and shutdowns.

#### 📊 Flow
Pollution → Complaint → Inspection → Regulation → Penalty/Closure
""")

        elif domain == "tax":
            st.markdown("### 💰 Tax Law")
            st.markdown("""
**Core Laws:**
- Income Tax Act  
- Goods and Services Tax (GST) Act  

**Key Concepts:**
- Tax compliance  
- Direct vs indirect tax  
- Tax evasion  
- Audit and assessment  

**Scope:**
Regulates taxation of individuals, businesses, and transactions.

#### 📌 Mini Case Example
""")
            st.info("A company underreports income → tax evasion case under Income Tax Act.")
            st.markdown("""
#### ⚖️ Practical Interpretation
Failure to comply with tax laws can result in heavy penalties and prosecution.

#### 📊 Flow
Income → Tax Filing → Audit → Assessment → Penalty
""")

        # CLOSE BUTTON
        st.button("❌ Close", on_click=lambda: st.session_state.update({"selected_domain": None}))

    

# =========================================================
# 📊 Analysis Dashboard
# =========================================================

elif page == "📊 Analysis Dashboard":

    st.subheader("📊 Legal Analysis Dashboard")

    if "last_result" in st.session_state and st.session_state.last_result.strip():

        st.markdown("### 📄 Final Report")

        st.markdown(st.session_state.last_result)

        st.download_button(
            "📥 Download Report",
            st.session_state.last_result,
            file_name="legal_analysis.txt"
        )

    else:
        st.warning("⚠️ No analysis available yet.")
        st.info("👉 Go to **Chat Assistant** and run a query first.")


# =========================================================
# 📞 EMERGENCY HELP (COLORED CARDS)
# =========================================================
elif page == "📞 Emergency Help":

    st.subheader("🚨 Emergency Legal & Safety Helplines (India)")

    st.markdown("""
    <style>
    .card {
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 12px;
        font-size: 16px;
        font-weight: 500;
    }

    .police { background: #e3f2fd; color: #0d47a1; }
    .ambulance { background: #e8f5e9; color: #1b5e20; }
    .fire { background: #ffebee; color: #b71c1c; }

    .women { background: #fce4ec; color: #880e4f; }
    .child { background: #fff3e0; color: #e65100; }
    .senior { background: #ede7f6; color: #4527a0; }

    .cyber { background: #e0f7fa; color: #006064; }
    .legal { background: #f1f8e9; color: #33691e; }
    .emergency { background: #fbe9e7; color: #bf360c; }

    @media (prefers-color-scheme: dark) {
        .police { background: #1e3a5f; color: #90caf9; }
        .ambulance { background: #1b3d2b; color: #a5d6a7; }
        .fire { background: #4a1c1c; color: #ef9a9a; }

        .women { background: #4a1c2f; color: #f48fb1; }
        .child { background: #4a2e0b; color: #ffcc80; }
        .senior { background: #2e1f4d; color: #b39ddb; }

        .cyber { background: #00363a; color: #80deea; }
        .legal { background: #2c3e1f; color: #c5e1a5; }
        .emergency { background: #4a2a1f; color: #ffab91; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card police">🚔 Police<br>📞 <b>100</b></div>
    <div class="card ambulance">🚑 Ambulance<br>📞 <b>108</b></div>
    <div class="card fire">🔥 Fire Brigade<br>📞 <b>101</b></div>

    <div class="card women">👩 Women Helpline<br>📞 <b>1091</b></div>
    <div class="card child">🧒 Child Helpline<br>📞 <b>1098</b></div>
    <div class="card senior">👴 Senior Citizen<br>📞 <b>14567</b></div>

    <div class="card cyber">💻 Cyber Crime<br>📞 <b>1930</b></div>
    <div class="card legal">⚖️ Legal Aid<br>📞 <b>15100</b></div>
    <div class="card emergency">🚨 National Emergency<br>📞 <b>112</b></div>
    """, unsafe_allow_html=True)


# =========================================================
# 📘 ABOUT SYSTEM
# =========================================================
elif page == "📘 About System":

    st.subheader("📘 About This System")

    st.markdown("""
### ⚖️ Multi-Agent Legal Reasoning System

This system uses multiple AI agents to simulate legal reasoning.

### 🔍 Features
- Case understanding
- IPC law retrieval
- Legal precedents
- Multi-perspective reasoning
- Explainable AI

### ⚠️ Disclaimer
This is for educational purposes only and not legal advice.
""")