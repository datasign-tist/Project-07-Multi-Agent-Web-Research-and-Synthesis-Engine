import sys
from pipeline import run_research_pipeline

def main():
    try:
        topic = input("Topic to research: ").strip()
        if not topic:
            sys.exit("Error: Topic cannot be empty.")
            
        print(f"Researching: '{topic}'...\n")
        final_state = run_research_pipeline(topic)
        
        print("\n--- FINAL REPORT ---")
        print(final_state.get("Report", "No report generated."))
            
        print("\n--- CRITIC FEEDBACK ---")
        print(final_state.get("Feedback", "No feedback provided."))

    except KeyboardInterrupt:
        sys.exit("\nProcess interrupted.")
    except Exception as e:
        sys.exit(f"\nSystem error: {e}")

if __name__ == "__main__":
    main()