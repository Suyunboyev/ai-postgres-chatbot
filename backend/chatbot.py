# chatbot.py - Enhanced logging with database raw response and timing

import time
from database import execute_query
from llm_utils import (
    is_database_query,
    generate_sql_query,
    is_safe_sql,
    get_llm_response
)

def process_user_query(question: str) -> str:
    """Main logic with detailed terminal logging"""
    
    start_total = time.time()

    print("\n" + "="*90)
    print(f"👤 USER QUESTION: {question}")
    print("="*90)

    # Step 1: Classify question
    classify_start = time.time()
    is_db = is_database_query(question)
    classify_time = time.time() - classify_start

    print(f"📊 CLASSIFICATION: {'DATABASE QUERY' if is_db else 'GENERAL CONVERSATION'}")
    print(f"   ⏱️  Classification time: {classify_time:.3f} seconds")

    if is_db:
        # === DATABASE PATH ===
        print("\n🔍 Generating SQL query...")

        # SQL Generation
        sql_start = time.time()
        sql = generate_sql_query(question)
        sql_time = time.time() - sql_start

        print(f"📝 GENERATED SQL:\n{sql}")
        print(f"   ⏱️  SQL Generation time: {sql_time:.3f} seconds")

        # Safety Check
        if not is_safe_sql(sql):
            response = "❌ Sorry, only safe SELECT queries are allowed."
            print("🚫 Unsafe SQL blocked by security check!")
        else:
            # Execute Query on Database
            print("\n⚡ Executing query on PostgreSQL...")
            db_start = time.time()
            raw_result = execute_query(sql)
            db_time = time.time() - db_start

            print(f"📊 RAW DATABASE RESPONSE:")
            print(raw_result)
            print(f"   ⏱️  Database execution time: {db_time:.3f} seconds")

            # Create final readable answer
            if isinstance(raw_result, str) and "error" in raw_result.lower():
                response = f"❌ Database error: {raw_result}"
            elif not raw_result:
                response = "No data found for your query."
            else:
                print("\n✍️  Generating natural language answer from raw data...")
                data_str = str(raw_result[:12])  # Limit to avoid very long prompts

                format_start = time.time()
                format_prompt = f"""User asked: "{question}"

Raw data from database:
{data_str}

Please convert this into a friendly, natural, and easy-to-read answer.
Use bullet points for multiple items. Be clear and concise."""

                response = get_llm_response(format_prompt, "You are a helpful assistant.")
                format_time = time.time() - format_start

                print(f"   ⏱️  Final answer generation time: {format_time:.3f} seconds")

    else:
        # === GENERAL CONVERSATION PATH ===
        print("\n💬 Handling as general conversation with LLM...")

        llm_start = time.time()
        response = get_llm_response(
            question,
            "You are a friendly and helpful AI chatbot."
        )
        llm_time = time.time() - llm_start

        print(f"   ⏱️  LLM response time: {llm_time:.3f} seconds")

    # Final Summary
    total_time = time.time() - start_total

    print("\n" + "-"*90)
    print(f"🤖 FINAL ANSWER TO USER:\n{response}")
    print("-"*90)
    print(f"⏱️  TOTAL PROCESSING TIME: {total_time:.3f} seconds")
    print("="*90 + "\n")

    return response