import os
from crewai import Agent, Task, Process, Crew
from crewai_tools import SerperDevTool

# Set environment variables
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPER_API_KEY"] = "f671ff767248922b587a1ee4526255909c29207f"

# Initialize the tool for internet searching capabilities
SearchTools = SerperDevTool()

# Get business idea from user input
business_idea = input("What is your business idea explain for me and i will give you a conperhansive detail ? ")
file_name = input("Enter the filename which is saved your result ?")

marketer = Agent(
    role="Market Research Analyst",
    goal="Find out how big is the demand for my products and suggest how to reach the widest possible customer base",
    backstory="""You are an expert at understanding the market demand, target audience, and competition. This is crucial for 
		validating whether an idea fulfills a market need and has the potential to attract a wide audience. You are good at coming up
		with ideas on how to appeal to widest possible audience.
		""",
    tools=[SearchTools],
    verbose=True,
    allow_delegation=True,
)

technologist = Agent(
    role="Technology Expert",
    goal="Make assessment on how technologically feasible the company is and what type of technologies the company needs to adopt in order to succeed",
    backstory="""You are a visionary in the realm of technology, with a deep understanding of both current and emerging technological trends. Your 
		expertise lies not just in knowing the technology but in foreseeing how it can be leveraged to solve real-world problems and drive business innovation.
		You have a knack for identifying which technological solutions best fit different business models and needs, ensuring that companies stay ahead of 
		the curve. Your insights are crucial in aligning technology with business strategies, ensuring that the technological adoption not only enhances 
		operational efficiency but also provides a competitive edge in the market.""",
    tools=[SearchTools],
    verbose=True,
    allow_delegation=True,
)

business_consultant = Agent(
    role="Business Development Consultant",
    goal="Evaluate and advise on the business model, scalability, and potential revenue streams to ensure long-term sustainability and profitability",
    backstory="""You are a seasoned professional with expertise in shaping business strategies. Your insight is essential for turning innovative ideas 
		into viable business models. You have a keen understanding of various industries and are adept at identifying and developing potential revenue streams. 
		Your experience in scalability ensures that a business can grow without compromising its values or operational efficiency. Your advice is not just
		about immediate gains but about building a resilient and adaptable business that can thrive in a changing market.""",
    tools=[SearchTools],
    verbose=True,
    allow_delegation=True,
)

task1 = Task(
    description=f"""Analyze what the market demand for {business_idea}. 
		Write a detailed report with description of what the ideal customer might look like, and how to reach the widest possible audience. The report has to 
		be concise with at least 10 bullet points and it has to address the most important areas when it comes to marketing this type of business.
    """,
    agent=marketer,
    tools=[SearchTools],
    expected_output="A detailed report with at least 10 bullet points on market demand and customer profile."
)

task2 = Task(
    description=f"""Analyze how to produce {business_idea}. Write a detailed report 
		with description of which technologies the business needs to use in order to make High Quality products. The report has to be concise with 
		at least 10 bullet points and it has to address the most important areas when it comes to manufacturing this type of business. 
    """,
    agent=technologist,
    tools=[SearchTools],
    expected_output="A detailed report with at least 10 bullet points on production technologies."
)

task3 = Task(
    description=f"""Analyze and summarize marketing and technological report and write a detailed business plan with 
		description of how to make a sustainable and profitable {business_idea}. 
		The business plan has to be concise with 
		at least 10 bullet points, 5 goals and it has to contain a time schedule for which goal should be achieved and when.
    """,
    agent=business_consultant,
    tools=[SearchTools],
    expected_output="A concise business plan with at least 10 bullet points, 5 goals, and a timeline."
)

# Function to format the output
def format_output(raw_output):
    # Convert the CrewOutput object to string (adjust based on actual structure)
    output_str = str(raw_output)  # or use raw_output.output if that's the correct attribute
    
    # Remove double asterisks and format the text
    formatted_output = output_str.replace("**", "").strip()
    
    # Add line breaks and structure the content
    formatted_output = formatted_output.replace("\n\n", "\n").replace("\n", "\n\n")
    
    return formatted_output

crew = Crew(
    agents=[marketer, technologist, business_consultant],
    tasks=[task1, task2, task3],
    verbose=True,
    process=Process.sequential,
)

result = crew.kickoff()

# Format the result
formatted_result = format_output(result)

print("######################")
print(result)

# Save the result to a text file
with open(f"{file_name}.txt", "w") as file:
    file.write(str(result))