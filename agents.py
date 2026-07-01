from langchain.agents import create_agent 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
import os
from dotenv import load_dotenv

load_dotenv() ## loading API keys

## setting up model
llm = ChatOpenAI(model = "gpt-4o-mini" , temperature = 0) # temperature = 1 --> highly creative --> more tokens

## Creation of Step 03: Search Agent

def build_search_agent():
    return create_agent ( 
                          model = llm,
                          tools = [web_search]
                        )


## Creation of Step 04 : Reader Agent

def build_reader_agent():
    return create_agent (
                          model = llm,
                          tools = [scrape_url]
                        )

## Writer Chain Creation

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
writer_chain = writer_prompt | llm | StrOutputParser() ##It will take the topic from user, get the url, fetch the detailed report and gives the final summary. 

## Critic Chain Creation

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

critic_chain = critic_prompt | llm | StrOutputParser() ## It takes the output report and gives critic replies for the report. 