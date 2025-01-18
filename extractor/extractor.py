# extractor.py
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import LLMChain  # Add this import

def extract_time_place_location_date(email_content, groq_api_key):
    """
    Extract time, place, location, and date from the email content using the Groq API and a custom prompt.
    
    Args:
    - email_content (str): The content of the email to be processed.
    - groq_api_key (str): The Groq API key for processing.
    
    Returns:
    - dict: Extracted time, place, location, and date information.
    """
    
    # Define the prompt for extracting the desired information
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""You are a helpful assistant capable of extracting key details from an email. 
        Please extract and return the following details from the email content: 
        - Time 
        - Place
        - Location
        - Date

        Only extract the specific details mentioned, without any additional context or explanation."""),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ])

    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-8b-8192')

    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
        memory=memory
    )
    
    # Generate the response from Groq API
    response = conversation.predict(human_input=email_content)
    
    extracted_info = {
        'dates': [],
        'times': [],
        'places': [],
        'locations': []
    }

    if response:
        lines = response.split("\n")
        for line in lines:
            if "Date" in line:
                extracted_info['dates'].append(line.replace("Date:", "").strip())
            elif "Time" in line:
                extracted_info['times'].append(line.replace("Time:", "").strip())
            elif "Place" in line:
                extracted_info['places'].append(line.replace("Place:", "").strip())
            elif "Location" in line:
                extracted_info['locations'].append(line.replace("Location:", "").strip())
    
    return extracted_info
