from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import LLMChain
from icalendar import Calendar, Event
from datetime import datetime
import pytz
import os
from textblob import TextBlob

app = FastAPI()

groq_api_key = "enter api key"

class EmailRequest(BaseModel):
    email_content: str

class EventData(BaseModel):
    summary: str
    description: str
    start_date: str  
    start_time: str  
    end_date: str    
    end_time: str   
    timezone: str = "UTC"  

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

def create_ics_file(event_data):
    calendar = Calendar()

    event = Event()
    event.add('summary', event_data['summary'])
    event.add('description', event_data['description'])

    start_datetime_str = f"{event_data['start_date']} {event_data['start_time']}"
    end_datetime_str = f"{event_data['end_date']} {event_data['end_time']}"

    timezone = pytz.timezone(event_data['timezone'])

    start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone)
    end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone)

    event.add('dtstart', start_datetime)
    event.add('dtend', end_datetime)

    calendar.add_component(event)

    return calendar.to_ical()

def save_ics_file(ics_data: bytes, save_path: str = "/Users/Raneet/Desktop/schedly/calendar_creator/") -> str:
    file_name = "event_created.ics"
    file_path = os.path.join(save_path, file_name)
    os.makedirs(save_path, exist_ok=True)
    
    with open(file_path, 'wb') as f:
        f.write(ics_data)
    
    return file_path

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

@app.post("/extract/")
async def extract_email_info(request: EmailRequest):
    """
    Extract time, place, location, and date from the email content provided by the user.

    Args:
    - request (EmailRequest): The request object containing the email content.

    Returns:
    - dict: Extracted time, place, location, and date information.
    """

    email_content = request.email_content

    try:
        extracted_info = extract_time_place_location_date(email_content, groq_api_key)

        if 'error' in extracted_info:
            raise HTTPException(status_code=500, detail=f"Error: {extracted_info['error']}")

        return {"extracted_info": extracted_info}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting information: {str(e)}")

@app.post("/generate_ics/")
async def generate_ics(event_data: EventData):
    """
    Generate an ICS file based on the event data provided by the user.

    Args:
    - event_data (EventData): The request object containing event details.

    Returns:
    - dict: Message and file path of the generated ICS file.
    """
    try:
        event_data_dict = event_data.dict()
        
        ics_data = create_ics_file(event_data_dict)
        
        save_path = "/Users/Raneet/Desktop/schedly/calendar_creator/"
        file_path = save_ics_file(ics_data, save_path)
        
        return {"message": "ICS file generated successfully", "file_path": file_path}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ICS file: {str(e)}")

@app.post("/process_email/")
async def process_email(request: EmailRequest):
    """
    Process an email to analyze sentiment and generate an AI response.

    Args:
    - request (EmailRequest): The request object containing the email content.

    Returns:
    - dict: The sentiment label, AI-generated response, and a success message.
    """
    email_content = request.email_content

    try:
        
        chat_history = []
        
    
        response, sentiment_label = process_email_content(email_content, chat_history, groq_api_key)

        return {
            "response": response,
            "sentiment": sentiment_label,
            "message": "Email processed successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")
