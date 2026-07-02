# ---------------------------------------------------------
# Step 03: Agent & Chain Definitions
# ---------------------------------------------------------

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv

load_dotenv() 

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0 , api_key=os.getenv("OPEN_AI_KEY")) 

# Agents require a specific prompt structure to know how to use tools
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an autonomous research assistant. Use your tools to fulfill the user's request accurately."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"), # Required for the agent to store its "thoughts"
])

def build_search_agent():
    tools = [web_search]
    # Create the agent logic
    agent = create_tool_calling_agent(llm, tools, agent_prompt)
    # The Executor is the actual runtime that runs the agent loop
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def build_reader_agent():
    tools = [scrape_url]
    agent = create_tool_calling_agent(llm, tools, agent_prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# ---------------------------------------------------------
# Writer Chain Creation (LCEL Pipeline)
# ---------------------------------------------------------
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

    Topic: {topic}
    Research Gathered:
    {research}
        
    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (list all URLs found in the research)

    Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser() 

# ---------------------------------------------------------
# Critic Chain Creation (LCEL Pipeline)
# ---------------------------------------------------------
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

    Report:
    {report}

    Respond in this exact format:
    Score: X/10
    Strengths:
    - ...
    - ...
    Areas to Improve:
    - ...
    - ...
    One line verdict:
    ..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()