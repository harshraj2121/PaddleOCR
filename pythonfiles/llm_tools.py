# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.tools import tool
# from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from sqlalchemy import text
from db_and_sql.database import get_db




DB_DIRECTORY = "faiss_chunks"
model = init_chat_model("groq:openai/gpt-oss-120b")



# @tool
# def search_form_database(query: str) -> str:
#     """
#     Search the form database for query about people or applicant_name,
#     forms, applications, documents, fields, and other information
#     stored in the form database.

#     Use this tool when the user's question requires information
#     from the form database.

#     Do not use this tool for general knowledge or unrelated questions.
#     """

#     # normalized_query = query.strip().lower()
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
#     vectorestore = FAISS.load_local(DB_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
#     docs = vectorestore.as_retriever(search_type="similarity", search_kwargs = {"score_threshold": 0.8, "k": 10}).invoke(query)
#     if not docs:
#         return "No matching records found in the database"
#     # return "\n\n---\n\n".join(doc.page_content for doc in docs)
#     return [doc.page_content for doc in docs]


# @tool
def search_from_sql(user_query: str) -> str:
    """
    Search the SQL database using the user's question.
    Use this tool whenever the user asks about information stored in the database.
    """

    try:
        sql_prompt = f"""
            You are a SQL query generator.
            Database table: forms
            columns:
            - id
            - application_number
            - applicant_name
            - form_id
            - gender
            - contact_number
            - email
            - city
            - complete_address
            - form_type
            - submission_date
            - martial_status
            - source_file

            User question:
            {user_query}

            Rules:
            - Always generate SELECT queries only.
            - Always use LIKE with wildcards (e.g., '%Yash%') instead of exact matches.
            - Select applicant_name also when you have queries for gender, city, submission_date, martial_status
            - Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE or any other query.

            SQL:
        """
        response = model.invoke(sql_prompt)
        sql_query = response.content.strip()

        #removes markdown if llm returns ```sql
        sql_query = sql_query.replace("```sql", "")
        sql_query = sql_query.replace("```", "").strip()

        #validator
        if not sql_query.lower().startswith("select"):
            return "Invalid database query."

        db = next(get_db())
        result =  db.execute(text(sql_query))
        rows = result.mappings().all()

        return rows


    except Exception as e:
        return f"Database Error: {str(e)}"

if __name__ == "__main__":
    result= search_from_sql("what is the gender of yash")
    print(result)