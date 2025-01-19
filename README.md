# Schedly

Schedly is a **FastAPI-based application** designed to revolutionize how users manage their schedules. By integrating **AI-powered Groq capabilities**, advanced **Natural Language Processing (NLP)** tools, and the **iCalendar library**, Schedly provides an intuitive and efficient way to handle email management, event scheduling, and sentiment analysis.

<p align="center">
  <img src="https://github.com/ranzeet013/FlirtyHuh/blob/main/image/1000029006.png](https://github.com/ranzeet013/schedly/blob/main/icon/1000029020.png" alt="Schedly Logo" width="300">
</p>

## Key Functionalities

### 1. **Email Content Extraction**
   - Extract critical scheduling details such as:
     - Time
     - Place
     - Location
     - Date
   - Powered by **Groq APIs**, utilizing the state-of-the-art **llama3-8b-8192 model** for precise information extraction.

### 2. **Event Calendar Creation**
   - Dynamically create `.ics` files to add events to calendars effortlessly.
   - Features include:
     - Time zone support
     - Accurate datetime conversion
   - Built using the **iCalendar library** to ensure compatibility across devices and platforms.

### 3. **Email Sentiment Analysis**
   - Analyze email content sentiment with **TextBlob** to classify tones as:
     - Positive
     - Negative
     - Neutral
   - Automatically generate **empathetic AI-based responses** tailored to the sentiment, fostering better communication.

## Features

### **Extract Email Information**
- Seamlessly parse email content to identify and extract essential scheduling details like time, location, and date.
- Employs **Groq's llama3-8b-8192 model** for unmatched accuracy in information extraction.

### **Generate ICS Files**
- Create `.ics` files dynamically, allowing users to integrate events into their calendars with ease.
- Robust features include:
  - Support for global time zones
  - Precise datetime conversions for seamless scheduling.

### **AI-Powered Email Sentiment Analysis**
- Analyze the sentiment of email content using **TextBlob** to determine:
  - Positive, negative, or neutral tones.
- Craft empathetic, AI-powered responses that align with the tone of the message, enhancing email interactions.

## Project Overview

Schedly is an **AI-powered application** designed to streamline email and scheduling tasks. By combining advanced natural language processing, calendar integrations, and sentiment analysis, Schedly simplifies the manual processes of extracting information, creating calendar events, and responding to emails. With its intuitive design and focus on user convenience, Schedly empowers users to stay organized, productive, and efficient effortlessly.

**Why Choose Schedly?**
- **Save Time**: Automates tedious tasks like parsing emails and creating calendar events.
- **Stay Organized**: Centralizes your scheduling needs in one platform.
- **Enhanced Communication**: Provides intelligent, empathetic responses to email tones.

Schedly combines cutting-edge **AI**, **NLP**, and **calendar integration** into a single platform to ensure effortless schedule management for all users.

## Installation Instructions

### 1. **Clone the Repository**
 ```bash
git clone https://github.com/ranzeet013/schedly.git
cd schedly
   ```

### 2. **Create a Virtual Environment**
 ```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

### 3. **Install Required Dependencies**
 ```bash
pip install -r requirements.txt
   ```

### 4. **Set Environment Variables**
 ```bash
GROQ_API_KEY=your_api_key
   ```

### 5. **Run the Application**
 ```bash
uvicorn main:app --reload
   ```

## Conclusion
Schedly streamlines scheduling and email management through AI-powered automation, offering features like extracting key details from emails, generating calendar events, analyzing sentiments, and providing empathetic AI-generated responses. It saves time, improves productivity, and lays the groundwork for future enhancements, ensuring it remains a reliable tool for efficient personal and professional organization.
