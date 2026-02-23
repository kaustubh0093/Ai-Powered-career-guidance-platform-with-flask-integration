import streamlit as st
from src.utils.text_utils import as_markdown, HAVE_STREAMLIT_CALLBACK

# Optional callback for streamed UI
if HAVE_STREAMLIT_CALLBACK:
    from langchain_community.callbacks import StreamlitCallbackHandler

def create_chat_interface(agent_executor):
    st.subheader("💬 AI Career Assistant")
    st.markdown("Ask anything about careers, skills, pathways, colleges, resumes, or the job market.")

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your career question here..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        context_preview = "\n".join(
            f"{m['role']}: {m['content']}" for m in st.session_state.chat_messages[-8:]
        )
        chat_prompt = f"""You are a helpful AI career advisor with expertise in:
- Career guidance and job market trends (especially in India)
- Indian colleges and universities
- Resume writing and optimization
- Skills development and learning paths

Conversation context:
{context_preview}

User question: {prompt}

Provide a helpful, concise answer. If you need live data about Indian colleges, job markets, or current trends, use the web_search tool.
When discussing education, focus on Indian institutions. When discussing salaries, use INR.
"""

        with st.chat_message("assistant"):
            try:
                if HAVE_STREAMLIT_CALLBACK:
                    container = st.container()
                    cb = StreamlitCallbackHandler(parent_container=container)
                    response = agent_executor.run(chat_prompt, callbacks=[cb])
                else:
                    response = agent_executor.run(chat_prompt)
                st.markdown(as_markdown(response))
                st.session_state.chat_messages.append({"role": "assistant", "content": as_markdown(response)})
            except Exception as e:
                err = f"❌ Error while answering: {e}"
                st.error(err)
                st.session_state.chat_messages.append({"role": "assistant", "content": err})
