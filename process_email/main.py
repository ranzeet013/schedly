from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email_processing import process_email_content

app = FastAPI()

class EmailRequest(BaseModel):
    email_content: str

@app.post("/process_email/")
async def process_email(request: EmailRequest):
    email_content = request.email_content
    groq_api_key = "enter api keyY"

    chat_history = []

    try:
        response, sentiment_label = process_email_content(email_content, chat_history, groq_api_key)
        
        return {
            "response": response,
            "sentiment": sentiment_label,
            "message": "Email processed successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")
