import argparse
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai

load_dotenv()

PROMPT_TEMPLATE = """
Context:  
The AI has access to a PDF document uploaded by the user, which contains information relevant to the query. The AI can analyze the content extracted from the document and use its reasoning to provide a meaningful response.

Instructions:  
- Analyze the uploaded PDF document to find relevant content addressing the user's query.  
- Provide a clear and definitive answer based on the document's content.  
- If the answer is not directly available but can be inferred using logical reasoning, provide a well-reasoned response without relying on vague phrases or indirect references.  
- If the information is not found or cannot be inferred, state clearly that it is not available in the document.  
- Avoid phrases like "the document mentions" or "according to the text." Instead, deliver the response as a straightforward, actionable answer.  
- Use professional, concise, and user-friendly language to provide the most helpful response.

AI Agent Guidelines:  
1. Utilize both the document's content and reasoning capabilities to generate a single, clear answer.  
2. Do not speculate without evidence or inference grounded in the document or common knowledge.  
3. If further clarification or elaboration is requested, provide thoughtful follow-up explanations based on the document's content.  
4. Deliver one coherent, actionable response tailored to the user's needs, ensuring the answer is direct and easy to understand.  

User Context:  
{context}

Input Query:  
{question}

Now, analyze the uploaded PDF and respond to the user's query effectively using these guidelines.

"""
CHROMA_PATH = "chroma"

api_key = os.getenv("API_KEY")

while True:
    query_text = str(input("Ask: "))

    genai.configure(api_key=api_key)

    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=api_key)
    db = Chroma(persist_directory=CHROMA_PATH,embedding_function=embedding_function)
    results = db.similarity_search_with_relevance_scores(query_text,k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text,question=query_text)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt).text
    print(response)