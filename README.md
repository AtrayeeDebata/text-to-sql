# Text-to-SQL Natural Language Query Engine

A conversational AI system that converts plain English questions into SQL queries and fetches real answers from a relational database — no SQL knowledge required.

## Demo
> ❓ "How many customers are from Brazil?"
> ✅ Answer: 5

## Tech Stack
| Component | Technology |
|---|---|
| Framework | LangChain |
| LLM | Llama 3.3 70B via Groq API |
| Database | Chinook SQLite |
| Environment | Kaggle Notebook |
| Language | Python |

## Features
- Natural language → SQL conversion using Llama 3.3 70B
- Automatic database schema parsing via LangChain SQLDatabaseChain
- Error handling for out-of-scope queries
- Interactive user input support

## How It Works
1. User types a plain English question
2. LangChain sends it to Groq (Llama 3.3 70B)
3. LLM generates the SQL query
4. SQL runs on Chinook SQLite database
5. Clean answer is returned to the user

## Setup
```bash
pip install langchain langchain-community langchain-groq langchain-experimental
```
Add your Groq API key and run all cells in the notebook.

## Database
Uses the [Chinook Database](https://github.com/lerocha/chinook-database) — a sample music store database with artists, albums, tracks, customers and invoices.
