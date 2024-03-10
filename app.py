import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import os
try:
    # Tentative de connexion à Hugging Face
    hf_email = st.secrets['EMAIL']
    hf_pass = st.secrets['PASS']
except Exception as e:
    st.error(f"Erreur lors de la connexion : {e}")


# App title
st.set_page_config(page_title="TAL-IA Chat free")

# Hugging Face Credentials
with st.sidebar:
    st.title('🤗💬 TAL-IA')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    st.markdown('📖 Talandria.fr')

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut comment puis je t'aider aujourd'hui ?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Salut comment puis je t'aider aujourd'hui?"}]
st.sidebar.button('Effacer la discussion', on_click=clear_chat_history)

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    for dict_message in st.session_state.messages:
        string_dialogue = "Tu es un assistant très intelligent et sympatique, tu réponds toujours en français."
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    prompt = f"{string_dialogue} {prompt_input} Assistant: "
    return chatbot.chat(prompt)

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Je réfléchis..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)