# AI Chatbot with Natural Language to SQL

A smart AI-powered chatbot that can answer general questions and retrieve data from a PostgreSQL database using natural language. Built with FastAPI, Groq LLM, and Streamlit.

## Features

- **Natural Language to SQL**: Converts user questions into SQL queries automatically
- **Multi-table Support**: Works with 4 related tables (`products`, `customers`, `orders`, `order_items`)
- **Safe SQL Execution**: Only allows `SELECT` queries (blocks INSERT, UPDATE, DELETE, etc.)
- **Dual Mode**: Handles both database queries and general conversation
- **Detailed Logging**: Shows question, generated SQL, raw database response, and timing in terminal
- **Modern Tech Stack**: FastAPI backend + Streamlit frontend

## Tech Stack

- **Backend**: Python, FastAPI, Groq (Llama 3.3)
- **Database**: PostgreSQL
- **Frontend**: Streamlit
- **ORM/Connection**: psycopg2
- **Environment Management**: python-dotenv

## 📁 Project Structure
```
ai-postgres-chatbot/
├── backend/
│   ├── main.py                 # FastAPI app
├── .env.example
│   ├── chatbot.py              # Main logic + logging
│   ├── llm_utils.py            # LLM functions + schema loading
│   ├── database.py             # PostgreSQL connection
│   ├── schema.sql              # Database schema (DDL)
│   └── __init__.py
├── frontend/
│   └── app.py                  # Streamlit chat interface
├── init_db.sql                 # Sample data + table creation
├── requirements.txt
└── README.md
```

## How to Run the Project

## 1. Clone the Repository
```bash
git clone https://github.com/Suyunboyev/ai-postgres-chatbot.git
cd ai-postgres-chatbot
```
## 2. Setup Database
* Install PostgreSQL and pgAdmin
* Create a database named `chatbot_db`
* Run `init_db.sql` script in pgAdmin, `or you can create the tables yourself`

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure Environment
* Copy `.env.example` to `.env`
* Add your Groq API Key and PostgreSQL credentials

## 5. Run the Application
### Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend:
```bash
cd frontend
streamlit run app.py
```
