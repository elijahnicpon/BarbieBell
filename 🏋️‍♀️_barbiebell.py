from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *

#Header for page
st.subheader("Barbiebell 🏋️ the PT Assistant")


#Initializes the storage of responses and request
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["What would you like help with?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory=ConversationBufferWindowMemory(k=30,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="Barbiebell, Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say 'I don't know'")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

st.title("Barbiebell Chatbot")
...
response_container = st.container()
textcontainer = st.container()
...
with textcontainer:
    query = st.text_input("Query: ", key="input")
    ...
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")

...
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

prompt = """
You are Barbie Bell, an eccentric Olympic trainer, and you’re about to meet your next client. Your goal is to give them a custom workout based on your knowledge and your client's specifications. Start by introducing yourself, then interview your client question by question and ask about them 10-15 questions about their fitness goals, gender, height, weight, health, access to equipment, time availability, whether they want a weekly plan or single day, and anything else to give them a good workout. When you’re finished say: “Here’s your workout plan!”, summarize the metrics you collected during the interview, and neatly format your final workout plan.
"""

# Use the 'prompt' variable when interacting with the AI
response = conversation.predict(input=prompt)


if query:
    with st.spinner("typing..."):
        ...
        response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
    st.session_state.requests.append(query)
    st.session_state.responses.append(response)
