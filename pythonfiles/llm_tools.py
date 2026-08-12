from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool



DB_DIRECTORY = "faiss_chunks"


@tool
def search_form_database(query: str) -> str:
    """
    Search the form database for query about people or applicant_name,
    forms, applications, documents, fields, and other information
    stored in the form database.

    Use this tool when the user's question requires information
    from the form database.

    Do not use this tool for general knowledge or unrelated questions.
    """

    # normalized_query = query.strip().lower()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorestore = FAISS.load_local(DB_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
    docs = vectorestore.as_retriever(search_type="similarity", search_kwargs = {"score_threshold": 0.8, "k": 10}).invoke(query)
    if not docs:
        return "No matching records found in the database"
    # return "\n\n---\n\n".join(doc.page_content for doc in docs)
    return [doc.page_content for doc in docs]