import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
load_dotenv()


query = "What contact number was provided by Yash Bansal"

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")




DB_DIRECTORY = "faiss_chunks"
system_message = (
    "you are a database manager. "
    "your task is to use search_from_database tool to answer the every user query "
    "you are strictly adviced to use the function only if you don't get the answer just say not found the query. "
    "Do not answer this tool for general knowledge or unrelated questions. "
)


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


    normalized_query = query.strip().lower()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorestore = FAISS.load_local(DB_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
    docs = vectorestore.as_retriever(search_type="similarity", search_kwargs = {"score_threshold": 0.8, "k": 4}).invoke(query)
    if not docs:
        return "No matching records found in the database"
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


model = init_chat_model("google_genai:gemini-3.5-flash", temperature = 0)
tools = [search_form_database]
model_with_tools = model.bind_tools(tools)


prompt = [SystemMessage(system_message), HumanMessage(query), ]
tool_call_message = model_with_tools.invoke(prompt)
print(tool_call_message.tool_calls)

for tool_call in tool_call_message.tool_calls:
    selected_tools = {
        "search_form_database": search_form_database, 
    }[tool_call["name"].lower()]
    tool_message = selected_tools.invoke(tool_call)
    print(tool_message)












