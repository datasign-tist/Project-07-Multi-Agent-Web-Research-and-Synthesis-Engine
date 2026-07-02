# ---------------------------------------------------------
# Step 04: The Orchestration Pipeline
# This file serves as the "Main Engine" of the application. 
# It stitches the agents and chains together into a sequential, 
# autonomous workflow using a shared memory state.
# ---------------------------------------------------------

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    """
    Executes the full multi-agent research pipeline.
    Data flows sequentially: Search -> Read/Scrape -> Write -> Critic.
    """
    
    # 'state' acts as the Shared Memory (or unified brain) for the pipeline.
    # Each agent reads from and writes to this dictionary to collaborate.
    state = {}

    # ---------------------------------------------------------------------------------------------------------------------------
    # Phase 01: Search Agent
    # Objective: Scour the web for broad, relevant context on the user's topic.
    # ---------------------------------------------------------------------------------------------------------------------------
    
    print("\n" + "="*50)
    print('''Phase 01 : Search Agent is Working ...''')
    print("\n" + "="*50)

    search_agent = build_search_agent()
    
    # Invoking the Search Agent with a specific prompt
    search_result = search_agent.invoke(
        {
            "Messages": [("user", f"Find recent, reliable and detailed information about : {topic}")]                      
        }
    )
    
    # Extract the agent's final response and store it in shared memory
    state["Search_Results"] = search_result['Messages'][-1].content
    print("\n Search Result ", state['Search_Results'])


    # ---------------------------------------------------------------------------------------------------------------------------
    # Phase 02: Reader Agent
    # Objective: Review the search results, pick the highest quality URL, and scrape its raw text.
    # ---------------------------------------------------------------------------------------------------------------------------
    
    print("\n" + "="*50)
    print('''Phase 02 : Reader Agent is Scraping Information ...''')
    print("\n" + "="*50)

    reader_agent = build_reader_agent()
    
    # The Reader Agent is fed the first 800 characters of the search results 
    # to decide which URL requires a deeper dive.
    reader_result = reader_agent.invoke(
        {
            "Messages": [("user",
                           f"Based on the following search results about '{topic}',"
                           f"Pick the most relevant URL and Scrape it for deeper content.\n\n"
                           f"Search Results :\n{state['Search_Results'][:800]}"
                          )]
        }
    )

    # Store the deeply scraped, cleaned text into shared memory
    state['Scraped_Content'] = reader_result['Messages'][-1].content
    print("\n Scraped Content: \n ", state['Scraped_Content'])


    # ---------------------------------------------------------------------------------------------------------------------------
    # Phase 03: Writer Chain 
    # Objective: Synthesize both broad search data and deep scraped data into a structured report.
    # ---------------------------------------------------------------------------------------------------------------------------
    
    print("\n" + "="*50)
    print('''Phase 03 : Writer Agent is Writing Research ...''')
    print("\n" + "="*50)

    # Combine data sources to give the Writer maximum context, preventing hallucinations
    research_combined = (
        f"Search Results : \n {state['Search_Results']} \n\n"
        f"Detailed Scraped Content : \n {state['Scraped_Content']}"
    )
    
    # Invoke the LCEL Writer Chain using the combined data
    state["Report"] = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined
        }
    )
    print("\n Final Report: \n ", state['Report'])


    # ---------------------------------------------------------------------------------------------------------------------------
    # Phase 04: Critic Chain
    # Objective: Act as automated Quality Assurance to evaluate and score the Writer's draft.
    # ---------------------------------------------------------------------------------------------------------------------------
    
    print("\n" + "="*50)
    print('''Phase 04 : Critic Agent is Verifying Reports ...''')
    print("\n" + "="*50)

    # Feed the generated report directly into the Critic LCEL chain
    state["Feedback"] = critic_chain.invoke(
        {
            "report": state['Report']
        }
    )
    print("\n Critic Report: \n ", state['Feedback'])

    # ---------------------------------------------------------------------------------------------------------------------------

    # Return the full state dictionary containing all steps, outputs, and metrics
    return state