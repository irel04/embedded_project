import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Supabase credentials
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_ANON_KEY")

# Check if credentials are loaded properly
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials are missing from the environment variables.")

# Initialize Supabase client
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
