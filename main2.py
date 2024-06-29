import streamlit as st
import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession
import os

os.environ['GRPC_DNS_RESOLVER'] = 'native'

project = "explorer-gemini"
vertexai.init(project = project)

config = generative_models.GenerationConfig(temperature=0.4)
model = GenerativeModel('gemini-pro',generation_config=config)
chat = model.start_chat()

st.title("Gemini Chatbot")
#clear_button = st.button('Clear Chat',type='primary')
if "messages" not in st.session_state:
    st.session_state.messages = [] # Create message history as empty list 
    st.session_state.messages.append({"role": "user", "content": '->Ask my name and refer to me with personalized greetings. You are a witty, funny chatbot that makes cringe jokes!'})
    st.session_state.messages.append({"role": "model","content": '->I have undertood the instructions.'})

for index, message in enumerate(st.session_state.messages):
    # Code for displaying and loading chat history
    content = Content(
        role=message['role'],
        parts= [Part.from_text(message['content'])])

    if index !=0 and index!=1:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    chat.history.append(content)

def llm_function(chat: ChatSession, query):
    with st.chat_message("user"):
        st.markdown(query)
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text
    with st.chat_message('model'):
        st.markdown(output)
    st.session_state.messages.append({'role':'user','content':query})
    st.session_state.messages.append({'role':'model','content':output})
    # message = st.session_state.messages[-1]
    # content = Content(
    #     role=message['role'],
    #     parts= [Part.from_text(message['content'])])
    # chat.history.append(content)
    # # Code for handling messages and displaying them in Streamlit
    # message = st.session_state.messages[-2]
    # content = Content(
    #     role=message['role'],
    #     parts= [Part.from_text(message['content'])])
    # chat.history.append(content)
    


# If user prompt is not empty
if prompt:= st.chat_input('What is up?'):
    llm_function(chat,prompt)