# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from extractor import extract_time_place_location_date

app = FastAPI()

groq_api_key = "enter api key"

class EmailRequest(BaseModel):
    email_content: str

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


@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Information Extraction API. Use /extract/ for extraction."}

