from crewai import Task
from .tools import scrape_tool
from .agents import credit_card_miner
from modules.scrape_format import scrape_format

# Function to create a credit card scraping task
def credit_card_task(url: str) -> Task:
    description = scrape_format(url)
    return Task(
        description=description,
        expected_output="A structured dictionary of credit card details in JSON format.",
        tools=[scrape_tool],
        agent=credit_card_miner,
        input={"url": url}
    )
