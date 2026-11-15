import streamlit as st
import requests
from pathlib import Path
# 1. Page configuration — must come first
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(
    page_title="COLC AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    css_path = Path(__file__).resolve().parent / "style.css"

    with open(css_path, encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")
load_css()
# 2. Session state
if "active_section" not in st.session_state:
    st.session_state.active_section = None


# 3. Button callback
def select_section(section):
    st.session_state.active_section = section


# 4. Prompt card
def prompt_card(icon, title, description, key):
    return st.button(
        title,
        key=f"{key}_click",
        use_container_width=True,
        on_click=select_section,
        args=(key,)
    )


# 5. Main heading
st.markdown("""
<div class="colc-heading">COLC AI</div>
<div class="colc-subtitle">
    Your business operations, one conversation away.
</div>
<div class="colc-section">Quick Actions</div>
<div class="colc-section-subtitle">
    Choose a task to get started.
</div>
""", unsafe_allow_html=True)

    


# 7. Four action buttons
with st.container(key="quick_actions"):
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        prompt_card(
            "👥", "Customer Lookup",
            "Find customer details", "customer"
        )

        prompt_card(
            "📋", "Lead Management",
            "Retrieve lead information", "lead"
        )

    with col2:
        prompt_card(
            "📦", "Order Tracking",
            "Check order status", "order"
        )

        prompt_card(
            "➕", "Create Lead",
            "Add a new business lead", "create_lead"
        )

def display_search_result(message,section):
    with st.container(key="search_result"):
        st.markdown(
            '<div class="result-label">SEARCH RESULT</div>',
            unsafe_allow_html=True
        )
        st.markdown("### AI Response")
        st.write(message)
API_URL = "https://colc-ai.vercel.app/chat"
# 8. Display selected section
if st.session_state.active_section == "customer":
    st.subheader("Customer Lookup")

    name = st.text_input("Customer Name")
    email = st.text_input("Customer Email")
    if st.button("Search", key="customer_search"):
      if name or email:
        message = f"Find customer with name {name} and email {email}"
        try:
          response = requests.post(API_URL,json={"message": message})
          response.raise_for_status()
          result = response.json()

          display_search_result(result["message"], "customer")

        except requests.exceptions.RequestException as e:
          st.error(f"API connection failed: {e}")

elif st.session_state.active_section == "lead":
    st.subheader("Lead Management")

    lead_name = st.text_input("Lead name or source or email:")
    if st.button("Search", key="lead_search"):
        if lead_name:
         message = f"Find customer with lead name {lead_name}"
         try:
             response = requests.post(API_URL, json={"message": message})
             result = response.json()
             display_search_result(result["message"], "lead")
         except requests.exceptions.RequestException as e:
          st.error(f"API connection failed: {e}")
elif st.session_state.active_section == "order":
    st.subheader("Order Tracking")
    order_id = st.text_input("Enter order id")
    if st.button("Search", key="order_search"):
       if order_id:
          message = f"Find order status of {order_id}"
          try:
           response = requests.post(API_URL, json={"message":message})
           result = response.json()
           display_search_result(result["message"], "order")
          except requests.exceptions.RequestException as e:
                    st.error(f"API connection failed: {e}")
elif st.session_state.active_section == "create_lead":
    st.subheader("Create Lead")
    name = st.text_input("Enter name:")
    email = st.text_input("Enter email:")
    source = st.text_input("Enter source:")
    if st.button("Create", key="create_lead"):
       message = f"Create a new business lead with {name}, {email}, and {source}."
       try:
          response = requests.post(API_URL, json={"message":message})
          result = response.json()
          display_search_result(result["message"], "Create Lead")
       except requests.exceptions.RequestException as e:
            st.error(f"API connection failed: {e}")      


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
if prompt := st.chat_input("Ask COLC AI anything..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user", avatar=":material/person:"):
        st.write(prompt)
    response = requests.post(API_URL, json={"message": prompt})
    result = response.json()
    answer = result["message"]
    st.session_state.messages.append({"role":"assistant", "content": answer})
    with st.chat_message("assistant",avatar=":material/smart_toy:"):
     st.write(answer)
if st.session_state.messages != []:
 if st.button("Clear chat", key="clear_chat"):
    st.session_state.messages.clear()
    st.rerun()