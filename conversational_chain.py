from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from vector_store import load_vector_store
from langchain.chat_models import ChatOpenAI
from your_config import OPENAI_API_KEY
import logging

logging.basicConfig(level=logging.INFO)

def get_conversational_chain():
    try:
        vector_store = load_vector_store()
        llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            openai_api_key=OPENAI_API_KEY,
            temperature=0.7
        )

        conversational_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, 
            retriever=vector_store.as_retriever(),
            return_source_documents=True
        )

        logging.info("Conversational chain initialized successfully.")
        return conversational_chain

    except Exception as e:
        logging.error(f"Error initializing conversational chain: {e}")
        raise e