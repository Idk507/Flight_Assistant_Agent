


def setup_langchain():
    """Setup Langchain with tools and agent."""
    from langchain import hub
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain.tools import BaseTool, StructuredTool, tool
    from langchain.prompts import PromptTemplate
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    tools = [
        StructuredTool.from_function(
            func=get_flight_status,
            name="get_flight_status",
            description="Get flight status information"
        ),
        StructuredTool.from_function(
            func=get_departure_gate,
            name="get_departure_gate",
            description="Get departure gate information"
        )
    ]
    
    prompt = PromptTemplate(
        template="""Answer the following question as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of {tool_names}
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}""",
        input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
    )
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),  # Use environment variable
        convert_system_message_to_human=True,
        verbose=True
    )
    
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    # Example usage
    print(get_flight_status("EK226"))
    
    # Gemini example
    chat = setup_gemini()
    response = chat.send_message("What is the departure gate for flight EK226?")
    print(response.text)
    
    # Langchain example
    agent_executor = setup_langchain()
    response = agent_executor.invoke({
        "input": "What is the status of EK242? Always include the source and destination along with the timings"
    })
    print(response['output'])
