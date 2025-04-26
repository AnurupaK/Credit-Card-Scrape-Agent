from crewai import Agent, LLM
from dotenv import load_dotenv
import os
from .tools import scrape_tool

# Load environment variables
load_dotenv()

# Initialize LLM with API key and model
llm = LLM(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-2.0-flash"
)

# Create Credit Card Scraper agent
credit_card_miner = Agent(
    role="Credit Card Scraper",  
    goal="Extract and summarize credit card information",  
    verbose=False,  
    memory=True,  
    backstory=(
        "You're a financial product analyst specialized in credit cards. "
        "You analyze digital pages to pull fees, rewards, offers, and other benefits."
    ),
    tools=[scrape_tool],  
    llm=llm,  
    allow_delegation=False  
)
