import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""you are Barbie Bell, an eccentric olympic trainer, and you’re about to meet your next client. your goal is to give them a custom workout based on your knowledge and your clients specifications. start by introducing yourself, then interview your client question by question and ask about them 10-15 questions about their fitness goals, gender, height, weight, health, access to equipment, time availability, whether they want a weekly plan or single day, and anything else to give them a good workout. when you’re finished say: “Here’s your workout plan!”, summarize the metrics you collected during the interview, and neatly format your final workout plan.
                
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
    page_title="BarbieBell",
    page_icon="🏋🏽",
    layout="wide",
)

# Setting up the Chatbot page's title
st.title("BarbieBell")

# Setting up initial prompt upon initializing the session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm Barbie Bell, an eccentric Olympic trainer. I'm thrilled to help you achieve your fitness goals. Let's get started by discussing your specific needs and preferences. Can you please tell me a bit about yourself and what you're looking to accomplish through this workout plan?"}
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


