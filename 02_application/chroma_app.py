from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import threading
import uvicorn
from typing import Any, Union
import chromadb
from chromadb.utils import embedding_functions


EMBEDDING_MODEL_REPO = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"
EMBEDDING_FUNCTION = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)



COLLECTION_NAME = os.getenv('COLLECTION_NAME')

DEBUG = os.getenv('DEBUG') or 0

print("initialising Chroma DB connection...")
chroma_client = chromadb.PersistentClient(path="/home/cdsw/chroma-data")
print("Chroma DB initialised")

print(f"Getting '{COLLECTION_NAME}' as object...")
try:
    collection = chroma_client.get_collection(name=COLLECTION_NAME, embedding_function=EMBEDDING_FUNCTION)
except ValueError:
    print("Creating new collection...")
    collection = chroma_client.create_collection(name=COLLECTION_NAME, embedding_function=EMBEDDING_FUNCTION)
    print("Success")

# Get latest statistics from index
current_collection_stats = collection.count()
print('Total number of embeddings in Chroma DB index is {}.'.format(current_collection_stats))

app = FastAPI()

# Helper function to return the number of documents in the collection
def count_documents():
    results = collection.count()
    return results

# Helper function for generating responses for the Chroma DB
def get_responses(question, max_results):
    results = collection.query(query_texts=question, n_results=max_results)
    if DEBUG:
        print(f"Response: {results}")
    return results


# Helper function for adding documents to the Chroma DB
# returns
def upsert_document(document, metadata=None, classification="public", ids=None):

    # Push document to Chroma vector db
    try:
        if ids is not None:
            collection.add(
                documents=[document],
                metadatas=[{"classification": classification}],
                ids=[ids]
            )
        else:
            collection.add(
                documents=[document],
                metadatas=[{"classification": classification}],
                ids=document[:50]
            )
        response = "Document inserted"
    except ValueError as e:
        response = "Error while inserting document"
    return response

# Return the Knowledge Base doc based on Knowledge Base ID (relative file path)
def load_context_chunk_from_data(id_path):
    with open(id_path, "r") as f: # Open file in read mode
        return f.read()

@app.get("/")
def status_gpu_check() -> dict[str, str]:
    chroma_status = "Chroma Vector DB READY" if collection else "Unavailable"
    return {
        "server_status": "Web server is ALIVE",
        "chroma_status": chroma_status
    }

# This defines the data json format expected for the endpoint, change as needed
class TextInput(BaseModel):
    inputs: str
    parameters: Union[dict[str, Any], None]

@app.post("/upsert")
def upsert_endpoint(data: TextInput) -> dict[str, Any]:
    try:
        document = data.inputs
        params = data.parameters or {}
        if DEBUG:
            print(str(document))

        if 'metadata' in params:
            metadata = str(params['metadata'])
            if DEBUG:
                print("Using: "+ str(metadata))
        else:
            metadata = None

        if 'classification' in params:
            classification = str(params['classification'])
        else:
            classification = "public"
        if DEBUG:
            print("Using: "+ str(classification))

        if 'ids' in params:
            ids = str(params['ids'])
            if DEBUG:
                print("Using: "+ str(ids) + " as ids")
        else:
            ids = None

        res = upsert_document(document, metadata, classification, ids)

        return {"response": res}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_endpoint(data: TextInput) -> dict[str, Any]:
    try:
        question = data.inputs
        params = data.parameters or {}

        if 'max_results' in params:
            max_results = int(params['max_results'])
        else:
            max_results = 1

        res = get_responses(question, max_results)
        return {"response": res}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/count")
def count_endpoint() -> dict[str, Any]:
    return {"Collection": COLLECTION_NAME, "Count": count_documents()}


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ['CDSW_APP_PORT']), log_level="warning", reload=False)

server_thread = threading.Thread(target=run_server)
server_thread.start()