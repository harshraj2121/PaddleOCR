import os
import shutil
import tempfile
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from backend.pythonfiles import search_form_database, valid_query_checker, re_ranker_function, llm_user_op, run_all_files, creating_embeddings, add_embedidngs, search_from_sql, check_if_exists_in_VDB
from fastapi import FastAPI, Depends, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from backend.db_and_sql import create_form, get_db, FormCreate, engine, Base, UserQuery

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
    "You are a database assistant. "
    "Answer only using the database. "
    
    "Use search_form_database for specific record/person/form details. "
    "Use search_from_sql for queries requiring multiple/all records, "
    "counting, filtering, aggregation, grouping, or comparison. "
    
    "Choose the tool based on the operation required, not keywords. "
    "Normally use only one tool per query. "
    
    "If the answer is not found, say: 'Not found in the database. "
)


@app.get("/")
def test_server():
    return "Server is running properly"


@app.post("/userquery")
def userquery(query: UserQuery):
    query = query.user_query

    valid_query = valid_query_checker(query)
    if valid_query == "document_query":
        #tool variables
        model = init_chat_model("groq:openai/gpt-oss-120b", temperature = 0)
        tools = [search_form_database, search_from_sql]
        model_with_tools = model.bind_tools(tools)



        prompt = [SystemMessage(system_message), HumanMessage(query), ]
        tool_call_message = model_with_tools.invoke(prompt)


        tool_call = tool_call_message.tool_calls[0]
        if tool_call["name"] == "search_form_database":
            tool_message = search_form_database.invoke(tool_call)
            tool_content = tool_message.content

            re_ranked_result = re_ranker_function(content= tool_content, query = query)

            final_result = llm_user_op(user_query = query, reranker_op = re_ranked_result)
            return {"reply": final_result}

        if tool_call["name"] == "search_from_sql":
            tool_message = search_from_sql.invoke(tool_call)
            tool_content = tool_message.content

            final_result = llm_user_op(user_query = query, reranker_op = tool_content)  #passing the o/p of toolmessage because there is no need of reranker here
            return {"reply": final_result}


        return {"reply": "Please enter a Valid Query.."}



    else:
        return {"reply": "Please enter a valid query"}

# form_data: FormCreate, isse function me parameter me dena hai
@app.post("/add_form")
def add_form(db: Session = Depends(get_db)):
    ALL_FILES = "pdfs"

    final_chunks, all_results = run_all_files(ALL_FILES)
    creating_embeddings(final_chunks)
    results = []

    for item in all_results:                                           #for item in all_results
        form_data = FormCreate(**item)
        result = create_form(db, form_data)
        results.append(result)


    if results:
        return "done"
    return "Something went wrong!"



# to jan new file upload hogi to pahle database me search hogi ki file exists karti hai ya nahi agar nahi karti hai to pahle uske chunks banenge then embeddings banegi then vector database me store hogi then sql database me
@app.post("/uploadfile")
def regex_str(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if check_if_exists_in_VDB(file.filename):
        return {"message": "file already exists"}
    
    try:
        upload_dir = tempfile.mkdtemp()
        file_path = os.path.join(upload_dir, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunks, all_results = run_all_files(upload_dir)
        print("chunks", chunks)
        print("allresults", all_results)

        shutil.rmtree(upload_dir)
    except:
        return {"message": "Something went wrong.."}


    try:
        add_embedidngs(chunks)
        results = []
        for item in all_results:                                           #for item in all_results
            form_data = FormCreate(**item)
            result = create_form(db, form_data)
            results.append(result)
    
        return {"message": "data successfully added.."}
    except:
        return {"message": "something broke"}

    

if __name__ == "__main__":
    output = userquery("how many male candidates are there")
    print(output)