from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from vector_store import load_vector_store
from config import OPENAI_API_KEY

def get_conversational_chain():
    # Load the vector store
    vector_store = load_vector_store()

    # Initialize the OpenAI Chat model
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", 
        openai_api_key=OPENAI_API_KEY,
        temperature=0.7  # Set temperature for response creativity
    )

    # Create and return the conversational chain
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=vector_store.as_retriever(),
        return_source_documents=True  # Return source documents for better context
    )

    return conversational_chain


"""from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from vector_store import load_vector_store
from config import OPENAI_API_KEY

def get_conversational_chain():
    vector_store = load_vector_store()
    llm = OpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    return ConversationalRetrievalChain.from_llm(llm, retriever=vector_store.as_retriever())
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from vector_store import load_vector_store
from config import OPENAI_API_KEY
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_conversational_chain():
    try:
        # Load the vector store
        logger.info("Loading vector store...")
        vector_store = load_vector_store()
        if vector_store is None:
            raise ValueError("Vector store failed to load.")
        
        # Initialize OpenAI LLM
        logger.info("Initializing OpenAI LLM...")
        llm = OpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
        
        # Set up conversational retrieval chain
        logger.info("Creating ConversationalRetrievalChain...")
        conversational_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(
                search_type="similarity",  # Customize if needed
                search_kwargs={"k": 5}  # Top 5 results
            )
        )
        logger.info("ConversationalRetrievalChain successfully created.")
        return conversational_chain

    except Exception as e:
        logger.error(f"Error initializing conversational chain: {e}")
        raise

# Example usage:
if __name__ == "__main__":
    chain = get_conversational_chain()

""""""from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from vector_store import load_vector_store
from config import OPENAI_API_KEY

def get_conversational_chain():
    vector_store = load_vector_store()
    llm = OpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY) return ConversationalRetrievalChain.from_llm(llm, retriever=vector_store.as_retriever())"""    

