from crewai_tools import FileReadTool, DirectoryReadTool, FirecrawlScrapeWebsiteTool, BaseTool, tool
from pathlib import Path

@tool
def structured_agent_tool(query:str) -> str:
    """A structured retriever agent tool. The agent takes in a string query and based on it creates and executes an SQL command on a database, retrieving relevant data. Args: query: What needs being found in the SQL dataset. Example Arg: 'Which country's customers spent the most?'"""
    # Loading API Keys
    from dotenv import load_dotenv
    load_dotenv()
    import getpass
    import os
    from langchain_openai import ChatOpenAI
    from langchain.chains import create_sql_query_chain
    from langchain_community.utilities import SQLDatabase

    # Construct the path to the database file
    openai_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=openai_key)

    if not os.environ.get("LANGCHAIN_API_KEY"):
        os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
        os.environ["LANGCHAIN_TRACING_V2"] = "true"


    # Just testing querying the dataset
    #Initializing the dataset
    db_path = "/Users/gleb/Desktop/CS/Projects/Event/Data_analyst/Structured_agent/music_artists_chinook.db"
    # Use this path when initializing the database
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    #Initializing the llm
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key="sk-proj-UWUQpPNJkUViyGzbZ6v3T3BlbkFJJT7aybLdzYDdtjcyTXLE")


    ####### ---------------------------- AGENT ---------------------------- ########
    # Lists SQL tools:
        # Create and execute querie tool
        # Check query syntax with schemas tool
        # Retrieve table descriptions tool
        # ... And more
    from langchain_community.agent_toolkits import SQLDatabaseToolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    tools
    # [QuerySQLDataBaseTool(description="Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.", db=<langchain_community.utilities.sql_database.SQLDatabase object at 0x11c5137a0>),
    #  InfoSQLDatabaseTool(description='Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables. Be sure that the tables actually exist by calling sql_db_list_tables first! Example Input: table1, table2, table3', db=<langchain_community.utilities.sql_database.SQLDatabase object at 0x11c5137a0>),
    #  ListSQLDatabaseTool(db=<langchain_community.utilities.sql_database.SQLDatabase object at 0x11c5137a0>),
    #  QuerySQLCheckerTool(description='Use this tool to double check if your query is correct before executing it. Always use this tool before executing a query with sql_db_query!', db=<langchain_community.utilities.sql_database.SQLDatabase object at 0x11c5137a0>, llm=ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x11c5c1df0>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x10f6fe150>, model_name='gpt-3.5-turbo-0125', openai_api_key=SecretStr('**********'), openai_proxy=''), llm_chain=LLMChain(prompt=PromptTemplate(input_variables=['dialect', 'query'], template='\n{query}\nDouble check the {dialect} query above for common mistakes, including:\n- Using NOT IN with NULL values\n- Using UNION when UNION ALL should have been used\n- Using BETWEEN for exclusive ranges\n- Data type mismatch in predicates\n- Properly quoting identifiers\n- Using the correct number of arguments for functions\n- Casting to the correct data type\n- Using the proper columns for joins\n\nIf there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.\n\nOutput the final SQL query only.\n\nSQL Query: '), llm=ChatOpenAI(client=<openai.resources.chat.completions.Completions object at 0x11c5c1df0>, async_client=<openai.resources.chat.completions.AsyncCompletions object at 0x10f6fe150>, model_name='gpt-3.5-turbo-0125', openai_api_key=SecretStr('**********'), openai_proxy='')))


    # System Prompt
    # This will consist of instructions for the agent of how to behave.
    from langchain_core.messages import SystemMessage

    SQL_PREFIX = """You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the below tools. Only use the information returned by the below tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    To start you should ALWAYS look at the tables in the database to see what you can query.
    Do NOT skip this step.
    Then you should query the schema of the most relevant tables."""

    system_message = SystemMessage(content=SQL_PREFIX)


    # Initializing agent
    from langchain_core.messages import HumanMessage
    from langgraph.prebuilt import create_react_agent

    agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)

    # The agent will execute multiple queries until it has the information it needs:
        # List available tables;
        # Retrieves the schema for three tables;
        # Queries multiple of the tables via a join operation.
    answer = []
    for s in agent_executor.stream({"messages": [HumanMessage(content=f"{query}")]}):
        answer.append(s)

    return (answer)