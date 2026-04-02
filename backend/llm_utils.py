# llm_utils.py - Reads schema from file + generates SQL safely

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("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"))

# Read schema from external SQL file
def load_schema() -> str:
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Schema file not found. Please create schema.sql"

DATABASE_SCHEMA = load_schema()

def get_llm_response(prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Current stable model on Groq
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

def is_database_query(question: str) -> bool:
    prompt = f"""Classify this user question.
If it asks about products, customers, orders, order items, prices, statistics, lists, or any data from the database → answer 'yes'
If it's greeting, casual talk, or general knowledge → answer 'no'

Question: {question}
Answer ONLY with 'yes' or 'no'."""
    
    resp = get_llm_response(prompt, "You are a strict classifier.").lower().strip()
    return resp.startswith("yes")

def generate_sql_query(question: str) -> str:
    """Generate SQL by reading schema from schema.sql file"""
    prompt = f"""You are an expert PostgreSQL SQL developer.

Here is the complete database schema from schema.sql:

{DATABASE_SCHEMA}

Rules:
- Generate ONLY SELECT queries. Never use INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, etc.
- Use proper JOINs when needed (use table aliases like p for products, c for customers, o for orders, oi for order_items)
- Return ONLY the raw SQL query. No explanation, no markdown, no ```sql.

User Question: {question}

SQL Query:"""

    sql = get_llm_response(prompt, "You are a precise SQL expert.")
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def is_safe_sql(sql: str) -> bool:
    if not sql:
        return False
    sql_upper = sql.upper().strip()
    if not sql_upper.startswith("SELECT"):
        return False
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE", "EXEC"]
    if any(word in sql_upper for word in forbidden):
        return False
    if sql.count(";") > 1:
        return False
    return True