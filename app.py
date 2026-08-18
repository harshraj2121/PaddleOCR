import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from pythonfiles import search_form_database, valid_query_checker, re_ranker_function, llm_user_op, run_all_files
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from db_and_sql import create_form, get_db, FormCreate, engine, Base
from db_and_sql import FormCreate


load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Sabhi origins allow
    allow_credentials=False,      # '*' ke saath True nahi ho sakta
    allow_methods=["*"],          # GET, POST, PUT, DELETE...
    allow_headers=["*"],          # Sabhi headers allow
)


#variables
DB_DIRECTORY = "faiss_chunks"
system_message = (
    "you are a database manager. "
    "you are strictly prohibited not to answer the queries other than database usage. "
    "you have to strictly use search_from_database tool only to answer the every user query. "
    "if you don't get the answer just say not found the query. "
)

@app.get("/")
def test_server():
    return "Server is running properly"


@app.get("/userquery")
def userquery(query):
    query = query.user_query

    valid_query = valid_query_checker(query)
    if valid_query == "document_query":
        #tool variables
        model = init_chat_model("groq:llama-3.3-70b-versatile", temperature = 0)
        tools = [search_form_database]
        model_with_tools = model.bind_tools(tools)



        prompt = [SystemMessage(system_message), HumanMessage(query), ]
        tool_call_message = model_with_tools.invoke(prompt)
        # print(tool_call_message.tool_calls)

        for tool_call in tool_call_message.tool_calls:
            selected_tools = {
                "search_form_database": search_form_database, 
            }[tool_call["name"].lower()]
            tool_message = selected_tools.invoke(tool_call)
            tool_content = tool_message.content

        print("Hold on! we are gathering the information")


        re_ranked_result = re_ranker_function(content= tool_content, query = query)

        final_result = llm_user_op(user_query = query, reranker_op=re_ranked_result)
        print(final_result)
        return final_result


    else:
        print("Enter a valid query")



# form_data: FormCreate, isse function me parameter me dena hai
@app.post("/add_form")
def add_form( db: Session = Depends(get_db)):
    _, all_results = run_all_files()

    results = []
    print(all_results)
    for item in all_results:
        form_data = FormCreate(**item)
        result = create_form(db, form_data)
        results.append(result)

    if results:
        return "done"
    return "Something went wrong!"
