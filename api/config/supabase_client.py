from supabase import create_client
from decouple import config
SUPABASE_URL = config("SUPABASE_URL")
SUPABASE_API_KEY = config("SUPABASE_API_KEY")
HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
