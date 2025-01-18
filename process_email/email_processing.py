from textblob import TextBlob
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import MessagesPlaceholder

def process_email_content(email_content, chat_history, groq_api_key):
    """
    Process the given email content to analyze sentiment and generate an appropriate response.
    
    Args:
    - email_content (str): The content of the email to be processed.
    - chat_history (list): A list of past messages (human and AI).
    - groq_api_key (str): The API key for Groq service.

    Returns:
    - tuple: (generated response, sentiment label)
    """

    # Sentiment analysis using TextBlob
    sentiment_blob = TextBlob(email_content)
    sentiment = sentiment_blob.sentiment.polarity

    sentiment_label = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"


    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""You are a thoughtful AI assistant capable of analyzing emails and responding with empathy. 
        Based on the sentiment of the email, generate an appropriate and constructive response. 
        If the email is positive, acknowledge the positive tone and express enthusiasm. 
        If the email is negative, provide understanding and offer support, suggesting ways to resolve the issue."""),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ])


    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
    

    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-8b-8192')

    # Initialize the conversation chain
    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )

    response = conversation.predict(human_input=email_content)
    message = {'human': email_content, 'AI': response}
    
    # Save the conversation
    chat_history.append(message)

    return response, sentiment_label
