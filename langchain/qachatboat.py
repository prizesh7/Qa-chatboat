from prompt_toolkit import prompt
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import os

st.set_page_config(page_title="Simple LangChain Chat with Groq", page_icon=":robot_face:")
st.title("Simple LangChain Chat with Groq")
st.markdown("Learn LangChain with Groq")

with st.sidebar:
    st.header("Settings")
    
    api_key= st.text_input("Groq API Key", type="password", help="GET key at console.groq.com.")  
      
    model_name = st.selectbox(
        "Model", 
        ["openai/gpt-oss-120b", "openai/gpt-oss-20b"],
        index=0
    ) 
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        
if "messages" not in st.session_state:
    st.session_state.messages = []

##init LLM 
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None
    
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=0.7,
        streaming=True
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant powered by GROQ. Answer the questions in proper way."),
            ("user", "{question}")
        ]
    )
   
    chain = prompt | llm | StrOutputParser()
    return chain

chain=get_chain(api_key, model_name)

if not chain:
    st.warning("Please enter your Groq API Key to start chatting.")

else:
    ## display the chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    ## chat input
    
    if question:=st.chat_input("Ask Me Anything:"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in chain.stream({"question": question}):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌") 
             
            message_placeholder.markdown(full_response)
        
            st.session_state.messages.append({"role": "assistant", "content": full_response})
       
                                                                                                                          