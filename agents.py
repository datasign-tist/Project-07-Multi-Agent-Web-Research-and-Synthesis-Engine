# ---------------------------------------------------------
# Step 03: Agent & Chain Definitions
# This file defines the core intelligence of the Multi-Agent System.
# It includes autonomous tools-using agents (Search, Reader) and 
# LCEL processing chains (Writer, Critic).
# ---------------------------------------------------------

from langchain.agents import create_agent 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv

# Load environment variables (API keys) securely from the .env file
load_dotenv() 

# ---------------------------------------------------------
# Core LLM Initialization
# ---------------------------------------------------------
# Using gpt-4o-mini for efficient, fast reasoning.
# Temperature is set to 0 for highly deterministic, factual, and 
# reliable outputs (crucial for accurate research pipelines).
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) 


# ---------------------------------------------------------
# Search Agent setup
# ---------------------------------------------------------
def build_search_agent():
    """
    Creates an autonomous agent equipped with the 'web_search' tool.
    Its primary job is to scour the web using Tavily to find relevant 
    URLs and snippets based on the user's research topic.
    """
    return create_agent( 
        model=llm,
        tools=[web_search]
    )


# ---------------------------------------------------------
# Reader Agent setup
# ---------------------------------------------------------
def build_reader_agent():
    """
    Creates an autonomous agent equipped with the 'scrape_url' tool.
    Its job is to take the high-quality URLs found by the Search Agent 
    and deep-read (scrape and clean) the actual page content.
    """
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# ---------------------------------------------------------
# Writer Chain Creation (LCEL Pipeline)
# ---------------------------------------------------------
# The Writer Chain doesn't need external tools. It uses standard LLM 
# capabilities to synthesize the gathered research into a structured report.
writer_prompt = ChatPromptTemplate.from_messages( 
    [
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
    ]
)

# Pipeline: Prompt -> LLM -> String Output (removes raw metadata)
# It takes the 'topic' and 'research' variables, synthesizes them, and outputs a final summary.
writer_chain = writer_prompt | llm | StrOutputParser() 


# ---------------------------------------------------------
# Critic Chain Creation (LCEL Pipeline)
# ---------------------------------------------------------
# The Critic Chain acts as an automated QA (Quality Assurance) step.
# It reviews the Writer's output to ensure it meets professional standards.
critic_prompt = ChatPromptTemplate.from_messages(
    [
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
    ]
)

# Pipeline: Prompt -> LLM -> String Output
# It takes the generated 'report', evaluates it, and returns structured feedback.
critic_chain = critic_prompt | llm | StrOutputParser()