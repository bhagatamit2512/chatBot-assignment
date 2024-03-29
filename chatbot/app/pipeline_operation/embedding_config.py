import os
from langchain_community.vectorstores.pgvector import PGVector
from pipeline_operation.file_loader import FileLoader
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv() 
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
db_driver=os.environ.get("DB_DRIVER")

def process_file(pipeline_id_value,filename):
    file_extension=os.path.splitext(filename)[1]
    loader=FileLoader(filename,file_extension)
    documents=loader.load_data()
    extra_metadata=[
         ("configId", str(pipeline_id_value))
    ]
    for document in documents:
        for key, value in extra_metadata:
            document.metadata[key] = value
    return documents


def vector_store_langchain():
    return PGVector.connection_string_from_db_params(
        driver=db_driver,
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )

def generate_embeddings(documents,table_name="data_embedding"):
    store=PGVector.from_documents(
        embedding=OpenAIEmbeddings(
            openai_api_key=os.environ.get("OPENAI_API_KEY")
            ),
        documents=documents,
        collection_name=table_name,
        connection_string=vector_store_langchain()
    )

    return "Embedding generation completed!"

def connection_string():
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    