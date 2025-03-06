import os
import gspread
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, SeleniumScrapingTool

# Set API Keys
os.environ["SERPER_API_KEY"] = "your-serper-api-key"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Authenticate Google Sheets
gc = gspread.service_account(filename="google-credentials.json")
sheet = gc.open("Athlete Information").sheet1  # Open the first sheet

# Tools
search_tool = SerperDevTool()
scraping_tool = SeleniumScrapingTool()

# Agents
form_finder = Agent(
    role="Form Finder",
    goal="Find recruiting questionnaire forms for colleges based on sport and name.",
    backstory="A skilled researcher in college sports recruitment.",
    tools=[search_tool],
    verbose=True
)

form_filler = Agent(
    role="Form Filler",
    goal="Extract athlete details from Google Sheets and complete the form.",
    backstory="A data entry expert that automates form submissions.",
    tools=[scraping_tool],
    verbose=True
)

response_collector = Agent(
    role="Response Collector",
    goal="Verify form submission success and record responses.",
    backstory="An expert in tracking submissions and storing results.",
    tools=[scraping_tool],
    verbose=True
)

# Function to extract athlete details
def get_athlete_data():
    data = sheet.get_all_records()
    return data[0]  # Assuming one athlete per form

# Function to run CrewAI workflow
def run_crew(college, sport):
    athlete_info = get_athlete_data()

    # Tasks
    find_form = Task(
        description=f"Search the internet for a recruiting questionnaire for {college}'s {sport} team.",
        expected_output="A direct link to the form.",
        tools=[search_tool],
        agent=form_finder
    )

    fill_form = Task(
        description="Use athlete details from Google Sheets to complete the form.",
        expected_output="A confirmation message after successful submission.",
        tools=[scraping_tool],
        agent=form_filler
    )

    check_submission = Task(
        description="Verify if the form submission was successful and store the response.",
        expected_output="A final report on submission status.",
        tools=[scraping_tool],
        agent=response_collector
    )

    # Crew Setup
    crew = Crew(
        agents=[form_finder, form_filler, response_collector],
        tasks=[find_form, fill_form, check_submission],
        process=Process.sequential
    )

    # Run Crew
    result = crew.kickoff(inputs={"college": college, "sport": sport})
    return result
