from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Create FastAPI app
app = FastAPI(
    title="HR Chatbot API",
    description="API for RAG-powered i2e Consulting chatbot",
    version="1.0.0"
)

# Pydantic models for request and response
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    query: str
    response: str

def initialize_rag_system():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("hr_vdb", embeddings, allow_dangerous_deserialization=True)
    # Initialize LLM
    llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-8b-8192")

    # Setup retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    prompt_template = """
    Using the information contained in the context,
    give a comprehensive answer to the question.
    Respond only to the question asked, response should be concise and relevant to the question.
    Provide the number of the source document when relevant.
    If the answer cannot be deduced from the context, do not give an answer.
            
    Question: {question}
    Context: {context}
            
    Answer: """

    rag_prompt = PromptTemplate(input_variables=["context", "question"], template= prompt_template,)

    rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm | StrOutputParser())
    
    return rag_chain

rag_chain = initialize_rag_system()

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Generate response using RAG chain
        result = rag_chain.invoke(request.query)
        
        # Return formatted response
        return ChatResponse(
            query=request.query,
            response=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)