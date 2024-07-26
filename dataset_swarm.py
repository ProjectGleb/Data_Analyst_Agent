


# Which artist produced the most albums? List all of the album titles they made. Also, which countries customer spent the most




## Multi-agent workflow:
# 1. Input query with info to find
# 2. Managing agent check the directory of both agents. DB must be tagged with metadata
# 3. Pasess the user_query to the agent 
# 4. Agents retrieve the info and return it to the managing agent. 
# 5. Pass it to the managing agent.
# 6. Managing agent makes sure the info is relevant, (if not, changes the query and tries again). 
# 7. Managing agent makes a report out of it/ simply returns it formatted. 
def main_logic(user_query):

    from dotenv import load_dotenv
    import os
    import warnings
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import FileReadTool, DirectoryReadTool, FirecrawlScrapeWebsiteTool, BaseTool, tool
    from Structured_agent.sql_agent import structured_agent_tool
    from Unstructured_agent.rag_agent import rag_agent_tool
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'



    # user_query = "Which country's customers spent the most?"
    # user_query = "Which artist produced the most albums? List all of the album titles they made. Also, which countries customer spent the most?"

    # Initialize tools
    file_read_tool = FileReadTool(file = '/Users/gleb/Desktop/CS/Projects/Event/Data_analyst/')
    directory_read_tool = DirectoryReadTool(directory='/Users/gleb/Desktop/CS/Projects/Event/Data_analyst/')

    ### --- DATA UPLOADING AGENT --- ###
    managing_agent = Agent(
        role="Managing Data Analyst",
        goal="Manage your sub-agents to retrieve structured or un-structured data relevant to the user_query and process it accordingly.",
        backstory="You are a manageing data analyst inside of a company, in charge of two other data analysts, one responsible for structured SQL database, another for un-structured RAG database.",
        tools=[directory_read_tool, structured_agent_tool, rag_agent_tool],
        allow_delegation=True,
        verbose=True,
        max_execution_time=None,
    )

    data_processing = Task(
        description=f"""user_query= {user_query}.\n
        1. Use a directory reading tool to look at files and databases in both of your junior agents disposal. The files have meta-data in their name which will give you a hint for which of the agents have access to the neccessary data for answering the user query.\n
        2. Use one of the agent tools to pass the query to the agent. Make a very specific query so it retrieves the information. The "un-structured agent" will be searching over un-structured RAG database, so your rquest will be used as to find similar entries. On the other hand "structured agent" will be searching over structured SQL database.\n 
        3. If the retrieved data by agents is irrelevant to the user query, or missess important details, itterate your query and try prompting them again a few times.\n
        4. Upon recieving enough information from your agents, process it according to the user_query. For example if a user asks you to create a report on the highest paying customers, it would require you to prompt one or more agents multiple times and after aggregating enough information compile a report detailing the highest paying customers.\n""",
        expected_output="Processed data according to the user query",
        agent=managing_agent
    )

    crew = Crew(
        agents=[managing_agent],
        tasks=[data_processing],
        verbose=2,
    )

    result = crew.kickoff()

    # My options:
    # 1. Give the agent other two agents as tools which will limit how it will retrieve info. 
    # 2. Create two more agents in crew ai. Allow them to call rag and sql as a tool. 

user_query = input("What would you like to know?: ")
# In Sam's agent eval work whats the accuracy of Chat-GPT using all tools vs required tools?
# 
main_logic(user_query)
