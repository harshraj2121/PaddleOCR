from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool



DB_DIRECTORY = "faiss_chunks"


@tool
def search_form_database(query: str) -> str:
    """
    use this function to asnwer user query when user asks something
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorestore = FAISS.load_local(DB_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
    docs = vectorestore.as_retriever(search_kwargs = {"k": 3}).invoke(query)
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

