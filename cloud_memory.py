from datetime import datetime
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

MAX_MESSAGES = 30  # keep only last 30 messages

def summarize_conversation(messages):
    """
    Create a simple summary of previous messages.
    For now, it just concatenates all messages into one string.
    You can improve this later with AI summarization.
    """
    summary = " ".join([msg["content"] for msg in messages])
    # You could call an LLM here instead of simple join to make smarter summaries
    return summary

def trim_memory(conversation):
    """
    Trim the conversation to the last MAX_MESSAGES messages.
    Older messages are summarized into a single system message.
    """
    if len(conversation) > MAX_MESSAGES:
        old_messages = conversation[:-MAX_MESSAGES]
        summary_text = summarize_conversation(old_messages)
        conversation = [{"role": "system", "content": f"Summary of previous conversation: {summary_text}"}] \
                       + conversation[-MAX_MESSAGES:]
    return conversation

def save_cloud_memory(user_id, conversation, user_message):
    now = datetime.utcnow().isoformat()

    # Trim & compress memory before saving
    conversation = trim_memory(conversation)

    # Fetch existing record
    existing = supabase.table("memory").select("*").eq("user_id", user_id).execute()

    if existing.data:
        record = existing.data[0]
        new_count = record.get("message_count", 0) + 1
        new_total_length = record.get("total_message_length", 0) + len(user_message)

        supabase.table("memory").update({
            "conversation": conversation,
            "last_seen": now,
            "message_count": new_count,
            "total_message_length": new_total_length
        }).eq("user_id", user_id).execute()

    else:
        supabase.table("memory").insert({
            "user_id": user_id,
            "conversation": conversation,
            "first_seen": now,
            "last_seen": now,
            "message_count": 1,
            "total_message_length": len(user_message)
        }).execute()

def load_cloud_memory(user_id):
    """Load the conversation for a user from Supabase."""
    result = supabase.table("memory").select("conversation").eq("user_id", user_id).execute()
    if result.data:
        return result.data[0]["conversation"]
    return []  # return empty list if no conversation exists
