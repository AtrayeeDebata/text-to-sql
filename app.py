import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq

st.set_page_config(page_title="Text-to-SQL", page_icon="🎵")
st.title("🎵 Text-to-SQL Query Engine")
st.write("Ask questions about the **Chinook Music Store** database in plain English!")

# --- About the Database ---
with st.expander("📂 What's in the Chinook Database? (click to expand)"):
    st.markdown("""
    The Chinook database is a **sample music store** with the following data:
    
    | Table | What it contains |
    |-------|-----------------|
    | Artist | Band/artist names |
    | Album | Albums with artist info |
    | Track | Songs with duration, genre, price |
    | Customer | Customer names, country, email |
    | Invoice | Purchase records with dates |
    | InvoiceLine | Items in each purchase |
    | Employee | Store employees |
    | Genre | Music genres (Rock, Jazz, etc.) |
    | Playlist | Playlists and their tracks |
    
    **Try asking:**
    - How many customers are from Brazil?
    - Which album has the most tracks?
    - List all music genres.
    - What is the total revenue from invoices?
    - Who are the top 5 artists by number of albums?
    - How many employees are there?
    """)

# --- Question Input ---
question = st.text_input("💬 Ask your question:")

if st.button("Get Answer"):
    if not question:
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Generating answer..."):
                # Read API key from Streamlit secrets
                groq_api_key = st.secrets["GROQ_API_KEY"]

                db = SQLDatabase.from_uri("sqlite:///chinook.db")
                llm = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    api_key=groq_api_key,
                    temperature=0
                )

                # Step 1: Generate SQL
                schema = db.get_table_info()
                sql_prompt = f"""You are a SQL expert. Given the database schema below, write a valid SQLite SQL query to answer the question.
Return ONLY the SQL query, nothing else. No explanation, no markdown, just the SQL.

Schema:
{schema}

Question: {question}

SQL Query:"""

                sql_response = llm.invoke(sql_prompt)
                sql_query = sql_response.content.strip()
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

                # Step 2: Execute SQL
                try:
                    db_result = db.run(sql_query)
                except Exception as sql_err:
                    st.error(f"SQL Error: {str(sql_err)}")
                    st.stop()

                # Step 3: Format answer in plain English
                answer_prompt = f"""Given this question: "{question}"
The SQL query ran and returned this result: {db_result}

Give a short, clear, plain English answer to the question based on the result."""

                answer_response = llm.invoke(answer_prompt)
                final_answer = answer_response.content.strip()

                # Display results
                st.subheader("🔍 Generated SQL Query:")
                st.code(sql_query, language="sql")

                st.subheader("✅ Answer:")
                st.success(final_answer)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")