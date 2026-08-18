import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = init_chat_model("groq:openai/gpt-oss-120b")
query_checker_model = init_chat_model("groq:openai/gpt-oss-20b")



def valid_query_checker(query: str):
    messages = f"""Classify the following user message as either:
            - "document_query": a question about any person, scanned forms, applicants, dates, fields, or content
            - "other": greetings, small talk, unrelated, or too vague to answer

            Message: "{query}"
            Respond with only one word: document_query or other"""
    response = query_checker_model.invoke(messages)
    return response.content
    


systemPrompt = (
    "You are an expert doucment handler. "
    "Your task is to read the given text and extract specific fields. "
    "You must return the output strictly in JSON format with no extra text. "
    "The JSON must contain the following keys: form_id, form_type, application_number, applicant_name, submission_date, complete_address, martial_status, contact_number, email, city, gender. "
    "If a value is missing, set it to null. "
    "Do not include explanations, comments, or any text outside of JSON."
    )



# function to get desired json from the ocr_text
def llm_call(human_prompt: str) -> dict:
    messages = [HumanMessage(human_prompt), SystemMessage(systemPrompt)]

    try:
        response = model.invoke(messages)
        content = response.content

        json_content = json.loads(content)
        return json_content

    except:
        return {
            "form_id": None,
            "form_type": None,
            "application_number": None,
            "applicant_name": None,
            "submission_date": None,
            "complete_address": None,
            "gender": None,
            "contact_number": None,
            "email": None,
            "city": None,
        }




def llm_user_op(user_query, reranker_op):
    systemPrompt = (
        "You are an excelent AI information extractor. "
        "Your are given the user Query and some information form the database. "
        "You have to give response to the user Query strictly form the information provided. "
        "you are srtictly restricted not response anything other than the provided information. "
        "you have to give short and clear response in a single parageaph format"
    )

    humanPrompt = (
        f"""Query: {user_query}
            content: {reranker_op}
        """
    )

    prompt = [SystemMessage(systemPrompt), HumanMessage(humanPrompt)]

    try:
        response = model.invoke(prompt)
        return response.content

    except:
        return "Something went wrong"





if __name__ == "__main__":

    sample_text = """
    INSURANCE ENROLLMENT FORM
    FORM_002
    APPLICATION DETAILS
    Application No.: APP-2024-0002 Submission Date: 2024-03-07
    Applicant Name: Mohit Mishra Date of Birth: 1989-05-05
    Gender: Other Marital Status: Prefer not to say
    CONTACT INFORMATION
    Address: 75 Model Town
    City: Ahmedabad State: Gujarat
    Postal Code: 380001 Phone: 9876543002
    Email: mohit.mishra2@example.com
    SERVICE SELECTION
    Selected Plan: Basic Standard Premium
    Application Status: Approved
    OFFICE NOTES
    Applicant requested SMs updates.
    Applicant Signature Authorized Officer
    Synthetic training document — no real personal information.
    """

    print(llm_call(sample_text))