import os
from datetime import datetime
from dotenv import load_dotenv
from cloud_memory import load_cloud_memory, save_cloud_memory
from llm.groq_client import ask_goku # pyright: ignore[reportMissingImports]

load_dotenv()

def strip_for_llm(conversation):
    """
    Groq does NOT accept extra fields like timestamp.
    This function removes everything except role + content.
    """
    clean_messages = []
    for msg in conversation:
        clean_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    return clean_messages

def main():
    print("I'm Goku!")

    user_id = "terminal-user"  # placeholder for terminal testing

    # Load old memory from Supabase
    conversation = load_cloud_memory(user_id)

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goku: Until next time!")
            break

        # Add USER message WITH timestamp (only stored in database)
        conversation.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Prepare messages for LLM → strip timestamps
        llm_conversation = strip_for_llm(conversation)

        # Get reply from Groq
        reply = ask_goku(llm_conversation)
        print("Goku:", reply)

        # Add ASSISTANT reply WITH timestamp (only stored in database)
        conversation.append({
            "role": "assistant",
            "content": reply,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Save to Supabase (auto-trimming + summarization applied inside)
        save_cloud_memory(user_id, conversation, user_input)

if __name__ == "__main__":
    main()
