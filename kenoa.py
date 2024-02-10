import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""you are KENoa, and your friend, barbie the personal trainer, just recommended a workout to your client. based on their conversation and your knowledge, create a nutrition plan for your client. tell them what types of food to eat and what to avoid, with examples of both.

                
                chat_history: {chat_history}

                Human: {question}
                
                AI:"""
)

# Configuring AI
llm = ChatOpenAI(openai_api_key="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")
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)
llm_chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt
)

# Configuring page details
st.set_page_config(
    page_title="KENoa",
    page_icon="🍚",
    layout="wide",
)

# Setting up the Chatbot page's title
st.title("KENoa")

# Setting up initial prompt upon initializing the session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Tell me about your diet"}
    ]

# Displaying the initial messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    
# Setting up user's ability to chat with bot
user_prompt = st.chat_input()
if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

# Check whether the last message in the chat history was a prompt or not
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = llm_chain.predict(question=user_prompt)
            st.write(ai_response)
    new_ai_message = {"role": "assistant", "content": ai_response}
    st.session_state.messages.append(new_ai_message)


