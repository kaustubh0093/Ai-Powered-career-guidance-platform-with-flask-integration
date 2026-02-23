def as_markdown(output):
    """
    Output cleaning helper for all model/agent outputs.
    """
    val = getattr(output, "content", None)
    if val is None:
        val = str(output)
    if val.startswith("content='") or val.startswith('content="'):
        start = val.find("'") + 1 if "'" in val else val.find('"') + 1
        val = val[start:]
        if val.endswith("'") or val.endswith('"'):
            val = val[:-1]
    val = val.replace("\\n", "\n").replace("\r", "")
    while "\n\n\n" in val:
        val = val.replace("\n\n\n", "\n\n")
    return val.strip()

# Optional callback for streamed UI (depends on LangChain version)
try:
    from langchain_community.callbacks import StreamlitCallbackHandler
    HAVE_STREAMLIT_CALLBACK = True
except Exception:
    HAVE_STREAMLIT_CALLBACK = False
