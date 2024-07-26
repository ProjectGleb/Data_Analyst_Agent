from crewai_tools import FileReadTool, DirectoryReadTool, FirecrawlScrapeWebsiteTool, BaseTool, tool


@tool
def rag_agent_tool(query:str) -> str:
    """An un-structured retriever agent tool. The agent takes in a string query and based on it makes a RAG search on a database, retrieving relevant data. Args: query: What needs being found in the RAG dataset. Example: 'What were the toolkits given to the agents in the WorkBench paper?', Arg: 'agent toolkits in the Workbench paper?'"""
    import os
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI
    from langchain import hub
    from langchain_chroma import Chroma
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain.document_loaders import PyMuPDFLoader  # Correct import for PDF loader

    # Load environment variables
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the language model
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=openai_api_key)

    # Load, chunk, and index the contents of the PDF.
    pdf_path = "/Users/gleb/Desktop/CS/Projects/Event/Data_analyst/Unstructured_agent/multi_agent_eval_paper_Workbench.pdf"  # Replace with your PDF file path
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create a vector store from the document splits
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the document
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Invoke the chain with a question
    # On which domain did the agent have the highest side effect % in WorkBench on? Why?"

    response = rag_chain.invoke(f"{query}")
    return(response)
