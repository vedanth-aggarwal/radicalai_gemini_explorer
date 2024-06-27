import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession
import os

os.environ['GRPC_DNS_RESOLVER'] = 'native'
# https://console.cloud.google.com/apis/api/aiplatform.googleapis.com/metrics?project=explorer-gemini
project = "explorer-gemini"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

model = GenerativeModel(
    'gemini-pro',
    generation_config=config
)

chat = model.start_chat()

def llm_function(chat: ChatSession, query):
    # Code for handling messages and displaying them in Streamlit
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message('model'):
        st.markdown(output)
    
    st.session_state.messages.append(
        {
            'role':'user',
            'content':query
        }
    )

    st.session_state.messages.append(
        {
            'role':'model',
            'content':output
        }
    )


st.title("Gemini Explorer")
if "messages" not in st.session_state:
    st.session_state.messages = []

for index, message in enumerate(st.session_state.messages):
    # Code for displaying and loading chat history
    content = Content(
        role=message['role'],
        parts= [Part.from_text(message['content'])]
    )

    if index !=0:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    chat.history.append(content)

# Step 3: Capture User Information
query = st.text_input(f'User: ')

if query:
    if len(st.session_state.messages) == 0:
        query1 = f"My name is {query} - Refer to me with personalized greetings over this discussion!Be very funny!!"
        llm_function(chat, query1)
    else:
        with st.chat_message('user'):
            st.markdown(query)
        llm_function(chat, query)
    
    
