import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_experimental.sql import SQLDatabaseChain

st.set_page_config(page_title="Text-to-SQL", page_icon="🎵")
st.title("🎵 Text-to-SQL Query Engine")
st.write("Ask questions about the Chinook music store database in plain English!")

groq_api_key = st.text_input("Enter your Groq API Key", type="password")

st.markdown("**Example questions you can ask:**")
st.markdown("- How many customers are from Brazil?")
st.markdown("- List all artists names.")
st.markdown("- Which album has the most tracks?")
st.markdown("- How many invoices were made in 2009?")

question = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if not groq_api_key:
        st.error("Please enter your Groq API key.")
    elif not question:
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Thinking..."):
                db = SQLDatabase.from_uri("sqlite:///chinook.db")
                llm = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    api_key=groq_api_key,
                    temperature=0
                )
                chain = SQLDatabaseChain.from_llm(
                    llm=llm,
                    db=db,
                    verbose=False,
                    return_intermediate_steps=True
                )
                result = chain.invoke({"query": question})

                # Extract SQL query
                try:
                    steps = result.get("intermediate_steps", [])
                    if steps:
                        for step in steps:
                            if isinstance(step, dict) and "input" in step:
                                sql = step["input"]
                                if "SQLQuery:" in sql:
                                    sql = sql.split("SQLQuery:")[-1].strip()
                                    sql = sql.split("SQLResult:")[0].strip()
                                    st.subheader("Generated SQL Query:")
                                    st.code(sql, language="sql")
                                    break
                except:
                    pass

                # Extract clean final answer
                raw = result.get("result", "")
                if "Answer:" in raw:
                    clean = raw.split("Answer:")[-1].strip()
                elif "SQLResult:" in raw:
                    clean = raw.split("SQLResult:")[-1].strip()
                else:
                    clean = raw.strip()

                st.subheader("Answer:")
                st.success(clean)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")