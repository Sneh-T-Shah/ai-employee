import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from crewai_tools import tool
import io
import os
import sys


# Define the Code Executor to run the generated Python code
@tool("Execute Python code and capture output")
def execute_code(code: str) -> str:
    """
    Execute the provided Python code and capture the output.
    """
    print("Executing the following code:")
    try:
        output = io.StringIO()  # Capture the output
        original_stdout = sys.stdout
        sys.stdout = output
        exec(code)
        captured_output = output.getvalue()
        sys.stdout = original_stdout
        print("Code executed successfully")
        print(captured_output)
        return captured_output
    except Exception as e:
        sys.stdout = original_stdout
        return str(e)

# API Key for ChatGroq
groq_api = "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"
llm = ChatGroq(temperature=0, model_name="llama-3.1-70b-versatile", api_key=groq_api)

# Define the analysis agent
def initialize_agents():
    
    # Define Agent 1: Analysis Type Selector
    analysis_type_selector = Agent(
        role="Analysis Type Selector",
        goal="Determine the most appropriate type of analysis based on the provided column names column names {column_names}.",
        backstory="You are an expert in data analysis techniques and can decide the best type of analysis to perform based on column names.",
        llm=llm,
        allow_delegation=False,
        tools=[],
        verbose=True
    )

    # Define Agent 2: Code Generator
    code_generator = Agent(
        role="Code Generator",
        goal="Generate Python code for analyzing data and creating charts. Assign appropriate names to the charts based on the analysis or the columns used. Save the charts as image files using the generated names.",
        backstory="You are an expert in Python and data visualization. You generate analysis code and dynamically assign appropriate names to the charts based on the data. Save them as image files in a specific folder.",
        llm=llm,
        allow_delegation=False,
        tools=[],
        verbose=True
    )

    # Define Agent 3: Code Executor
    code_executor = Agent(
        role="Code Executor",
        goal="Execute the generated Python code and return the results.",
        backstory="You execute Python code and return the results. Your task is to run code and capture its output.",
        llm=llm,  # This agent doesn't need an LLM
        allow_delegation=False,
        tools=[execute_code],
        verbose=True
    )

    # Define Agent 4: Results Compiler
    results_compiler = Agent(
        role="Results Compiler",
        goal="Compile and synthesize the results from the various analyses performed.",
        backstory="You compile and interpret the results from different analyses to provide a comprehensive summary.",
        llm=llm,
        allow_delegation=False,
        tools=[],
        verbose=True
    )

    # Define Tasks
    analysis_type_task = Task(
        description="""1) Analyze the provided column names: {column_names} and suggest the most appropriate type of analysis based on the type of schema
        2) Make the analysis plan such that it is at normal viewer level and not at data scientist level i.e do not make analysis like arima test or p-test.
        3) Make the analysis plan such that it is easy to understand and execute.
        4) Do not suggest process like perform eda or data-cleansing or also visulaization tasks
        5) Suggest some-thing like find the max sales of a in b, or something like that which is specific to the data
        6) If data is looking about tips that analysis based on that or if data is about sales then analysis based on that""",
        expected_output="The type of analysis to be performed.",
        agent=analysis_type_selector,
        async_execution=False
    )

    code_generation_task = Task(
        description="""
        Generate code without any comments specially do not comment code to load data i.e pd.read_csv line of code.
        Generate Python code  for the type of analysis suggested by the Analysis Type Selector agent.
        Take in mind the following things while generating the code:
        first you have to generate only one code snippet for the analysis type suggested by the Analysis Type Selector agent.
        the code should be in python and simple to execute. 
        I already have the data in pandas dataframe format in a variable called df.
        These are the data types of the columns in the dataframe: {dtypes} of columns {column_names} so make could accordingly:
        use print statements to print the results of the analysis.
        Try to avoid graphs and plots in the code as I will be generating them separately do statistical analysis instead.
        Make the code less complex and simple such that it is easy to execute and understand.
        Start the code as follows:
        import pandas as pd
        df = pd.read_csv("{file_name}")
        """,
        expected_output="Python code for performing the analysis.",
        agent=code_generator,
        async_execution=False
    )

    code_execution_task = Task(
        description="""Execute the generated Python code made by code generator agent using the tool.
                        **Do not change the code given to you by the code generator agent give it to tool as it is**
                        The tool will capture the output of the code execution and return it to you.
                        If it fails to execute the code, it will return the error message.
                        You must pass the code with proper indentation and syntax in string format..,
                        **If you get error in the code return that failed to compile code.
                        compile all the results of the code execution and return it to the results compiler agent.""",
        expected_output="Results of the analysis.",
        agent=code_executor,
        async_execution=False
    )

    results_compilation_task = Task(
        description="""Compile and synthesize results from various analyses to provide a 
        comprehensive summary along with explanation what results does the output shows .
        also print the outputs that you recieved with proper formatting i.e when you return the markdown make sure that it is properly formatted.""",
        expected_output="A summary of the insights derived from the analysis.",
        agent=results_compiler,
        async_execution=False
    )



    return Crew(agents=[analysis_type_selector,code_generator,code_executor,results_compiler],tasks=[analysis_type_task,code_generation_task,code_execution_task,results_compilation_task],verbose=2)


def get_analysis(file_name: str):
    df = pd.read_csv(file_name)

    # Initialize crew and agents
    crew = initialize_agents()

    # Extract column names for the task
    cols = ", ".join(df.columns)

    dtypes_string = df.dtypes.astype(str)
    # Define input for the task
    input_data = {"column_names":cols,"dtypes":dtypes_string, "file_name": file_name}

    # Kickoff the task and return the results
    results = crew.kickoff(input_data)
    return results


