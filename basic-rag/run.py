import os
from PyPDF2 import PdfReader
from pinecone import Pinecone, ServerlessSpec
from google import genai
from google.genai import types
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY   = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION  = os.getenv("PINECONE_ENVIRONMENT")  

client = genai.Client(api_key=GOOGLE_API_KEY)

def get_gemini_embedding(text):
    resp = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    # resp.embeddings is a List[ContentEmbedding]
    return resp.embeddings[0].values  # List[float]



def answer_question(query):
    print(f"\n💬 User query: {query}")
    
    # Get embedding for the user query
    query_embedding = get_gemini_embedding(query)

    # Connect to Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("medicalbook")

    # Retrieve top-k relevant chunks
    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )
    
    if not results.matches:
        print("❌ No relevant context found.")
        return

    # Collect matched text chunks
    contexts = [match["metadata"]["text"] for match in results.matches]
    context_text = "\n\n".join(contexts)

    # Construct prompt for Gemini
    prompt = f"""Use the following context to answer the user's question:

Context:
{context_text}

Question: {query}
Answer:

"""

    print("\n🧠 Generating answer from Gemini...")
    response = client.models.generate_content(model="gemini-2.0-flash",contents= prompt)
    print("\n📝 Gemini's Response:")
    print(response.text)


# ------------------ Entry Point ------------------ #
if __name__ == "__main__":
    # Sample Q&A loop after embeddings are uploaded
    while True:
        user_query = input("\n🔎 Enter a question (or type 'exit'): ")
        if user_query.lower() == "exit":
            break
        answer_question(user_query)
