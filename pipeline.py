# ---------------------------------------------------------
# Step 04: The Orchestration Pipeline
# ---------------------------------------------------------

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    state = {}

    # ---------------------------------------------------------
    # Phase 01: Search Agent
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print('''Phase 01 : Search Agent is Working ...''')
    print("\n" + "="*50)

    search_agent = build_search_agent()
    
    # Standard AgentExecutors use the "input" key
    search_result = search_agent.invoke({
        "input": f"Find recent, reliable and detailed information about : {topic}"
    })
    
    # Standard AgentExecutors return the final answer in the "output" key
    state["Search_Results"] = search_result['output']
    print("\n Search Result ", state['Search_Results'])

    # ---------------------------------------------------------
    # Phase 02: Reader Agent
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print('''Phase 02 : Reader Agent is Scraping Information ...''')
    print("\n" + "="*50)

    reader_agent = build_reader_agent()
    
    reader_result = reader_agent.invoke({
        "input": (
            f"Based on the following search results about '{topic}',\n"
            f"Pick the most relevant URL and Scrape it for deeper content.\n\n"
            f"Search Results :\n{state['Search_Results'][:800]}"
        )
    })

    state['Scraped_Content'] = reader_result['output']
    print("\n Scraped Content: \n ", state['Scraped_Content'])

    # ---------------------------------------------------------
    # Phase 03: Writer Chain 
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print('''Phase 03 : Writer Agent is Writing Research ...''')
    print("\n" + "="*50)

    research_combined = (
        f"Search Results : \n {state['Search_Results']} \n\n"
        f"Detailed Scraped Content : \n {state['Scraped_Content']}"
    )
    
    state["Report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\n Final Report: \n ", state['Report'])

    # ---------------------------------------------------------
    # Phase 04: Critic Chain
    # ---------------------------------------------------------
    print("\n" + "="*50)
    print('''Phase 04 : Critic Agent is Verifying Reports ...''')
    print("\n" + "="*50)

    state["Feedback"] = critic_chain.invoke({
        "report": state['Report']
    })
    print("\n Critic Report: \n ", state['Feedback'])

    return state