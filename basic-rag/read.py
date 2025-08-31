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
PINECONE_REGION  = os.getenv("PINECONE_ENVIRONMENT")  # e.g. "us-west-2"

# ------------------ Init Google Gemini ------------------ #
client = genai.Client(api_key=GOOGLE_API_KEY)

# ------------------ PDF Text Extraction ------------------ #
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    return "\n".join(p.extract_text() or "" for p in reader.pages)

# ------------------ Text Chunking (~500 words) ------------------ #
def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    return [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

# ------------------ Gemini Embedding ------------------ #
def get_gemini_embedding(text):
    resp = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    # resp.embeddings is a List[ContentEmbedding]
    return resp.embeddings[0].values  # List[float]



# ------------------ Main ------------------ #
def run():
    print("Tharan")
    pdf_path = "uploads/Medical_book.pdf"
    print(f"📘 Extracting text from {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)

    print("🔹 Splitting into chunks...")
    chunks = split_text_into_chunks(text)
    print(f"   → {len(chunks)} chunks generated.")

    # *Probe one embedding to get the correct dimension*
    print("🔎 Generating a sample embedding to detect dimension...")
    sample_emb = get_gemini_embedding(chunks[0])
    dimension = len(sample_emb)
    print(f"   → Embedding dimension = {dimension}")

    # ------------------ Init Pinecone (new SDK) ------------------ #
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "medicalbook"

    # Create index if missing, using the detected dimension
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_REGION
            )
        )
    index = pc.Index(index_name)

    # ------------------ Upload All Chunks ------------------ #
    for i, chunk in enumerate(chunks, start=1):
        emb = get_gemini_embedding(chunk)  # List[float] of length dimension
        vid = str(uuid.uuid4())
        index.upsert([
            {"id": vid, "values": emb, "metadata": {"text": chunk}}
        ])
        print(f"✅ Uploaded chunk {i}/{len(chunks)}")

    print(f"\n🎉 Done! {len(chunks)} embeddings uploaded (dim={dimension}).")

run()