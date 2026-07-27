import streamlit as st
import requests

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="NexusFreight AI",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "https://nexusfreight-api.onrender.com/chat"

def ask_backend(question):
    response = requests.post(
        API_URL,
        json={"message": question},
        timeout=120
    )

    response.raise_for_status()

    return response.json()

# ==========================================================
# SESSION
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# MODERN CSS
# ==========================================================

st.markdown("""
<style>

/* -------------------- Google Font -------------------- */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html,
body,
[class*="css"]{

font-family:'Inter',sans-serif;

}

/* -------------------- Main App -------------------- */

.stApp{

background:#F5F7F2;

}

/* -------------------- Hide Streamlit -------------------- */

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

div[data-testid="stSidebarNav"]{
display:none;
}

/* -------------------- Container -------------------- */

.block-container{

padding-top:25px;

padding-left:45px;

padding-right:45px;

padding-bottom:20px;

}

/* -------------------- Sidebar -------------------- */

section[data-testid="stSidebar"]{

background:#FCFDFB;

width:320px !important;

border-right:1px solid #D8E2D1;

}

/* -------------------- Sidebar Logo -------------------- */

.logo-card{

background:linear-gradient(
135deg,
#6D8B74,
#8AA58A
);

padding:28px;

border-radius:22px;

margin-bottom:35px;

box-shadow:0 12px 28px rgba(109,139,116,.28);

}

.logo-title{

font-size:30px;

font-weight:700;

color:white;

margin-bottom:8px;

}

.logo-sub{

font-size:14px;

color:rgba(255,255,255,.9);

line-height:1.6;

}

/* -------------------- Navigation -------------------- */

.nav-title{

font-size:24px;
font-weight:700;
color:#5F7161;
letter-spacing:.5px;
margin-bottom:18px;

}

/* -------------------- Streamlit Buttons -------------------- */

.stButton>button{

width:100%;

height:80px;

border-radius:18px;

background:#F7FAF5;

border:1px solid #D6E1D2;

padding-left:24px;

transition:.25s;

box-shadow:0 5px 16px rgba(0,0,0,.04);

}


/* Navigation Button Text */

.stButton>button p{

font-size:22px !important;

font-weight:700 !important;

color:#4B5D4B !important;

text-align:left !important;

margin:0;

}

/* -------------------- Divider -------------------- */

hr{

margin-top:28px;

margin-bottom:28px;

}

/* -------------------- Status Card -------------------- */

.status-card{

background:#FBFCFA;

padding:18px;

border-radius:18px;

border:1px solid #D7E2D1;

margin-top:20px;

box-shadow:0 6px 18px rgba(0,0,0,.03);

}

.status-title{

font-size:15px;

font-weight:700;

margin-bottom:12px;

}

.status-item{

font-size:14px;

padding:7px 0;

}

/* -------------------- Hero -------------------- */

.hero{

background:#FCFDFB;

padding:42px;

border-radius:28px;

box-shadow:0 12px 30px rgba(0,0,0,.05);

margin-bottom:35px;

border:1px solid #D6E2D2;

}

.hero h1{

font-size:46px;

font-weight:700;

color:#4D644F;

margin-bottom:12px;

}

.hero p{

font-size:19px;

color:#667566;

line-height:1.8;

}

/* -------------------- Chat Bubble -------------------- */

.stChatMessage{

background:#FCFDFB;

border-radius:22px;

padding:24px 26px;

margin-bottom:16px;

box-shadow:0 8px 22px rgba(0,0,0,.05);

border:1px solid #ECECEC;

}

/* Assistant */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){

background:white;

}

/* User */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){

background:#EAF4E5;

}

/* -------------------- Source Badge -------------------- */

.source-card{

display:flex;

justify-content:space-between;
align-items:center;

margin-top:18px;
margin-bottom:6px;

padding:10px 16px;

width:95%;
margin-left:auto;
margin-right:auto;

background:#F4F8F2;

border:1px solid #D8E2D1;

border-radius:14px;

font-size:13px;

color:#667566;

min-height:55px;

}

.source-card div{

line-height:1.3;

}

.source-card b{

font-size:12px;

color:#7B8B7A;

font-weight:600;

}



/* -------------------- Chat Input -------------------- */

.stChatInput textarea{

border-radius:18px !important;

font-size:18px;

padding:14px;

background:#FCFDFB;

border:1px solid #D8E2D1;

}

/* -------------------- Footer -------------------- */

.footer{

text-align:center;

color:#708670;

font-size:13px;

margin-top:40px;

}

/* Popular Question Buttons */

div[data-testid="column"] .stButton>button{

height:70px;

background:#F4F8F1;

border-radius:18px;

border:1px solid #D7E2D1;

}

div[data-testid="column"] .stButton>button p{

font-size:18px !important;

font-weight:600 !important;

color:#516851 !important;

}



div[data-testid="stAlert"]{

border-radius:20px;

font-size:18px;

padding:20px;

}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("""

<div class="logo-card">

<div class="logo-title">
🚚 NexusFreight
</div>

<div class="logo-sub">

Enterprise Logistics Intelligence Platform

</div>

</div>

""", unsafe_allow_html=True)

    st.markdown(
        "<div class='nav-title'>Navigation</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "🤖   AI Assistant",
        use_container_width=True
    ):
        st.switch_page("streamlit_app.py")

    if st.button(
        "📊   Risk Dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/2_Risk_Dashboard.py")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""

<div class="status-card">

<div class="status-title">

System Status

</div>

<div class="status-item">🟢 Backend Connected</div>

<div class="status-item">🧠 AI Models Ready</div>

<div class="status-item">📚 Knowledge Base Loaded</div>

<div class="status-item">⚡ Hybrid Search Active</div>

</div>

""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🗑 Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# ==========================================================
# HERO
# ==========================================================

if len(st.session_state.messages) == 0:

    st.markdown("""

<div class="hero">
<h1>🚚 Welcome to NexusFreight AI</h1>

<p>

Your intelligent enterprise logistics assistant.

Ask questions about shipments, warehouses, customs,
delivery history, AI predictions, vehicles, carriers,
routes or any logistics documentation.

Everything is powered using a Hybrid AI architecture
combining PostgreSQL + ChromaDB + LLM.

</p>

</div>

""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
### 🚚 Try asking

• Show shipment **5fd50c5c-973f-43bc-a629-06e4b5cd541b**

• List all customers

• Which shipment has high risk?

• Show warehouse details

• Explain Incoterms

• Show delivery history
""")

    with col2:

        st.success("""
### 💡 Capabilities

✅ SQL Database Search

✅ ChromaDB Knowledge Search

✅ Hybrid Retrieval

✅ AI Risk Prediction

✅ Context Memory

✅ Enterprise Logistics Intelligence
""")

# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # ----------------------------
        # Assistant Footer
        # ----------------------------

        if message["role"] == "assistant":

            source = message.get(
                "source",
                "Unknown"
            )

            query = message.get(
                "query_type",
                "Unknown"
            )

            st.markdown(

f"""

<div class="source-card">

<div>

📚 <b>Source</b><br>

{source}

</div>

<div>

🧠 <b>Query</b><br>

{query}

</div>

</div>

""",

unsafe_allow_html=True

            )

# ==========================================================
# QUICK SUGGESTIONS
# ==========================================================

if len(st.session_state.messages) == 0:

    st.markdown("### 💬 Popular Questions")

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🚚 Show Shipment 5fd50c5c-973f-43bc-a629-06e4b5cd541b",
            use_container_width=True,
            key="quick1"
        ):
            st.session_state.quick_prompt = "Show shipment 5fd50c5c-973f-43bc-a629-06e4b5cd541b"

        if st.button(
            "👥 List All Customers",
            use_container_width=True,
            key="quick2"
        ):
            st.session_state.quick_prompt = "List all customers"

        if st.button(
            "📦 List Warehouses",
            use_container_width=True,
            key="quick3"
        ):
            st.session_state.quick_prompt = "List warehouses"

    with c2:

        if st.button(
            "🌍 Explain Incoterms",
            use_container_width=True,
            key="quick4"
        ):
            st.session_state.quick_prompt = "What is Incoterms?"

        if st.button(
            "⚠ High Risk Shipments",
            use_container_width=True,
            key="quick5"
        ):
            st.session_state.quick_prompt = "Show high risk shipments"

        if st.button(
            "🚛 List Vehicles",
            use_container_width=True,
            key="quick6"
        ):
            st.session_state.quick_prompt = "List vehicles"

# ==========================================================
# QUICK PROMPT SUPPORT
# ==========================================================

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None
    
# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "Message NexusFreight AI..."
)

# ----------------------------------------
# Handle Quick Prompt
# ----------------------------------------

if prompt is None and st.session_state.quick_prompt:

    prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None

# ==========================================================
# PROCESS MESSAGE
# ==========================================================

if prompt:

    # -----------------------------
    # USER MESSAGE
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # -----------------------------
    # ASSISTANT
    # -----------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        placeholder.markdown(
            """
🤖 *Thinking...*

Searching PostgreSQL...

Searching Knowledge Base...

Generating Response...
"""
        )

        try:

            result = ask_backend(prompt)

            answer = result.get("bot_response", "No response generated.")
            source = result.get("source", "Unknown")
            query = result.get("query_type", "Unknown")

        except Exception as e:
            answer = f"""
❌ Unable to connect to FastAPI.

Details

{e}
"""

            source = "Offline"

            query = "Connection Error"

        # -------------------------------------
        # Show final answer
        # -------------------------------------

        placeholder.empty()

        st.markdown(answer)

        st.markdown(

f"""

<div class="source-card">

<div>

📚 <b>Source</b><br>

{source}

</div>

<div>

🧠 <b>Query</b><br>

{query}

</div>

</div>

""",

unsafe_allow_html=True

        )

    # -------------------------------------
    # SAVE RESPONSE
    # -------------------------------------

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": answer,

            "source": source,

            "query_type": query

        }

    )

    st.rerun()
    
# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""

<br>
<br>

<div class="footer">

🚚 <b>NexusFreight AI Assistant</b>
<br>
Enterprise Logistics Intelligence Platform
<br><br>
Powered by
<b>Hybrid AI</b>
•PostgreSQL• ChromaDB •LLM
</div>

""", unsafe_allow_html=True)    
