import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: Supabase credentials not found in environment variables.")
    # In production, we should probably raise an error here.
    # raise ValueError("Supabase credentials not found in environment variables.")

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL or "", SUPABASE_KEY or "")
