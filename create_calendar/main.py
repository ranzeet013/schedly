# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from calendar_creator import create_ics_file, save_ics_file

app = FastAPI()

class EventData(BaseModel):
    summary: str
    description: str
    start_date: str  
    start_time: str  
    end_date: str    
    end_time: str   
    timezone: str = "UTC"  


@app.post("/generate_ics/")
async def generate_ics(event_data: EventData):
    try:
        event_data_dict = event_data.dict()
        
        ics_data = create_ics_file(event_data_dict)
        
        save_path = "path to ics file"
        file_path = save_ics_file(ics_data, save_path)
        
        return {"message": "ICS file generated successfully", "file_path": file_path}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ICS file: {str(e)}")

