from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from pipeline_operation.embedding_config import connection_string, vector_store_langchain
from langchain.memory import PostgresChatMessageHistory
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import  get_buffer_string
from langchain_core.prompts import format_document
from langchain_core.runnables import RunnableParallel
from operator import itemgetter
import os
import json
from dotenv import load_dotenv
load_dotenv() 

def chat_service(data):
   
   
        embed_model=OpenAIEmbeddings(
            api_key=os.environ.get("OPENAI_API_KEY")
            ),
        model =ChatOpenAI(
            model="gpt-4",
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        store=PGVector(
            connection_string=vector_store_langchain(),
            collection_name="data_embedding",
            embedding_function=embed_model,
        )
        retriever=store.as_retriever(
            search_kwargs={'filter':{"configId":data["pipeline_id"]}},
            
            )
       
        history=PostgresChatMessageHistory(
            connection_string=connection_string(),
            table_name="chat_history",
            session_id=str(data["session_id"])
        )
    
        chat_history=history.messages
        

        template = """Answer the question based only on the following context:
                     {context}

                    Question: {question}
                    """
        ANSWER_PROMPT = ChatPromptTemplate.from_template(template)
        _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
                    Chat History:
                    {chat_history}
                    Follow Up Input: {question}
                    Standalone question:"""


        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
        DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


        def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
            doc_strings = [format_document(doc, document_prompt) for doc in docs]
            return document_separator.join(doc_strings)
        
    
        _inputs = RunnableParallel(
            standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: get_buffer_string(x["chat_history"])
         )
        | CONDENSE_QUESTION_PROMPT
        | model
        | StrOutputParser(),
         )
        _context = {
        "context": itemgetter("standalone_question") | retriever | _combine_documents,
        "question": lambda x: x["standalone_question"],
        }
        conversational_qa_chain  =  _inputs | _context | ANSWER_PROMPT | model
        result=conversational_qa_chain.invoke({
            "question":data["question"],
            "chat_history":chat_history
        })
       
        history.add_user_message(data["question"])
        history.add_ai_message(result)
        return json.loads(result.json())["content"]
    



   